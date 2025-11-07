**Project Overview**

This project simulates a Query Plan Caching Mechanism that optimizes SQL query execution by storing and reusing query plans.
It demonstrates how databases can avoid regenerating execution plans for similar queries by using query normalization, ANTLR-based parsing, and mock plan generation.
The goal is to illustrate the internal workflow of a query cache mechanism in a simplified, Python-based environment.
***

**Problem Statement**

In real-world databases, executing queries repeatedly with different literal values often triggers redundant plan generation, consuming extra computation time.
For example, two queries with different parameter values but identical structure may produce identical execution plans — yet most systems will re-plan them each time.
This project addresses that inefficiency by implementing a query plan cache that recognizes structural similarity between queries and reuses existing plans.
***



**Technologies & Tools Used**

| **Tool / Module**          | **Purpose**                            | **Key Functionalities**                                                                                              |
| -------------------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Python 3**               | Core programming language              | - Implements the entire caching, normalization, and testing logic                                                    |
| **ANTLR (SQLite Grammar)** | SQL parsing and syntax tree generation | - Converts SQL queries into structured parse trees<br>- Helps in detecting subqueries and literals for normalization |
| **Regex (re module)**      | Text pattern matching                  | - Extracts table names, literals, and SQL clauses<br>- Identifies query structure elements (e.g., WHERE, JOIN)       |
| **hashlib**                | Unique ID generation                   | - Creates MD5-based plan IDs for identifying mock execution plans                                                    |
| **unittest.mock (patch)**  | Testing simulation tool                | - Overrides functions during tests to simulate plan generation delay and track performance                           |
<br>

**System requirements :**

1. Python 3.8+
2. Java JDK 8 or higher (required for ANTLR)
3. pip (Python package manager)
4. ANTLR v4.13.1 (for SQL grammar parsing)
<br>

***
<br> 

**System Architecture** / **Workflow**

The system follows a structured workflow that mimics how a real database engine handles query parsing, normalization, and plan caching.
Each SQL query passes through a defined series of stages — from parsing to caching and testing — to simulate the end-to-end process of query plan management.

**Workflow Overview**
```python
SQL Query Input
      │
      ▼
walker_listner.py  →  Uses ANTLR4 Parser + Listener to:
                        • Extract all SELECT blocks (outer + inner)
                        • Replace literals with placeholders (?)
                        • Mask nested subqueries intelligently
                        • Return:
                              - Full normalized query
                              - Leaf-level subqueries
                              - Outer query with leafs preserved
                              - Extracted literals
      │
      ▼
main.py (QueryPlanManager)
  ├── Uses normalized forms from listener
  ├── Searches cache:
  │     • Full query plan cache
  │     • Subquery-level plans (reused if matching)
  ├── If cache miss → Simulates plan generation using `generate_dummy_plan()`
  └── Updates cache metrics:
          - Total requests
          - Hits / Misses
          - Complexity score (proxy for planning cost)
      │
      ▼
test_main.py
  → Runs workload of 20–30 test queries (simple → nested)
  → Measures:
        • Execution time with & without cache
        • Cache hit ratio
        • Complexity-based performance simulation
      │
      ▼
📄 Output
  → Prints formatted query plans:
        - Outer plan + inner subplans
        - Cache hit/miss summary
        - Extracted literals
        - Final performance comparison matrix

```
**Explanation**

**ANTLR Integration:**
1. Uses the ANTLR4 SQLite grammar to parse SQL queries into a structured syntax tree.
2. This enables accurate recognition of SQL components such as SELECT, WHERE, and nested subqueries without manual string parsing.
<br>

**Walker–Listener Framework:**
1. Replaces the earlier manual DFS traversal with an event-driven listener mechanism.
2. ParseTreeWalker automatically triggers callbacks (e.g., enterSelect_core, enterLiteral_value) during traversal, simplifying nested query detection and literal extraction.
   
<br>

**Normalization Process:**
1. Each query is normalized by replacing literal values with "?" placeholders and masking nested subqueries intelligently.
2. The listener distinguishes between leaf-level subqueries (which get their own cached plan) and composite queries (which reuse inner plans).

