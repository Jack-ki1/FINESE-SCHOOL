"""SQL subtopics."""

SUBTOPICS = [
    dict(
        id="select-where",
        title="SELECT, WHERE & Filtering",
        hook="Every SQL query is really just describing the shape of the answer you want — the database figures out how to get there.",
        explanation=(
            "`SELECT` chooses which columns come back, `FROM` names the table, and `WHERE` filters rows before "
            "any grouping happens. SQL is declarative: you describe *what* you want, not the loop that fetches "
            "it, which is the biggest mental shift for anyone coming from an imperative language like Python.\n\n"
            "Comparison operators (`=`, `<>`, `>`, `BETWEEN`, `IN`, `LIKE`) combine with `AND`/`OR`, and operator "
            "precedence matters: `AND` binds tighter than `OR`, so mixing them without parentheses is a common "
            "source of subtly wrong results. `NULL` behaves unlike any normal value — `= NULL` never matches "
            "anything, even another NULL, which is why `IS NULL` / `IS NOT NULL` exist as dedicated operators."
        ),
        code=dict(
            lang="sql",
            label="Filtering with precedence and NULL handling",
            src=(
                "SELECT customer_id, order_total, status\n"
                "FROM orders\n"
                "WHERE (status = 'shipped' OR status = 'delivered')\n"
                "  AND order_total > 50\n"
                "  AND cancelled_at IS NULL\n"
                "ORDER BY order_total DESC\n"
                "LIMIT 10;"
            ),
        ),
        example=(
            "A support dashboard querying 'unresolved high-value tickets' needs both the OR (multiple valid "
            "statuses) and the AND (value threshold) — getting the parentheses wrong silently returns cancelled "
            "orders alongside shipped ones."
        ),
        best_practices=[
            "Always use `IS NULL` / `IS NOT NULL`, never `= NULL`.",
            "Parenthesize mixed AND/OR conditions explicitly rather than relying on precedence rules.",
            "Filter as early as possible in WHERE rather than fetching everything and filtering in application code.",
        ],
        pitfalls=[
            "Assuming `column = NULL` works like `column = 5` — it silently returns zero rows.",
            "Forgetting `LIMIT` on exploratory queries against a large table.",
        ],
        prompts=[
            "Show me every common pitfall with NULL in SQL WHERE clauses.",
            "How does operator precedence between AND and OR actually work?",
            "What's the difference between LIKE and a regex match in SQL?",
        ],
    ),
    dict(
        id="joins",
        title="JOINs Explained",
        hook="A JOIN is just a rule for pairing rows from two tables — the type of JOIN decides what happens to rows that don't have a match.",
        explanation=(
            "`INNER JOIN` keeps only rows that match in both tables. `LEFT JOIN` keeps every row from the left "
            "table regardless of a match, filling unmatched columns from the right table with NULL — the most "
            "common join for 'show me all X, and their Y if they have any'. `RIGHT JOIN` is the mirror image, and "
            "`FULL OUTER JOIN` keeps unmatched rows from both sides.\n\n"
            "Always JOIN with explicit `ON` conditions rather than relying on implicit comma joins — it's clearer "
            "and prevents accidental cross joins (every row paired with every row) when a join condition is "
            "missing. A CROSS JOIN is occasionally intentional (generating combinations), but it's almost always a "
            "bug when it happens by accident."
        ),
        code=dict(
            lang="sql",
            label="LEFT JOIN to include customers with zero orders",
            src=(
                "SELECT c.customer_name, COUNT(o.order_id) AS order_count\n"
                "FROM customers c\n"
                "LEFT JOIN orders o ON o.customer_id = c.customer_id\n"
                "GROUP BY c.customer_name\n"
                "ORDER BY order_count ASC;\n"
                "-- customers with 0 orders show up with order_count = 0,\n"
                "-- which an INNER JOIN here would have silently dropped."
            ),
        ),
        example=(
            "A churn-analysis report specifically needs LEFT JOIN because customers who placed zero orders are the "
            "exact rows the report cares about — an INNER JOIN would exclude the most important segment."
        ),
        best_practices=[
            "Use explicit `JOIN ... ON` syntax, never implicit comma joins.",
            "Reach for LEFT JOIN whenever 'rows with zero matches' are meaningful to the question you're answering.",
            "Alias tables (c, o) for readability once a query involves more than two tables.",
        ],
        pitfalls=[
            "Using INNER JOIN by default and silently dropping rows that have no match on the other side.",
            "Joining on a column without an index, causing a full table scan on large tables.",
        ],
        prompts=[
            "Walk me through the difference between all four JOIN types with a diagram-style example.",
            "When would I actually want a CROSS JOIN on purpose?",
            "Why does an INNER JOIN sometimes silently drop rows I expected to see?",
        ],
    ),
    dict(
        id="group-by-aggregations",
        title="GROUP BY & Aggregations",
        hook="GROUP BY collapses many rows into one per group, and aggregate functions decide what that one row summarizes.",
        explanation=(
            "`GROUP BY` groups rows sharing the same value in one or more columns, and aggregate functions "
            "(`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) compute one value per group. Every column in the `SELECT` list "
            "that isn't wrapped in an aggregate function must appear in `GROUP BY`, or the database won't know "
            "which of the many possible values to show for that group.\n\n"
            "`HAVING` filters groups after aggregation, while `WHERE` filters rows before aggregation — this is "
            "the single most common SQL interview question, because trying to filter on an aggregate in `WHERE` "
            "(`WHERE COUNT(*) > 5`) simply doesn't work; the aggregate doesn't exist yet at that stage of query "
            "execution."
        ),
        code=dict(
            lang="sql",
            label="WHERE before aggregation, HAVING after",
            src=(
                "SELECT department, COUNT(*) AS headcount, AVG(salary) AS avg_salary\n"
                "FROM employees\n"
                "WHERE hire_date >= '2020-01-01'      -- filters rows first\n"
                "GROUP BY department\n"
                "HAVING COUNT(*) > 5                    -- filters groups after aggregation\n"
                "ORDER BY avg_salary DESC;"
            ),
        ),
        example=(
            "A revenue-by-region report that only wants regions with more than 10 orders needs HAVING, not WHERE "
            "— the order count doesn't exist as a value until GROUP BY has already run."
        ),
        best_practices=[
            "Use WHERE to filter rows before grouping and HAVING to filter the resulting groups.",
            "Every non-aggregated column in SELECT must be in GROUP BY — most databases enforce this, some silently pick an arbitrary value.",
            "Alias aggregate expressions (`AS avg_salary`) so downstream code and ORDER BY can reference them cleanly.",
        ],
        pitfalls=[
            "Trying to filter on an aggregate using WHERE instead of HAVING.",
            "Selecting a non-aggregated, non-grouped column and getting an unpredictable value per group.",
        ],
        prompts=[
            "Give me three real business questions and the GROUP BY query that answers each.",
            "Why can't I use an aggregate function directly in WHERE?",
            "How do COUNT(*) and COUNT(column_name) differ when NULLs are involved?",
        ],
    ),
    dict(
        id="subqueries-ctes",
        title="Subqueries & CTEs",
        hook="A CTE is a subquery you name and reuse, which turns a tangled nested query into something you can actually read top to bottom.",
        explanation=(
            "A subquery is a query nested inside another — in the `WHERE` clause (`WHERE id IN (SELECT ...)`), in "
            "`FROM` (a derived table), or in `SELECT` itself (a scalar subquery). They're powerful but get hard to "
            "read once nested two or three levels deep, especially when the same subquery logic gets repeated.\n\n"
            "A Common Table Expression (`WITH name AS (...)`) names a subquery once at the top of the statement "
            "and lets you reference it like a real table anywhere in the main query, including multiple times. "
            "CTEs can also be recursive (`WITH RECURSIVE`), which is the standard way to query hierarchical data "
            "like an org chart or a category tree in a single statement."
        ),
        code=dict(
            lang="sql",
            label="Replacing a nested subquery with a readable CTE",
            src=(
                "WITH high_value_customers AS (\n"
                "    SELECT customer_id, SUM(order_total) AS lifetime_value\n"
                "    FROM orders\n"
                "    GROUP BY customer_id\n"
                "    HAVING SUM(order_total) > 1000\n"
                ")\n"
                "SELECT c.customer_name, hvc.lifetime_value\n"
                "FROM customers c\n"
                "JOIN high_value_customers hvc ON hvc.customer_id = c.customer_id\n"
                "ORDER BY hvc.lifetime_value DESC;"
            ),
        ),
        example=(
            "A dashboard query that needs 'top customers' in three different places (a total, a chart, and a "
            "table) defines it once as a CTE instead of copy-pasting the same subquery three times with room for "
            "the copies to drift out of sync."
        ),
        best_practices=[
            "Prefer a CTE over a deeply nested subquery whenever the logic is reused or the nesting hurts readability.",
            "Name CTEs descriptively — `high_value_customers`, not `cte1`.",
            "Use `WITH RECURSIVE` for hierarchical data instead of application-side recursive queries.",
        ],
        pitfalls=[
            "Assuming a CTE is always materialized/cached by the database — in many engines it's just inlined each time it's referenced.",
            "Nesting subqueries three or four levels deep instead of naming intermediate steps as CTEs.",
        ],
        prompts=[
            "Show me a recursive CTE example for querying an org chart.",
            "When does a CTE actually improve query performance versus just readability?",
            "Rewrite this nested subquery as a CTE for me.",
        ],
    ),
    dict(
        id="window-functions",
        title="Window Functions",
        hook="Window functions compute an aggregate across a set of rows without collapsing them into one row per group, unlike GROUP BY.",
        explanation=(
            "`GROUP BY` reduces many rows to one per group. A window function (`... OVER (PARTITION BY ... ORDER "
            "BY ...)`) computes an aggregate 'window' around each row while keeping every original row intact — "
            "you get a running total, a rank, or a moving average right alongside the detail data.\n\n"
            "`RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()` are the most common window functions for 'top N per "
            "group' queries; `RANK()` leaves gaps after ties, `DENSE_RANK()` doesn't, and `ROW_NUMBER()` gives a "
            "unique number even for exact ties. `SUM() OVER (PARTITION BY ... ORDER BY ...)` is how you compute a "
            "running total without a self-join or a correlated subquery."
        ),
        code=dict(
            lang="sql",
            label="Ranking and a running total, both without collapsing rows",
            src=(
                "SELECT\n"
                "    employee_name,\n"
                "    department,\n"
                "    salary,\n"
                "    RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank,\n"
                "    SUM(salary) OVER (ORDER BY hire_date) AS running_payroll_total\n"
                "FROM employees;"
            ),
        ),
        example=(
            "A 'top 3 highest-paid employee per department' report is a single window-function query where the "
            "equivalent using only GROUP BY and self-joins would need a much more convoluted, slower query."
        ),
        best_practices=[
            "Reach for a window function instead of a correlated subquery whenever you need per-row context alongside an aggregate.",
            "Use `ROW_NUMBER()` specifically when you need exactly one row per group (like deduplication).",
            "Combine `PARTITION BY` with `ORDER BY` deliberately — omitting `ORDER BY` changes the window's meaning for running totals.",
        ],
        pitfalls=[
            "Confusing RANK() (leaves gaps after ties) with DENSE_RANK() (no gaps) and getting unexpected numbering.",
            "Forgetting that window functions run after WHERE/GROUP BY/HAVING but before the final ORDER BY.",
        ],
        prompts=[
            "Show me a 'top 3 per group' query using window functions.",
            "What's the exact difference between RANK, DENSE_RANK, and ROW_NUMBER?",
            "How do I compute a 7-day moving average with a window function?",
        ],
    ),
    dict(
        id="indexing-optimization",
        title="Indexing & Query Optimization",
        hook="An index turns 'scan every row' into 'jump straight to the answer' — at the cost of extra storage and slower writes.",
        explanation=(
            "Without an index, the database performs a full table scan to satisfy a `WHERE` filter — checking "
            "every row. An index on the filtered column (typically a B-tree) lets the database jump directly to "
            "matching rows, similar to using a book's index instead of reading every page. The trade-off: every "
            "`INSERT`/`UPDATE`/`DELETE` also has to update the index, so indexing every column isn't free.\n\n"
            "`EXPLAIN` (or `EXPLAIN ANALYZE`) shows the actual query plan the database chose — whether it used an "
            "index, did a full scan, or picked a join strategy you didn't expect. Composite indexes (multiple "
            "columns) only help if the query's filter matches the index's column order from the left, which is a "
            "frequent source of 'I have an index but it's not being used' confusion."
        ),
        code=dict(
            lang="sql",
            label="Creating an index and checking the plan",
            src=(
                "CREATE INDEX idx_orders_customer_status\n"
                "    ON orders (customer_id, status);\n\n"
                "EXPLAIN ANALYZE\n"
                "SELECT * FROM orders\n"
                "WHERE customer_id = 4821 AND status = 'pending';\n"
                "-- Look for 'Index Scan' vs 'Seq Scan' in the output —\n"
                "-- Seq Scan on a large table is the signal something needs an index."
            ),
        ),
        example=(
            "A `users` table with a million rows and no index on `email` turns a login query into a full table "
            "scan on every single login attempt — adding one index on `email` is often the single highest-leverage "
            "performance fix available on a struggling app."
        ),
        best_practices=[
            "Index columns used frequently in WHERE, JOIN, and ORDER BY clauses — not every column.",
            "Run EXPLAIN ANALYZE before and after adding an index to confirm it's actually being used.",
            "Put the most selective column first in a composite index for the most common query pattern.",
        ],
        pitfalls=[
            "Adding indexes speculatively without checking EXPLAIN, which can slow down writes for no read benefit.",
            "Expecting a composite index to help a query that filters only on its second column, skipping the first.",
        ],
        prompts=[
            "Walk me through reading an EXPLAIN ANALYZE output line by line.",
            "When does adding an index actually hurt performance?",
            "How do composite index column order rules work in practice?",
        ],
    ),
]
