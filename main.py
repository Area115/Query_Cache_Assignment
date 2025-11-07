import re, hashlib, json, copy
from walker_listner import ExtractAndNormalize
import show_plan

class QueryPlanManager():
    def __init__(self):
        self.query_cache = {}
        self.cache_metrics = {
            "requests": 0,
            "hits": 0,
            "misses": 0,
        }
        self.extract_and_normalize = ExtractAndNormalize()
        self.use_cache = True
        self.total_complexity_score = 0

    def estimate_query_complexity(self , query: str) -> int:
    
        query = query.lower()
        score = 0
        score += query.count("where") * 3
        score += query.count("and") * 2
        score += query.count("or") * 2
        score += query.count("join") * 5
        score += query.count("group by") * 4
        score += query.count("order by") * 4
        score += query.count("having") * 3
        if re.search(r"\b(sum|count|min|max|avg)\b", query):
            score += 5
        score += query.count("select") 
        return max(score , 1)

    def generate_dummy_plan(self, query: str):
        """
        Generate a dummy JSON query plan for cache miss.
        """
        plan_id = "PLN_" + hashlib.md5(query.encode()).hexdigest()[:8]
        plan_type = "Index Scan" if re.search(r"\bWHERE\b", query, re.IGNORECASE) else "Full Table Scan"

        tables = re.findall(r"FROM\s+(\w+)", query, re.IGNORECASE)
        joins = re.findall(r"JOIN\s+(\w+)", query, re.IGNORECASE)
        all_tables = list(set(tables + joins))

        plan = {
            "plan_id": plan_id,
            "plan_type": plan_type,
            "tables": all_tables or ["unknown_table"],
        }
        return json.dumps(plan, indent=4)

    def fetch_or_generate_query_plan(self, sql_query) -> dict:
        cache_hits_of_current_query = 0 

        full_norm, leaf_list, outer_keep_leaf, literals = self.extract_and_normalize.process(sql_query) 
        full_norm_copy = full_norm

        # Check if the query is a single (non-nested) SELECT
        if len(leaf_list) == 1 and leaf_list[0] == full_norm:
            # This means input query is a single query
            self.cache_metrics["requests"] += 1
            if full_norm in self.query_cache and self.use_cache: 
                cache_hits_of_current_query += 1
                self.cache_metrics["hits"] += 1
                return self.query_cache[full_norm], literals, cache_hits_of_current_query
            else:
                self.cache_metrics["misses"] += 1
                new_plan = self.generate_dummy_plan(full_norm)
                self.total_complexity_score += self.estimate_query_complexity(full_norm)
                self.query_cache[full_norm] = new_plan
                return new_plan, literals, cache_hits_of_current_query

        # Check for full query hit in cache
        if full_norm_copy in self.query_cache and self.use_cache:
            self.cache_metrics["hits"] += 1
            self.cache_metrics["requests"] += 1
            cache_hits_of_current_query += 1
            return self.query_cache[full_norm_copy], literals, cache_hits_of_current_query
        else:
            # Cache miss for full query; check subqueries
            if leaf_list:
                sub_query_plans = {}
                for inner_query in leaf_list:
                    # Replace subquery with placeholder to avoid duplicate plan generation
                    pattern = re.escape(inner_query)
                    full_norm_copy = re.sub(pattern, '?', full_norm_copy)
                    self.cache_metrics["requests"] += 1

                    if inner_query in self.query_cache and self.use_cache:
                        cache_hits_of_current_query += 1
                        self.cache_metrics["hits"] += 1
                        cache_hits_of_current_query += 1
                        sub_query_plans[inner_query] = self.query_cache[inner_query]
                    else:
                        self.cache_metrics["misses"] += 1
                        new_plan = self.generate_dummy_plan(inner_query)
                        self.total_complexity_score += self.estimate_query_complexity(inner_query)
                        sub_query_plans[inner_query] = new_plan 
                        self.query_cache[inner_query] = new_plan 

                # Generate plan for main (outer) query after subquery plans
                new_plan_for_main_query = self.generate_dummy_plan(full_norm_copy)
                self.total_complexity_score += self.estimate_query_complexity(full_norm_copy)
                self.cache_metrics["requests"] += 1
                self.cache_metrics["misses"] += 1

                final_plan = {}
                final_plan[full_norm_copy] = new_plan_for_main_query
                final_plan["Inner Query Plans : "] = sub_query_plans
                self.query_cache[full_norm] = final_plan
                return final_plan, literals, cache_hits_of_current_query

            else:
                # Simple query — no subqueries
                self.cache_metrics["misses"] += 1
                self.cache_metrics["requests"] += 1
                new_plan = self.generate_dummy_plan(full_norm_copy)
                self.total_complexity_score += self.estimate_query_complexity(full_norm_copy)
                self.query_cache[full_norm_copy] = new_plan
                return new_plan, literals, cache_hits_of_current_query





if __name__ == "__main__" : 
    # ---------------- Test Driver ---------------- #
    query1 = """SELECT * FROM customers WHERE id = 101"""

    query2 = """SELECT * FROM customers WHERE id = 202;"""

    query_plan_manager = QueryPlanManager()

    plan1 , literals , cache_hits_of_current_query  = query_plan_manager.fetch_or_generate_query_plan(query1)
    show_plan.display_query_plan_results(plan1 , literals , query_plan_manager.cache_metrics , query1 , cache_hits_of_current_query)
    print(query_plan_manager.total_complexity_score)

    plan1 , literals , cache_hits_of_current_query = query_plan_manager.fetch_or_generate_query_plan(query2)
    show_plan.display_query_plan_results(plan1 , literals , query_plan_manager.cache_metrics , query2 , cache_hits_of_current_query)