<br>

**Cache Management:**
1. Normalized queries act as unique structural keys.
2. When a query is executed, the system checks the cache for a matching normalized form — fetching an existing plan if available or generating a mock plan if not.

<br>

**Performance Simulation & Testing:**

1. A separate test suite runs queries with and without caching, measuring:
2. Cache hits and misses
3. Complexity-based simulated plan generation cost
3. Total and per-query execution times
4. This demonstrates the effectiveness of query plan caching in reducing overall planning effort
  
***

**Core Components**

The project is divided into modular Python files, each responsible for a specific part of the query plan caching workflow.
This structure makes the system easy to maintain, extend, and test independently.
<br>
**File-Wise Breakdown**
| **File Name**             | **Purpose**                          | **Key Functionalities**                                                                                                                               |
| ------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Main.py`                 | Core cache and execution manager     | - Handles query normalization and cache lookups<br>- Generates mock plans for cache misses<br>- Tracks metrics (requests, hits, misses)               |
| `ParseExtractQuery.py`    | SQL parsing and normalization module | - Integrates ANTLR for query parsing<br>- Traverses parse tree using DFS<br>- Replaces literals and inner `SELECT`s with `?` placeholders             |
| `Test_main.py`            | Performance testing and benchmarking | - Runs multiple SQL queries (simple & nested)<br>- Simulates planning delays using complexity scores<br>- Compares performance with and without cache |
| `Grammar/SQLiteLexer.py`  | Lexer generated by ANTLR             | - Tokenizes SQL input into keywords, operators, and identifiers<br>- Forms base tokens for parsing                                                    |
| `Grammar/SQLiteParser.py` | Parser generated by ANTLR            | - Builds structured parse tree from SQL tokens<br>- Enables traversal for normalization and subquery extraction                                       |
| `Output.txt`              | Output log file                      | - Stores printed test outputs, normalized queries, plans, and cache performance metrics     |
<br>

**Note :**  SQL grammar (.g4) file taken from open source git hub.
<br> 

***

**End to End flow of Query**

```python
SQL Query Input
      │
      ▼
walker_listner.py  →  Uses ANTLR4 Parser + Listener to:
                        • Parse SQL into a structured parse tree
                        • Replace all literal values with '?'
                        • Identify leaf-level (straightforward) subqueries
                        • Mask nested subqueries intelligently
                        • Return:
                              - Full normalized query
                              - List of independent subqueries
                              - Outer query with inner queries replaced or preserved
                              - Extracted literals
      │
      ▼
main.py (QueryPlanManager)
  ├── Checks for existing plans in cache
  ├── If plan found → Cache Hit → Reuses plan
  ├── If plan not found → Cache Miss → Calls generate_dummy_plan()
  ├── Stores:
  │     • Normalized full query
  │     • Independent subquery plans
  └── Updates cache metrics:
          - Total Requests
          - Hits / Misses
          - Complexity Score
      │
      ▼
Output (Terminal / File)
  → Displays:
        • Outer + Inner Query Plans
        • Normalized Query Structure
        • Extracted Literals
        • Cache Hit/Miss Summary
        • Execution Time Comparison ( At the end of testing queries )
```
***

**ANTLR Implementation**

Why it’s used:
* To accurately identify SQL components like SELECT, WHERE, IN, and subqueries.
* To handle nested queries systematically without relying on string matching.
* To make the query normalization and plan geneSQL Query  →  ANTLR Parse Tree

<br>

Example :
For input query : **SELECT names FROM orders WHERE city = “Mumbai” and amount > 5000** <br> 
ANTLR return Tree like this

```python
sql_stmt_list
└── sql_stmt
    └── select_stmt
        ├── select_core
        │   ├── SELECT
        │   ├── result_column
        │   │   └── names
        │   ├── FROM
        │   ├── table_or_subquery
        │   │   └── orders
        │   ├── WHERE
        │   └── expr
        │       ├── expr
        │       │   ├── column_name → city
        │       │   ├── =
        │       │   └── literal_value → "Mumbai"
        │       ├── AND
        │       └── expr
        │           ├── column_name → amount
        │           ├── >
        │           └── literal_value → 5000
        └── SEMI
