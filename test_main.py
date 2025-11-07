import time
import re
import pandas as pd
from unittest.mock import patch
from main import QueryPlanManager  # import your main class
import show_plan

scores = []

# ===============================
# 🧩 Test Query Workload
# ===============================
test_queries = [
    # 1–3: Simple structure repeating (base cache warm-up)
    "SELECT * FROM customers WHERE id = 101",
    "SELECT * FROM customers WHERE id = 202",
    "SELECT * FROM customers WHERE id = 303",

    # 4–6: Same structure, nested single-level subquery (pattern repetition)
    """
    SELECT * FROM users
    WHERE city_id IN (
        SELECT id FROM cities WHERE country = 'India'
    )
    """,
    """
    SELECT * FROM users
    WHERE city_id IN (
        SELECT id FROM cities WHERE country = 'USA'
    )
    """,
    """
    SELECT * FROM users
    WHERE city_id IN (
        SELECT id FROM cities WHERE country = 'Japan'
    )
    """,

    # 7–9: Two-level nested subquery (complex but same pattern)
    """
    SELECT * FROM orders
    WHERE customer_id IN (
        SELECT id FROM customers
        WHERE region_id IN (
            SELECT id FROM regions WHERE zone = 'North'
        )
    )
    """,
    """
    SELECT * FROM orders
    WHERE customer_id IN (
        SELECT id FROM customers
        WHERE region_id IN (
            SELECT id FROM regions WHERE zone = 'South'
        )
    )
    """,
    """
    SELECT * FROM orders
    WHERE customer_id IN (
        SELECT id FROM customers
        WHERE region_id IN (
            SELECT id FROM regions WHERE zone = 'East'
        )
    )
    """,

    # 10–12: Nested query inside WHERE with aggregation (same pattern)
    """
    SELECT name FROM employees
    WHERE salary > (
        SELECT AVG(salary) FROM employees WHERE dept = 'IT'
    )
    """,
    """
    SELECT name FROM employees
    WHERE salary > (
        SELECT AVG(salary) FROM employees WHERE dept = 'Finance'
    )
    """,
    """
    SELECT name FROM employees
    WHERE salary > (
        SELECT AVG(salary) FROM employees WHERE dept = 'HR'
    )
    """,

    # 13–15: Multi-level nested queries (deepest structure)
    """
    SELECT name FROM managers
    WHERE dept_id IN (
        SELECT id FROM departments
        WHERE division_id IN (
            SELECT id FROM divisions WHERE region = 'West'
        )
    )
    """,
    """
    SELECT name FROM managers
    WHERE dept_id IN (
        SELECT id FROM departments
        WHERE division_id IN (
            SELECT id FROM divisions WHERE region = 'East'
        )
    )
    """,
    """
    SELECT name FROM managers
    WHERE dept_id IN (
        SELECT id FROM departments
        WHERE division_id IN (
            SELECT id FROM divisions WHERE region = 'South'
        )
    )
    """,

    # 16–17: New unique patterns (expected cache miss)
    """
    SELECT * FROM invoices
    WHERE total > 5000
    AND customer_id IN (
        SELECT id FROM customers WHERE city = 'Pune'
    )
    """,
    """
    SELECT product_name FROM products
    WHERE category_id IN (
        SELECT id FROM categories WHERE parent_category = 'Electronics'
    )
    AND price BETWEEN 1000 AND 2000
    """
]


# ===============================
# 🧩 Test Function
# ===============================
def test_query_plan_cache(use_cache: bool):
    planner = QueryPlanManager()
    planner.use_cache = use_cache

    print(" Starting Cache Simulation Test\n")
    start_time = time.perf_counter()

    for idx, query in enumerate(test_queries, start=1):
        print(f" Query {idx}:")
        print(query.strip())

        plans, literals  , cache_hits_of_current_query = planner.fetch_or_generate_query_plan(query)
        show_plan.display_query_plan_results(plans , literals , planner.cache_metrics , query , cache_hits_of_current_query)

    total_complexity = planner.total_complexity_score
    score_generated = total_complexity or 0
    print("\n------------------------------------------")
    print(" Test Completed")
    print(f" Final Cache Metrics: {planner.cache_metrics}")
    print("Total Complexity score generated is", score_generated)
    scores.append(score_generated)
    print("------------------------------------------\n")

    total_time = time.perf_counter() - start_time
    return {
        "requests": 17,
        "hits": planner.cache_metrics["hits"],
        "misses": planner.cache_metrics["misses"],
        "total_complexity": score_generated,
        "total_time": total_time,
    }


# ===============================
# 🧩 Summary Report Function
# ===============================
def print_performance_report(results_with_cache, results_without_cache):
    print(" FINAL PERFORMANCE COMPARISON MATRIX")
    print("=========================================\n")

    data = {
        "Metric": [
            "Total Queries Executed",
            "Cache Hits",
            "Cache Misses",
            "Hit Ratio (%)",
            "Total Complexity Score",
            "Total Time (s)",
            "Avg Time per Query (ms)",
        ],
        "Without Cache": [
            results_without_cache["requests"],
            0,
            results_without_cache["requests"],
            0.0,
            results_without_cache["total_complexity"],
            f"{results_without_cache['total_time']:.2f}",
            f"{(results_without_cache['total_time'] / results_without_cache['requests']) * 1000:.2f}",
        ],
        "With Cache": [
            results_with_cache["requests"],
            results_with_cache["hits"],
            results_with_cache["misses"],
            round(
                (results_with_cache["hits"] / max(1, results_with_cache["requests"])) * 100, 2
            ),
            results_with_cache["total_complexity"],
            f"{results_with_cache['total_time']:.2f}",
            f"{(results_with_cache['total_time'] / results_with_cache['requests']) * 1000:.2f}",
        ],
    }

    df = pd.DataFrame(data)
    print(df.to_string(index=False))
    print("\n Observation: Caching significantly reduces total execution time while maintaining the same workload.\n")


# ===============================
# 🧩 Main Execution Block
# ===============================
if __name__ == "__main__":

    # Keep reference to the original function before patching
    _real_generate_plan = QueryPlanManager.generate_dummy_plan

    # Fake function to simulate database planner cost
    def fake_generate_plan(self, query: str):
        complexity = self.estimate_query_complexity(query)
        delay = 0.05 * complexity  # 50 ms per complexity unit
        print(f" Simulating planning delay: {delay:.2f}s for complexity {complexity}")
        time.sleep(delay)
        return _real_generate_plan(self, query)

    # Run test with patch applied
    with patch.object(QueryPlanManager, "generate_dummy_plan", new=fake_generate_plan):

        print("\n========== RUNNING WITH CACHE ==========")
        results_with_cache = test_query_plan_cache(use_cache=True)
        print(f"Total time required (with cache): {results_with_cache['total_time']:.2f}s")

        print("\n========== RUNNING WITHOUT CACHE ==========")
        results_without_cache = test_query_plan_cache(use_cache=False)
        print(f"Total time required (without cache): {results_without_cache['total_time']:.2f}s")

    print_performance_report(results_with_cache, results_without_cache)
