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
Input SQL Query
      │
      ▼
ANTLR Parser (SQLite Grammar)
      │
      ▼
Parse Tree Generation
      │
      ▼
DFS Traversal on Tree
  → Identify all SELECT nodes
  → Extract subqueries
  → Replace literals & inner SELECTs with '?'
      │
      ▼
Normalized Query Output
  → Used as cache key
  → Collect literals list
      │
      ▼
Check Cache
  ├── Cache Hit → Fetch existing plan
  └── Cache Miss → Generate new mock plan (JSON)
      │
      ▼
Return:
  • Normalized Query  
  • Execution Plan  
  • Literal Bindings
```
**Explanation**
* ANTLR Integration: Converts SQL queries into a parse tree for structural analysis.
* DFS Traversal: Recursively visits all nodes to find select_core and literal_value elements.
* Normalization: Replaces literals and nested subqueries with ? placeholders for plan reuse.
* Cache Management: Normalized queries serve as unique keys for fetching or generating mock plans.
* Testing Simulation: Measures time, cache hits, and misses to evaluate cache performance.
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
ParseExtractQuery.py  →  Normalizes Query  →  Returns normalized form + literals
      │
      ▼
Main.py (QueryPlanManager)
  ├── Checks cache for existing plan
  ├── If miss → calls generate_dummy_plan()
  └── Updates cache metrics (hit/miss count)
      │
      ▼
Test_main.py
  → Executes multiple queries
  → Measures cache effectiveness & total execution time
      │
      ▼
Output.txt
  → Stores results and metrics for analysis
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

Usefulness of ANTLR tree : 
* Efficient traversal through each node and track nested SELECT and Literal values.
* Depth First Search logic helps to detect sub-queries which can be fetch from cache if available.<br>

***
<br>

**Query Normalization Logic**

Query normalization ensures that structurally similar SQL queries are treated as identical by the caching system — even if their literal values differ.
This is achieved using ANTLR parse tree traversal and Depth-First Search (DFS) to replace variable components like constants and inner subqueries with placeholders (?).
<br>
```python
def replace_node_with_placeholder(current_node):
            start = current_node.start.tokenIndex
            stop = current_node.stop.tokenIndex
            for i in range(start, stop + 1):
                token_stream.tokens[i].text = ""
            token_stream.tokens[start].text = "?"   
       
     if hasattr(node, "getRuleIndex"):
                rule = parser.ruleNames[node.getRuleIndex()]

                # Replace literal values
                if rule == "literal_value":
                    self.literals_list.append(node.getText())
                    replace_node_with_placeholder(node)
                    return

                # Replace quoted any_name (string identifiers)
                if rule == "any_name":
                    text = node.getText()
                    if text.startswith('"') and text.endswith('"'):
                        self.literals_list.append(text)
                        replace_node_with_placeholder(node)
                        return

                # Replace only inner SELECTs (not outermost)
                if rule == "select_core":
                    if flag:
                        flag = False
                    else:
                        replace_node_with_placeholder(node)
                        return
```
<br>


**Flow of Normalization and Extraction of sub-queries**
```python
SQL Query  →  ANTLR Parse Tree
      │
      ▼
DFS Traversal of Tree
  ├── Detect "literal_value" nodes
  │     → Replace with "?"
  │     → Store in literals list
  │
  ├── Detect "select_core" (inner SELECTs)
  │     → Extract and store subquery text (for logging/analysis)
  │     → Replace inner SELECT with "?"
  │
  └── Keep outermost SELECT unchanged
      │
      ▼
Return:
  • Normalized Query (used as cache key)
  • List of extracted literals (for binding)
  • Collected inner subquery texts (for reference/metrics)

```
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