```
<br>

***
<br>

**Query Normalization Logic**

* Ensures that structurally identical SQL queries share the same cache entry, regardless of literal values.

* Achieved using ANTLR’s parse tree traversal with the Walker–Listener framework for precise query structure analysis.

* Replaces all variable parts — such as numbers, strings, and boolean constants — with placeholders (?).

* Detects and masks nested subqueries, allowing reuse of existing plans for identical query patterns.

* Produces normalized SQL, extracted literals, and leaf-level subqueries used as cache keys.

<br>

```python
SQL Query Input
      │
      ▼
┌───────────────────────────────┐
│ ANTLR4 Parser & Token Stream  │
│  → Builds a Parse Tree        │
└───────────────────────────────┘
      │
      ▼
Parse Tree Walker
      │
      ▼
┌──────────────────────────────────────────────┐
│ Listener 1: LiteralExtractorListener         │
│  • Detects all literal values                │
│  • Captures numbers, strings, booleans       │
│  • Example: "age = 25" → "age = ?"           │
└──────────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────────┐
│ Listener 2: SubqueryCollector                │
│  • Finds all SELECT blocks                   │
│  • Detects leaf-level subqueries (no nested) │
│  • Returns list of independent subqueries    │
│    → e.g., [ "SELECT salary FROM emp WHERE id = ?" ]  │
└──────────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────────┐
│ Listener 3: MaskInnerSelectsListener         │
│  • Walks through the tree                    │
│  • Replaces nested SELECTs with '?'          │
│  • Keeps outer SELECT body intact            │
│  • Example:                                  │
│    Input: SELECT * FROM A WHERE id IN (SELECT id FROM B)  │
│    Output: SELECT * FROM A WHERE id IN (?)                 │
└──────────────────────────────────────────────┘
      │
      ▼
┌──────────────────────────────────────────────┐
│ Listener 4: NormalizeQuery                   │
│  • Performs final cleanup                    │
│  • Replaces remaining literals with '?'      │
│  • Converts "IN (?, ?, ?)" → "IN (??)"       │
│  • Builds normalized SQL text                │
└──────────────────────────────────────────────┘
      │
      ▼
Final Normalization Output:
  ├── Full Normalized Query
  ├── List of Straightforward (Leaf) Subqueries
  ├── Masked Outer Query (with leafs replaced)
  └── Extracted Literals

```
<br>

**Why to store sub-queries ?**
* Each nested subquery is stored before being replaced with ?, ensuring it can be individually normalized and cached for future reuse.
* When a query reappears with a different outer structure but an identical subquery, the system can fetch the existing plan for that subquery from cache instead of re-planning it.

<br>

***

**Plan Caching Mechanism**<br>

When a query is normalized, the system uses its normalized form as a unique cache key.
If the same structural query appears again (even with different literal values), the cache returns the pre-generated plan instantly.
<br>

**Cache Structure**

```python
{
SELECT * FROM orders WHERE customer_id IN ( ? )
  Plan:
{
    "plan_id": "PLN_b03cabf1",
    "plan_type": "Index Scan",
    "tables": [
        "orders"
    ]
}
}
```
<br>

**key** : SELECT * FROM orders WHERE customer_id IN ( ? )

<br>

**Value** : {
    "plan_id": "PLN_b03cabf1",
    "plan_type": "Index Scan",
    "tables": [
        "orders"
    ]
}

<br>

**Cache Metrics**

```python
{
    "requests": 10,
    "hits": 7,
    "misses": 3
}
```

<br>

**Cache Metrics**: Track the performance of the caching system by counting total requests, cache hits, and cache misses to measure overall efficiency and reuse effectiveness.

***
<br>

**End to End flow of input query from Parsing --> Normalization --> Plan :** 
<br> 

![Alt text](https://github.com/Area115/Query_Plan_Caching/blob/8a4897be5757255fb5d9c102f8718656fd32dd11/images/functional_diagram_updated.png)

<br> 

*** 

**Mock Plan Generation**

When a query results in a cache miss, the system simulates how a real database optimizer would generate an execution plan.
Instead of running actual SQL, a mock (dummy) plan is created to represent how a query might be executed — helping test the caching workflow realistically.

```python
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
```
<br>

**Purpose**
* To simulate real-world plan generation
* Provide unique PlanID for each new structure after every cache miss.
<br>

**Query Complexity Estimation**
<br>

This module simulates the computational cost of generating a query plan, similar to how a real database optimizer evaluates query complexity.
Instead of executing SQL, it assigns a numerical complexity score based on SQL keywords and structure.
This score is later used in testing to introduce realistic time delays for plan generation.
<br>

```python
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
```
<br>

**Note :**

* The complexity score logic is designed purely to simulate realistic planning delays during testing.
* It ensures that complex queries (with multiple joins, filters, or aggregations) take longer to “plan” than simple ones,
  allowing the caching system to demonstrate its performance advantage more effectively.
<br>

**Cache Hit/Miss handling**
<br>

```python
execution_plan = {}
        for normalized_query in normalized_queries:
            self.cache_metrics["requests"] += 1

            # ✅ FIXED: use normalized_query (not normalized_form from outer scope)
            if normalized_query in self.query_cache and self.flag:
                self.cache_metrics["hits"] += 1
                execution_plan[normalized_query] = self.query_cache[normalized_query]
            else:
                self.cache_metrics["misses"] += 1
                new_plan = self.generate_dummy_plan(normalized_query)
                self.query_cache[normalized_query] = new_plan
                execution_plan[normalized_query] = new_plan
                self.total_complexity_score += self.estimate_query_complexity(normalized_query)
```
<br>

**Cache Behavior**
* When a query is executed, the system first checks if its normalized form exists in the cache.

* If found → Cache Hit ✅ → the stored plan is reused instantly (no delay).

* If not found → Cache Miss ❌ → a new mock plan is generated.

* During a cache miss, the system calculates the query’s complexity score.

* The higher the complexity, the longer the simulated planning delay (to mimic real database cost).
* Once generated, the new plan is stored in the cache for future reuse.
<br>

***
**Testing :**
```python
run command : python -u "d:\query_plan_cache\test_main.py" > .\output.txt
```
<br>

1. Check output.txt for output of each input query.
2. Set of queries will run first with using cache and then without using cache.
3. At the end performance comparison will appear to show how cache improves efficiency after reusing stored plans.

![Alt text](https://github.com/Area115/Query_Plan_Caching/blob/172a19c8d71b6b1c7d1d8e92e256c7b2d1407784/images/output.png)
<br>

**Testing with Monkey Patching and Simulated Delay**
1. unittest.mock.patch is used to simulate time delay to show difference between with cache and without cache.
2. Formula used : delay = 0.05 * complexity, showing how cache hits save time by skipping the simulated planning phase.

**Performance Comparison ( With and Without Cache ) :**
![Alt text](https://github.com/Area115/Query_Plan_Caching/blob/170665ebb12c68e29b9357e01edf842b89d6adde/images/Screenshot%20(32).png)

<br>

***

**Flow-Diagram**

![Alt text](https://github.com/Area115/Query_Plan_Caching/blob/dbf4dfdc2a19aa584aed9e7ebcc4fe7e4c62469c/images/Architecture_Diagram.png)
<br>
***

**AI Policy Usage :**
<br>

**AI Tools Used in Development**
<br>

This project was developed with limited assistance from AI tools, primarily for structural guidance and documentation clarity.
All core logic, design flow, and implementation decisions were created independently.
<br>

**Code Generation and Architecture:**
1. AI assistance was used to understand ANTLR parse tree traversal concepts and explore possible implementation patterns.
2. Code templates and structure suggestions were taken for mock plan generation, complexity scoring, and testing setup — but the logic, algorithm, and implementation were entirely self-designed.
3. Minor support was used for syntax corrections and improving code readability.
   <br>
   
**Documentation:**

1. AI helped in drafting technical explanations and architectural documentation for better clarity.
2. It also assisted in structuring the README and creating diagram outlines for visualization










