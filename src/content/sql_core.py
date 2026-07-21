"""SQL subtopics — enriched schema: deep_dive, advanced_code, glossary, faq, quiz added to every lesson."""

SUBTOPICS = [
    dict(
        id="select-where",
        title="SELECT & WHERE: The Foundation",
        hook="Every SQL query, however complex, is fundamentally answering the same question — 'which columns, from which rows' — and SELECT/WHERE is where that question gets asked.",
        explanation=(
            "`SELECT column1, column2 FROM table WHERE condition;` is the skeleton of nearly every SQL query: "
            "`SELECT` chooses which columns to return, `FROM` names the table, and `WHERE` filters which rows "
            "qualify. `SELECT *` returns every column, convenient for exploration but discouraged in "
            "production code since it breaks silently if the table's columns change and transfers more data "
            "than necessary.\n\n"
            "`WHERE` supports comparison operators (`=`, `!=`, `<`, `>`, `<=`, `>=`), logical combinators "
            "(`AND`, `OR`, `NOT`), pattern matching (`LIKE '%pattern%'`), set membership (`IN (1, 2, 3)`), "
            "range checks (`BETWEEN 10 AND 20`), and null checks (`IS NULL`, `IS NOT NULL` — critically, `= "
            "NULL` never matches anything, since NULL represents 'unknown' and nothing is considered equal to "
            "an unknown value, not even another NULL).\n\n"
            "`ORDER BY column [ASC|DESC]` sorts the result set (ascending by default), and `LIMIT n` (or "
            "`TOP n` in SQL Server, `FETCH FIRST n ROWS ONLY` in the ANSI standard) restricts how many rows "
            "come back — commonly paired for 'top N' queries like the 10 most recent orders.\n\n"
            "Column and table aliases (`SELECT price AS unit_price FROM products AS p`) rename results for "
            "readability or to resolve naming conflicts when a query involves multiple tables with "
            "overlapping column names, which becomes essential once joins enter the picture."
        ),
        deep_dive=(
            "SQL has a logical order of execution that's different from the order you type the clauses: "
            "roughly `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `LIMIT`. This is why "
            "you can't reference a column alias defined in `SELECT` inside the same query's `WHERE` clause — "
            "`WHERE` is evaluated before `SELECT` even runs, so that alias doesn't exist yet at that point in "
            "execution.\n\n"
            "`DISTINCT` removes duplicate rows from the result set, applied after the columns are selected — "
            "`SELECT DISTINCT city FROM customers` returns each unique city once, but `DISTINCT` considers the "
            "combination of *all* selected columns, so `SELECT DISTINCT city, country` only removes rows where "
            "both fields match another row exactly.\n\n"
            "Comparisons and pattern matching can be case-sensitive or not depending on the database's "
            "configured collation — PostgreSQL is case-sensitive by default for `=` and `LIKE` (needing "
            "`ILIKE` for case-insensitive matching), while MySQL's default collation is often case-insensitive "
            "— a frequent source of behavior that looks identical in development and differs in production "
            "depending on which database and collation is actually configured."
        ),
        code=dict(
            lang="sql",
            label="SELECT with filtering, sorting, and limiting",
            src=(
                "SELECT customer_name, order_date, total\n"
                "FROM orders\n"
                "WHERE total > 100\n"
                "  AND order_date >= '2026-01-01'\n"
                "  AND status IN ('shipped', 'delivered')\n"
                "ORDER BY order_date DESC\n"
                "LIMIT 10;"
            ),
        ),
        advanced_code=dict(
            lang="sql",
            label="Pattern matching, NULL handling, and aliases",
            src=(
                "SELECT\n"
                "    c.name AS customer_name,\n"
                "    c.email\n"
                "FROM customers AS c\n"
                "WHERE c.email LIKE '%@company.com'\n"
                "  AND c.phone IS NOT NULL          -- never use = NULL, it matches nothing\n"
                "  AND c.status NOT IN ('banned', 'deleted');"
            ),
        ),
        example=(
            "A support dashboard showing 'unresolved tickets from paying customers created this month' is a "
            "single WHERE clause combining a status filter, a join-derived customer tier condition, and a date "
            "range — the entire business question expressed declaratively, letting the database figure out "
            "the most efficient way to actually find those rows."
        ),
        best_practices=[
            "Select only the columns you actually need instead of `SELECT *`, especially in application code and views.",
            "Always use `IS NULL` / `IS NOT NULL` for null checks, never `= NULL` or `!= NULL`.",
            "Use table aliases once a query touches more than one table, for both brevity and clarity about which table a column comes from.",
            "Add `LIMIT` to exploratory queries against large tables to avoid accidentally pulling millions of rows while poking around.",
        ],
        pitfalls=[
            "Writing `WHERE status = NULL` expecting it to match null rows — it always evaluates to unknown/false, silently returning zero rows.",
            "Referencing a `SELECT`-defined alias inside the same query's `WHERE` clause, which fails because `WHERE` executes before `SELECT` logically.",
            "Assuming string comparisons are case-insensitive (or case-sensitive) without checking the specific database and collation actually in use.",
        ],
        glossary=[
            dict(term="Predicate", definition="A condition in a WHERE (or HAVING/JOIN ON) clause that evaluates to true, false, or unknown for each row."),
            dict(term="NULL", definition="SQL's representation of an unknown or missing value; comparisons involving NULL with = or != always evaluate to unknown, not true or false."),
            dict(term="Collation", definition="The rules a database uses for comparing and sorting text, including case sensitivity — configurable per database, table, or column."),
            dict(term="Logical query processing order", definition="The order SQL clauses are conceptually evaluated in (FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY), which differs from the order they're written."),
        ],
        faq=[
            dict(q="Why can't I use a column alias from SELECT inside my WHERE clause?", a="SQL's logical execution order evaluates WHERE before SELECT, so any alias defined in SELECT doesn't exist yet when WHERE runs. You'd need to repeat the underlying expression in WHERE, or use a subquery/CTE that already has the alias applied."),
            dict(q="Why did WHERE email = NULL return zero rows even though some emails are null?", a="NULL represents 'unknown', and SQL's three-valued logic means any comparison with NULL (including = NULL) evaluates to unknown, which is treated as false for filtering purposes. Use IS NULL instead."),
            dict(q="Is SQL case-sensitive?", a="It depends entirely on the specific database and its configured collation. PostgreSQL's default is case-sensitive for string comparisons (use ILIKE for case-insensitive matching); many MySQL default collations are case-insensitive. Always check your specific setup."),
        ],
        quiz=[
            dict(
                question="What does `WHERE phone = NULL` return?",
                options=["Rows where phone is null", "Rows where phone is not null", "Always zero rows, regardless of data", "A syntax error"],
                correct=2,
                explanation="Comparing anything to NULL with = always evaluates to unknown (treated as false), so this condition never matches any row — IS NULL is required instead.",
            ),
        ],
        prompts=[
            "Why is SELECT * considered bad practice in production queries?",
            "Explain SQL's logical order of execution and why it matters for WHERE and SELECT aliases.",
            "Write a query to find the 5 most recent orders over $200 that aren't cancelled.",
            "What's the difference between LIKE and ILIKE, and when does it matter?",
        ],
    ),
    dict(
        id="joins",
        title="JOINs: Combining Tables",
        hook="Every JOIN answers the same fundamental question — 'for each row on one side, which rows on the other side match?' — and INNER vs LEFT vs RIGHT vs FULL is entirely about what happens when there's no match.",
        explanation=(
            "An `INNER JOIN` (often just written `JOIN`) returns only rows where the join condition matches on "
            "both tables — a customer with no orders simply doesn't appear in `customers INNER JOIN orders`. A "
            "`LEFT JOIN` (or `LEFT OUTER JOIN`) returns every row from the left table regardless of whether a "
            "match exists on the right, filling in `NULL` for the right table's columns when there's no match "
            "— essential for questions like 'which customers have never placed an order' (`WHERE orders.id IS "
            "NULL` after a LEFT JOIN).\n\n"
            "A `RIGHT JOIN` is the mirror of `LEFT JOIN` (keep every row from the right table), and is "
            "functionally interchangeable with rewriting the query with the tables swapped and a LEFT JOIN "
            "instead — most style guides prefer standardizing on LEFT JOIN for consistency rather than mixing "
            "both directions. A `FULL OUTER JOIN` keeps every row from both tables, matching where possible "
            "and filling NULLs on whichever side lacks a match.\n\n"
            "The join condition (`ON a.id = b.a_id`) determines which rows are considered a match — it doesn't "
            "have to be equality (`ON a.start_date <= b.event_date AND a.end_date >= b.event_date` is a valid "
            "range-based join), though equality joins on indexed columns are by far the most common and "
            "best-performing case.\n\n"
            "A `CROSS JOIN` produces the Cartesian product — every row from the first table paired with every "
            "row from the second, with no join condition at all — genuinely useful for generating combinations "
            "(every product paired with every size/color variant) but a common accidental performance disaster "
            "when a join condition is forgotten by mistake, silently multiplying row counts."
        ),
        deep_dive=(
            "A self-join joins a table to itself, used for hierarchical or comparative relationships within "
            "one table — finding each employee's manager (also stored in the employees table) requires "
            "`employees AS e JOIN employees AS mgr ON e.manager_id = mgr.id`, aliasing the same table twice "
            "to treat it as two logical roles in the query.\n\n"
            "Filtering on a LEFT JOIN's right-side table requires care about *where* the condition goes: "
            "putting a filter in the `ON` clause (`LEFT JOIN orders ON c.id = orders.customer_id AND orders."
            "status = 'shipped'`) still keeps every customer, just only matching shipped orders (or NULL if "
            "none). Putting the same filter in `WHERE` instead (`WHERE orders.status = 'shipped'`) silently "
            "converts the query back into an effective INNER JOIN, because any customer with no shipped order "
            "has NULL there, and NULL never satisfies a WHERE equality condition.\n\n"
            "Join performance depends heavily on indexes on the join columns — an unindexed join column forces "
            "the database to compare every row of one table against every row of the other (a nested loop over "
            "unindexed data, or a full table scan feeding a hash join), which becomes painfully slow as table "
            "sizes grow, while an indexed join column lets the database look up matches directly."
        ),
        code=dict(
            lang="sql",
            label="INNER JOIN vs. LEFT JOIN — the difference in what's kept",
            src=(
                "-- Only customers WITH at least one order\n"
                "SELECT c.name, o.order_date\n"
                "FROM customers c\n"
                "INNER JOIN orders o ON c.id = o.customer_id;\n\n"
                "-- ALL customers, orders columns NULL if they've never ordered\n"
                "SELECT c.name, o.order_date\n"
                "FROM customers c\n"
                "LEFT JOIN orders o ON c.id = o.customer_id;\n\n"
                "-- Customers who have NEVER placed an order\n"
                "SELECT c.name\n"
                "FROM customers c\n"
                "LEFT JOIN orders o ON c.id = o.customer_id\n"
                "WHERE o.id IS NULL;"
            ),
        ),
        advanced_code=dict(
            lang="sql",
            label="A self-join for hierarchical data",
            src=(
                "-- employees table has a manager_id column referencing another row in the same table\n"
                "SELECT\n"
                "    e.name AS employee,\n"
                "    mgr.name AS manager\n"
                "FROM employees e\n"
                "LEFT JOIN employees mgr ON e.manager_id = mgr.id\n"
                "ORDER BY mgr.name;\n\n"
                "-- LEFT JOIN so the CEO (manager_id IS NULL) still appears, with manager = NULL"
            ),
        ),
        example=(
            "An inventory report needs both 'products with sales this month' and 'products with zero sales this "
            "month' visible in one result — a LEFT JOIN from products to this month's sales, with `COALESCE"
            "(SUM(sale.amount), 0)` to show zero instead of NULL for products that didn't sell, answers both "
            "questions in a single query."
        ),
        best_practices=[
            "Default to LEFT JOIN over RIGHT JOIN for readability, rewriting the table order instead of mixing join directions in one query.",
            "Put right-table filtering conditions in the ON clause (not WHERE) when using a LEFT JOIN, to avoid silently turning it into an INNER JOIN.",
            "Ensure join columns are indexed, especially on the larger table, for acceptable performance as data grows.",
            "Use table aliases in every multi-table query for both brevity and to disambiguate columns with the same name across tables.",
        ],
        pitfalls=[
            "Filtering a LEFT JOIN's right-side table in WHERE instead of ON, silently converting it into an INNER JOIN and losing the 'unmatched' rows you specifically wanted to keep.",
            "Forgetting a join condition entirely, accidentally producing a CROSS JOIN that returns a row count equal to the product of both tables' row counts.",
            "Joining on an unindexed column in a large table, causing query performance to degrade sharply as the tables grow.",
        ],
        glossary=[
            dict(term="INNER JOIN", definition="Returns only rows with a match on both sides of the join condition."),
            dict(term="LEFT JOIN", definition="Returns every row from the left table, with NULLs filling in unmatched columns from the right table."),
            dict(term="Self-join", definition="A table joined to itself, typically via two aliases, used for hierarchical or comparative relationships within one table."),
            dict(term="Cartesian product", definition="Every possible pairing of rows from two tables, produced by a CROSS JOIN or an accidentally missing join condition."),
        ],
        faq=[
            dict(q="What's the practical difference between putting a condition in ON versus WHERE for a LEFT JOIN?", a="A condition in ON only affects which right-side rows count as a match, still keeping every left-side row (with NULLs if nothing matched). The same condition in WHERE is applied after the join, filtering out any row where that condition isn't true — which discards rows where the right side was NULL, effectively undoing the LEFT JOIN's purpose."),
            dict(q="Why would I ever use RIGHT JOIN instead of just swapping table order and using LEFT JOIN?", a="Functionally they're equivalent — RIGHT JOIN exists mainly for convenience when you don't want to reorder a query you're editing. Most style guides recommend standardizing on LEFT JOIN for consistency across a codebase."),
            dict(q="Why is my join returning way more rows than either table has?", a="This is the classic sign of an accidental Cartesian product — check that your ON condition is actually present and correctly matches a genuinely related column on both sides."),
        ],
        quiz=[
            dict(
                question="After a LEFT JOIN from customers to orders, which customers appear with NULL order columns?",
                options=["No customers, LEFT JOIN excludes unmatched rows", "Customers with no matching orders", "All customers, always", "Only customers with more than one order"],
                correct=1,
                explanation="LEFT JOIN keeps every row from the left (customers) table; if there's no matching order, the order-side columns come back as NULL.",
            ),
            dict(
                question="Where should a filter on the right table go to avoid turning a LEFT JOIN into an INNER JOIN?",
                options=["In the WHERE clause", "In the ON clause", "It doesn't matter", "In a separate subquery only"],
                correct=1,
                explanation="Putting the filter in ON keeps it part of the join's matching logic, preserving unmatched left rows with NULLs; putting it in WHERE discards those NULL rows entirely.",
            ),
        ],
        prompts=[
            "Write a query to find customers who have never placed an order.",
            "Explain why my LEFT JOIN is behaving like an INNER JOIN.",
            "Show me a self-join example for an employee/manager hierarchy.",
            "Why did my join return far more rows than I expected?",
        ],
    ),
    dict(
        id="group-by-aggregations",
        title="GROUP BY & Aggregate Functions",
        hook="GROUP BY collapses many rows into one summary row per group — and every column you SELECT alongside it either has to be part of that grouping or wrapped in an aggregate function, no exceptions.",
        explanation=(
            "Aggregate functions — `COUNT()`, `SUM()`, `AVG()`, `MIN()`, `MAX()` — compute a single value "
            "from a set of rows. Used alone, `SELECT COUNT(*) FROM orders` summarizes the whole table into one "
            "row. Combined with `GROUP BY`, `SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id` "
            "computes that count separately for each distinct value of `customer_id`, producing one summary "
            "row per group.\n\n"
            "Every column in the `SELECT` list of a grouped query must either appear in the `GROUP BY` clause "
            "or be wrapped in an aggregate function — SQL has no way to know which single value to show for a "
            "non-aggregated, non-grouped column when multiple rows are being collapsed into one, so most "
            "databases reject the query outright rather than guessing.\n\n"
            "`HAVING` filters *after* grouping and aggregation, the way `WHERE` filters *before* — `HAVING "
            "COUNT(*) > 5` keeps only groups with more than 5 rows, which `WHERE` can't express since "
            "`COUNT(*)` doesn't exist yet at the point `WHERE` is logically evaluated. This is the single most "
            "common reason for a 'why can't I filter on this aggregate in WHERE' confusion.\n\n"
            "`COUNT(*)` counts all rows including nulls; `COUNT(column_name)` counts only rows where that "
            "specific column is non-null — a subtle but important difference when a table has optional fields, "
            "since `COUNT(*)` and `COUNT(some_nullable_column)` can return genuinely different numbers on the "
            "same table."
        ),
        deep_dive=(
            "`COUNT(DISTINCT column)` counts unique non-null values rather than every row — useful for "
            "questions like 'how many distinct customers placed an order this month' as opposed to 'how many "
            "orders were placed this month,' which are meaningfully different numbers if customers order more "
            "than once.\n\n"
            "Grouping by multiple columns (`GROUP BY region, product_category`) produces one row per unique "
            "combination of those columns — the equivalent of a multi-level breakdown, like a pivot table's "
            "row grouping. `GROUPING SETS`, `ROLLUP`, and `CUBE` (supported by most major databases) extend "
            "this to compute multiple levels of subtotals and a grand total in a single query, instead of "
            "running several separate GROUP BY queries and combining the results manually.\n\n"
            "`NULL` values form their own group when grouping — rows with a NULL in the grouped column don't "
            "get dropped, they're collected into a single group represented as NULL in the output, which is "
            "occasionally surprising if you expected NULLs to be excluded entirely from a grouped summary."
        ),
        code=dict(
            lang="sql",
            label="GROUP BY with HAVING to filter aggregated results",
            src=(
                "SELECT\n"
                "    customer_id,\n"
                "    COUNT(*) AS order_count,\n"
                "    SUM(total) AS lifetime_value\n"
                "FROM orders\n"
                "GROUP BY customer_id\n"
                "HAVING COUNT(*) >= 3          -- filters on the aggregate, WHERE can't do this\n"
                "ORDER BY lifetime_value DESC;"
            ),
        ),
        advanced_code=dict(
            lang="sql",
            label="Multi-column grouping and COUNT(DISTINCT ...)",
            src=(
                "SELECT\n"
                "    region,\n"
                "    product_category,\n"
                "    COUNT(DISTINCT customer_id) AS unique_customers,\n"
                "    SUM(total) AS revenue\n"
                "FROM orders\n"
                "GROUP BY region, product_category\n"
                "ORDER BY region, revenue DESC;"
            ),
        ),
        example=(
            "A monthly business report needs 'total revenue and unique customer count, per region, for "
            "regions generating over $10,000' — GROUP BY region with SUM and COUNT(DISTINCT customer_id), "
            "filtered by HAVING SUM(total) > 10000, answers the entire question in one query."
        ),
        best_practices=[
            "Use HAVING for conditions on aggregate results, and WHERE for conditions on individual rows before grouping — putting an aggregate condition in WHERE is a syntax error.",
            "Be explicit about COUNT(*) versus COUNT(specific_column) when the column can contain NULLs — they can return different numbers.",
            "Use COUNT(DISTINCT column) when you need unique value counts, not just row counts.",
            "Filter with WHERE before grouping whenever possible — it's more efficient than grouping everything first and filtering with HAVING afterward.",
        ],
        pitfalls=[
            "Selecting a non-aggregated, non-grouped column alongside GROUP BY, which most databases reject with an error (though some, like older MySQL configurations, silently pick an arbitrary value — best avoided entirely).",
            "Trying to filter an aggregate with WHERE instead of HAVING, hitting an error because the aggregate value doesn't exist yet at WHERE's point in logical execution.",
            "Confusing COUNT(*) and COUNT(column) on a table with nullable columns, leading to a subtly wrong count.",
        ],
        glossary=[
            dict(term="Aggregate function", definition="A function (COUNT, SUM, AVG, MIN, MAX) that computes a single summary value from a set of rows."),
            dict(term="GROUP BY", definition="Collapses rows sharing the same value(s) in specified columns into one summary row per group."),
            dict(term="HAVING", definition="Filters grouped results based on an aggregate condition, evaluated after GROUP BY, unlike WHERE which is evaluated before."),
            dict(term="COUNT(DISTINCT ...)", definition="Counts unique non-null values in a column, rather than every row."),
        ],
        faq=[
            dict(q="Why can't I put COUNT(*) > 5 in my WHERE clause?", a="WHERE is evaluated before grouping and aggregation happen (per SQL's logical execution order), so the aggregate value doesn't exist yet at that point. HAVING is specifically designed to filter after aggregation completes."),
            dict(q="Why did my query error out when I selected a column that wasn't in GROUP BY or an aggregate?", a="SQL has no defined way to pick a single value for that column when multiple rows are being collapsed into one group — most databases reject this ambiguity outright rather than silently picking an arbitrary row's value."),
            dict(q="What's the difference between COUNT(*) and COUNT(column_name)?", a="COUNT(*) counts every row in the group regardless of NULLs. COUNT(column_name) counts only rows where that specific column is non-null — the two can differ meaningfully on tables with optional fields."),
        ],
        quiz=[
            dict(
                question="What's wrong with `SELECT customer_id, order_date, COUNT(*) FROM orders GROUP BY customer_id`?",
                options=["Nothing, it's valid", "order_date is neither grouped nor aggregated, which most databases reject", "COUNT(*) can't be used with GROUP BY", "GROUP BY requires ORDER BY"],
                correct=1,
                explanation="order_date isn't in the GROUP BY clause and isn't wrapped in an aggregate, so SQL has no defined single value to show for it per group.",
            ),
            dict(
                question="When should you use HAVING instead of WHERE?",
                options=["Always, HAVING is the modern replacement for WHERE", "When filtering on an aggregate function's result", "Never, HAVING is deprecated", "Only with COUNT(*), not other aggregates"],
                correct=1,
                explanation="HAVING filters after grouping/aggregation, making it the correct (and only) place to filter based on an aggregate value like SUM or COUNT.",
            ),
        ],
        prompts=[
            "Write a query showing total revenue per region, only for regions over $50,000.",
            "Why does my query error when I select a column not in GROUP BY?",
            "Explain the difference between COUNT(*) and COUNT(DISTINCT customer_id).",
            "When should I filter with WHERE versus HAVING?",
        ],
    ),
    dict(
        id="subqueries-ctes",
        title="Subqueries & CTEs (WITH clause)",
        hook="A Common Table Expression is functionally just a named subquery — but naming it turns a deeply nested, hard-to-read query into a sequence of clearly labeled steps.",
        explanation=(
            "A subquery is a query nested inside another query, usable nearly anywhere a table or value is "
            "expected: in the `WHERE` clause (`WHERE customer_id IN (SELECT id FROM vip_customers)`), in the "
            "`FROM` clause (treating the subquery's result as a temporary table), or even in the `SELECT` list "
            "as a single computed value per row (a scalar subquery).\n\n"
            "A CTE (Common Table Expression), written with `WITH name AS (query), ...`, defines one or more "
            "named, temporary result sets that the main query can reference by name, as if they were real "
            "tables. This is functionally similar to a subquery in `FROM`, but reads top-to-bottom instead of "
            "nested inside-out, and a single CTE can be referenced multiple times in the main query without "
            "repeating its definition.\n\n"
            "A correlated subquery references a column from the outer query inside its own `WHERE` clause, "
            "meaning it has to be re-evaluated once per outer row rather than once total — `SELECT * FROM "
            "orders o WHERE total > (SELECT AVG(total) FROM orders WHERE customer_id = o.customer_id)` "
            "recomputes each customer's average fresh for every order row, which is powerful but can be "
            "considerably slower than an equivalent window function or join-based rewrite for large tables.\n\n"
            "Recursive CTEs (`WITH RECURSIVE`) let a CTE reference itself, which is how SQL expresses "
            "genuinely hierarchical or graph-like queries — walking an org chart from an employee up to the "
            "CEO, or finding all descendant categories of a product category — that a plain join can't express "
            "for an unknown, variable depth."
        ),
        deep_dive=(
            "Most modern query optimizers treat non-recursive CTEs as inlined into the main query for planning "
            "purposes (similar to a subquery), rather than as a materialized, separately-computed temporary "
            "table — this varies by database and version, so 'CTEs are always faster/slower than subqueries' "
            "is not a safe generalization; the two are frequently equivalent in actual execution plan, and the "
            "real benefit of CTEs is readability, not guaranteed performance.\n\n"
            "A recursive CTE has two parts unioned together: an anchor member (the starting point, like 'the "
            "CEO, who has no manager') and a recursive member that references the CTE's own name, joined back "
            "to the base table to find the next level, repeating until no more rows are produced. Nearly every "
            "database enforces some form of recursion limit or requires the recursive term to eventually "
            "terminate, to prevent an infinite loop from a cyclical data error.\n\n"
            "`EXISTS` and correlated subqueries are frequently interchangeable with joins, and for many query "
            "planners `EXISTS` (which can stop as soon as it finds one matching row) outperforms an equivalent "
            "`IN (SELECT ...)` subquery, especially when the subquery could return a very large result set."
        ),
        code=dict(
            lang="sql",
            label="A CTE simplifying a multi-step calculation",
            src=(
                "WITH monthly_totals AS (\n"
                "    SELECT customer_id, DATE_TRUNC('month', order_date) AS month, SUM(total) AS total\n"
                "    FROM orders\n"
                "    GROUP BY customer_id, DATE_TRUNC('month', order_date)\n"
                "),\n"
                "high_spenders AS (\n"
                "    SELECT customer_id\n"
                "    FROM monthly_totals\n"
                "    WHERE total > 1000\n"
                ")\n"
                "SELECT c.name\n"
                "FROM customers c\n"
                "WHERE c.id IN (SELECT customer_id FROM high_spenders);"
            ),
        ),
        advanced_code=dict(
            lang="sql",
            label="A recursive CTE walking an org chart",
            src=(
                "WITH RECURSIVE org_chart AS (\n"
                "    -- Anchor: the top of the hierarchy\n"
                "    SELECT id, name, manager_id, 1 AS depth\n"
                "    FROM employees\n"
                "    WHERE manager_id IS NULL\n\n"
                "    UNION ALL\n\n"
                "    -- Recursive: find the next level down each time\n"
                "    SELECT e.id, e.name, e.manager_id, oc.depth + 1\n"
                "    FROM employees e\n"
                "    JOIN org_chart oc ON e.manager_id = oc.id\n"
                ")\n"
                "SELECT * FROM org_chart ORDER BY depth, name;"
            ),
        ),
        example=(
            "A finance report calculating 'this month's revenue as a percentage of the trailing 12-month "
            "average' breaks naturally into two CTEs — one computing monthly totals, one computing the "
            "trailing average from those totals — turning what would be a deeply nested subquery into two "
            "clearly labeled, readable steps."
        ),
        best_practices=[
            "Use CTEs to break a complex query into named, readable steps instead of deeply nesting subqueries inside each other.",
            "Prefer EXISTS over IN (subquery) when you only need to check for the presence of at least one matching row, especially against a potentially large subquery result.",
            "Ensure a recursive CTE's recursive term will actually terminate — verify the underlying data has no cycles, or add an explicit depth limit as a safety net.",
            "Don't assume a CTE is automatically faster than an equivalent subquery — check the actual execution plan on your specific database if performance matters.",
        ],
        pitfalls=[
            "Writing a correlated subquery inside a large SELECT list that re-executes once per outer row, causing severe performance problems on large tables where a window function or join would be far cheaper.",
            "Assuming CTEs are always materialized as a separate temporary table — behavior varies by database and can affect performance in ways that surprise people coming from a database with different optimizer behavior.",
            "Writing a recursive CTE on data with an undetected cycle, causing infinite (or database-limit-capped) recursion.",
        ],
        glossary=[
            dict(term="Subquery", definition="A query nested inside another query, usable in WHERE, FROM, or the SELECT list."),
            dict(term="CTE (Common Table Expression)", definition="A named, temporary result set defined with WITH, referenceable by name in the main query."),
            dict(term="Correlated subquery", definition="A subquery that references a column from the outer query, requiring re-evaluation once per outer row."),
            dict(term="Recursive CTE", definition="A CTE that references itself, used for hierarchical or graph-like queries of unknown depth."),
        ],
        faq=[
            dict(q="Are CTEs always faster than subqueries?", a="Not necessarily — many databases treat a non-recursive CTE similarly to an inlined subquery for query planning purposes. The main, reliable benefit of CTEs is readability, not a guaranteed performance advantage; check your specific database's execution plan if performance matters."),
            dict(q="What's the difference between IN (subquery) and EXISTS?", a="IN checks whether a value appears anywhere in the subquery's full result set. EXISTS just checks whether the subquery returns at least one row, and can often stop early once it finds a match — frequently faster for large subquery results, though modern optimizers sometimes produce equivalent plans for both."),
            dict(q="Why does my recursive CTE never finish?", a="Almost always a cycle in the underlying data (e.g., employee A reports to B, who reports back to A), or a missing/incorrect anchor condition. Add a depth limit as a safety net while debugging the actual data issue."),
        ],
        quiz=[
            dict(
                question="What does a recursive CTE need to avoid running forever?",
                options=["An ORDER BY clause", "A properly terminating recursive term and non-cyclical data", "A HAVING clause", "It's not possible to avoid, recursive CTEs always need a manual stop"],
                correct=1,
                explanation="A recursive CTE stops naturally when the recursive term produces no new rows; a cycle in the underlying data or an incorrect anchor can prevent that from ever happening.",
            ),
        ],
        prompts=[
            "Rewrite this deeply nested subquery as a readable CTE.",
            "Write a recursive CTE to find all subcategories under a given product category.",
            "When should I use EXISTS instead of IN with a subquery?",
            "Why is my correlated subquery so slow on a large table?",
        ],
    ),
    dict(
        id="window-functions",
        title="Window Functions",
        hook="A window function is the answer to 'I need a per-row calculation that looks at other rows too, without collapsing the result down to one row per group' — GROUP BY can't do that, window functions can.",
        explanation=(
            "A window function computes a value across a set of rows related to the current row (its "
            "'window'), without collapsing those rows into a single output row the way GROUP BY does — you "
            "still get one output row per input row, each with an added calculated column. The syntax is "
            "`function() OVER (PARTITION BY column ORDER BY column)`: `PARTITION BY` defines the window (like "
            "GROUP BY, but non-collapsing), and `ORDER BY` (optional, needed for ranking and running "
            "calculations) defines the order within each partition.\n\n"
            "`ROW_NUMBER()` assigns a unique sequential number within each partition; `RANK()` assigns the "
            "same rank to ties but leaves gaps afterward (1, 2, 2, 4); `DENSE_RANK()` assigns the same rank to "
            "ties without gaps (1, 2, 2, 3). Choosing between them depends on whether you want strictly unique "
            "positions, or want ties to genuinely share the same rank.\n\n"
            "Aggregate functions (`SUM`, `AVG`, `COUNT`) work as window functions too when given an `OVER` "
            "clause — `SUM(amount) OVER (PARTITION BY customer_id)` shows each order alongside that "
            "customer's total across all their orders, on every row, without needing a separate query or a "
            "self-join.\n\n"
            "`LAG(column, n)` and `LEAD(column, n)` access a value from a previous or following row within the "
            "same partition/order — directly answering 'what was the previous month's value' or 'what's the "
            "next event' without a self-join, which is exactly the kind of row-to-row comparison window "
            "functions were designed to make simple."
        ),
        deep_dive=(
            "The frame clause (`ROWS BETWEEN ... AND ...` or `RANGE BETWEEN ... AND ...`) further refines "
            "exactly which rows within a partition contribute to the calculation for the current row — "
            "`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` computes a rolling 3-row window (the current row plus "
            "the two before it), which is how running totals and moving averages are expressed. Without an "
            "explicit frame clause, most databases default to `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT "
            "ROW` when `ORDER BY` is present in the window, which is effectively a running total from the "
            "start of the partition.\n\n"
            "Window functions execute logically after `WHERE`, `GROUP BY`, and `HAVING`, but before the final "
            "`ORDER BY` of the outer query — this is why you can't directly reference a window function's "
            "result in the same query's `WHERE` clause (the same restriction as aggregate functions and "
            "`HAVING`); filtering on a window function's result requires wrapping the query in a CTE or "
            "subquery and filtering in the outer layer.\n\n"
            "Multiple window functions in the same query can share an identical `OVER` specification, which "
            "many databases let you name once with a `WINDOW` clause and reuse, avoiding repeating the same "
            "`PARTITION BY`/`ORDER BY` across several columns."
        ),
        code=dict(
            lang="sql",
            label="Ranking and running totals with window functions",
            src=(
                "SELECT\n"
                "    customer_id,\n"
                "    order_date,\n"
                "    total,\n"
                "    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_sequence,\n"
                "    SUM(total) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total\n"
                "FROM orders\n"
                "ORDER BY customer_id, order_date;"
            ),
        ),
        advanced_code=dict(
            lang="sql",
            label="LAG for month-over-month comparison, and a rolling average",
            src=(
                "SELECT\n"
                "    month,\n"
                "    revenue,\n"
                "    LAG(revenue) OVER (ORDER BY month) AS prev_month_revenue,\n"
                "    revenue - LAG(revenue) OVER (ORDER BY month) AS change,\n"
                "    AVG(revenue) OVER (\n"
                "        ORDER BY month\n"
                "        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW\n"
                "    ) AS rolling_3mo_avg\n"
                "FROM monthly_revenue\n"
                "ORDER BY month;"
            ),
        ),
        example=(
            "A sales leaderboard showing each rep's rank within their region, alongside their percentage of "
            "the region's total, uses `RANK() OVER (PARTITION BY region ORDER BY sales DESC)` and `sales / "
            "SUM(sales) OVER (PARTITION BY region)` side by side on the same per-rep rows — no GROUP BY, no "
            "collapsing, no self-join required."
        ),
        best_practices=[
            "Reach for a window function whenever you need a per-row calculation that also depends on other related rows — before writing a correlated subquery or self-join for the same job.",
            "Choose ROW_NUMBER, RANK, or DENSE_RANK deliberately based on whether ties should get unique, gapped, or ungapped positions.",
            "Use an explicit frame clause (ROWS BETWEEN ...) whenever you need a bounded window like a rolling average, rather than relying on the (varying) default frame.",
            "Filter on a window function's result by wrapping the query in a CTE or subquery, since WHERE can't reference it directly in the same query.",
        ],
        pitfalls=[
            "Trying to filter directly on a window function's result in the same query's WHERE clause, hitting the same restriction that applies to aggregate functions.",
            "Forgetting PARTITION BY entirely, causing the window function to operate across the whole result set instead of per group.",
            "Assuming the default window frame is always a full running total — it depends on whether ORDER BY is present in the OVER clause and varies slightly by database.",
        ],
        glossary=[
            dict(term="Window function", definition="A function computing a value across a set of related rows without collapsing them into one output row, using an OVER clause."),
            dict(term="PARTITION BY", definition="Divides rows into groups for a window function, analogous to GROUP BY but without collapsing rows."),
            dict(term="Frame clause", definition="Specifies exactly which rows within a partition (e.g. ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) contribute to the window calculation for the current row."),
            dict(term="LAG / LEAD", definition="Window functions that access a value from a previous (LAG) or following (LEAD) row within the same partition/order."),
        ],
        faq=[
            dict(q="What's the real difference between GROUP BY and a window function?", a="GROUP BY collapses multiple rows into one summary row per group. A window function keeps every original row and adds a calculated column computed across a related set of rows — you get both the detail and the aggregate together."),
            dict(q="Why can't I filter on ROW_NUMBER() directly in WHERE?", a="Like other window functions, ROW_NUMBER() is computed after WHERE in SQL's logical execution order, so it doesn't exist yet at that point. Wrap the query in a CTE or subquery and filter in the outer query instead."),
            dict(q="What's the difference between RANK and DENSE_RANK for tied values?", a="RANK leaves a gap after ties (1, 2, 2, 4), reflecting that two rows tied for 2nd means the next distinct rank is 4th overall. DENSE_RANK doesn't leave gaps (1, 2, 2, 3), treating the next rank as simply the next distinct value."),
        ],
        quiz=[
            dict(
                question="Why can't you put ROW_NUMBER() OVER (...) = 1 directly in a WHERE clause?",
                options=["ROW_NUMBER() doesn't exist in SQL", "Window functions are evaluated after WHERE in logical execution order", "It's a performance issue, not a logical one", "You actually can, this works fine"],
                correct=1,
                explanation="Window functions are computed after WHERE, GROUP BY, and HAVING but before the final ORDER BY — filtering on their result requires an outer query or CTE wrapping the window function.",
            ),
        ],
        prompts=[
            "Write a query showing each employee's salary rank within their department.",
            "Show me how to calculate a 7-day rolling average with a window function.",
            "Why can't I filter directly on a window function's output in WHERE?",
            "Explain the difference between ROW_NUMBER, RANK, and DENSE_RANK with an example.",
        ],
    ),
    dict(
        id="indexing-and-query-optimization",
        title="Indexing & Query Optimization",
        hook="An index trades write speed and storage space for read speed — understanding that trade-off is the difference between indexing thoughtfully and indexing everything (which usually makes things worse).",
        explanation=(
            "An index is a separate data structure (usually a B-tree) that lets the database find rows "
            "matching a condition without scanning the entire table — similar to a book's index letting you "
            "jump directly to a page instead of reading cover to cover. `CREATE INDEX idx_orders_customer ON "
            "orders(customer_id);` speeds up any query filtering or joining on `customer_id`, at the cost of "
            "extra storage and slightly slower writes (every INSERT/UPDATE/DELETE also has to update the "
            "index).\n\n"
            "A composite (multi-column) index — `CREATE INDEX idx ON orders(customer_id, order_date);` — "
            "speeds up queries filtering on `customer_id` alone, or on `customer_id` AND `order_date` "
            "together, but generally does *not* help a query filtering on `order_date` alone, because of how "
            "B-tree indexes are structured: leftmost columns of a composite index must be involved for the "
            "index to be usable, similar to how a phone book sorted by (last name, first name) doesn't help "
            "you look someone up by first name alone.\n\n"
            "`EXPLAIN` (or `EXPLAIN ANALYZE` for actual execution statistics, not just the plan) shows exactly "
            "how the database intends to execute a query — whether it's using an index or falling back to a "
            "full table scan, in what order tables are joined, and where the estimated cost is concentrated. "
            "Reading an execution plan is the single most reliable way to understand why a specific query is "
            "slow, rather than guessing.\n\n"
            "Indexes help reads but cost writes — a table with ten indexes pays the write cost of updating all "
            "ten on every insert, which is why indexing every column 'just in case' is a common and genuinely "
            "harmful anti-pattern on write-heavy tables."
        ),
        deep_dive=(
            "A B-tree index stores values in sorted order, which is why it accelerates equality lookups "
            "(`WHERE customer_id = 5`), range queries (`WHERE order_date BETWEEN ... AND ...`), and sorting "
            "(`ORDER BY indexed_column`) — but generally can't help a condition wrapped in a function call "
            "(`WHERE UPPER(email) = 'X'`) unless a functional index specifically matching that expression "
            "exists, since the stored sorted values are of the raw column, not the transformed result.\n\n"
            "A covering index includes every column a query needs (in the index itself, not just the columns "
            "used to filter), letting the database satisfy the entire query from the index alone without ever "
            "touching the underlying table rows — a meaningful performance win for queries that run "
            "frequently and only need a small, predictable set of columns.\n\n"
            "Query optimizers use table statistics (row counts, value distributions) to decide whether using "
            "an index is actually cheaper than a full table scan — for a small table, or a query expected to "
            "match a large fraction of rows, a full scan can genuinely be faster than the overhead of index "
            "lookups, which is why an index existing doesn't guarantee the optimizer will choose to use it, "
            "and why stale statistics (after a bulk data load, for example) can cause the optimizer to make "
            "poor choices until statistics are refreshed."
        ),
        code=dict(
            lang="sql",
            label="Creating an index and reading an execution plan",
            src=(
                "CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);\n\n"
                "EXPLAIN ANALYZE\n"
                "SELECT * FROM orders\n"
                "WHERE customer_id = 42 AND order_date >= '2026-01-01';\n"
                "-- Look for \"Index Scan using idx_orders_customer_date\" in the output\n"
                "-- versus \"Seq Scan\" (full table scan), which indicates the index isn't being used"
            ),
        ),
        advanced_code=dict(
            lang="sql",
            label="Why column order in a composite index matters",
            src=(
                "CREATE INDEX idx ON orders(customer_id, order_date);\n\n"
                "-- Uses the index efficiently: leftmost column present\n"
                "SELECT * FROM orders WHERE customer_id = 42;\n"
                "SELECT * FROM orders WHERE customer_id = 42 AND order_date > '2026-01-01';\n\n"
                "-- Generally CANNOT use this index efficiently: leftmost column missing\n"
                "SELECT * FROM orders WHERE order_date > '2026-01-01';\n"
                "-- Would need a separate index starting with order_date to help this query"
            ),
        ),
        example=(
            "A dashboard query that took 8 seconds against a 10-million-row orders table dropped to under 50 "
            "milliseconds after adding a single composite index on `(customer_id, order_date)` — the exact "
            "columns the slow query was filtering on, confirmed by comparing the `EXPLAIN ANALYZE` output "
            "before and after."
        ),
        best_practices=[
            "Index columns actually used in WHERE, JOIN, and ORDER BY clauses of your slowest, most frequent queries — not every column defensively.",
            "Put the most selective (or most commonly filtered-alone) column first in a composite index.",
            "Run EXPLAIN ANALYZE on slow queries before guessing at a fix — it shows exactly where the actual cost is concentrated.",
            "Periodically review and remove unused indexes, since every index adds write overhead without a corresponding read benefit if nothing queries it.",
        ],
        pitfalls=[
            "Adding an index to every column 'just in case,' significantly slowing down writes on a busy table for indexes that are rarely, if ever, used by actual queries.",
            "Wrapping an indexed column in a function in WHERE (`WHERE UPPER(email) = 'X'`) without a matching functional index, silently defeating the index and forcing a full scan.",
            "Building a composite index with columns in the wrong order for the actual query patterns, leaving the index unused for the queries it was meant to help.",
        ],
        glossary=[
            dict(term="Index", definition="A separate, sorted data structure (typically a B-tree) that lets the database find matching rows without scanning the whole table."),
            dict(term="Composite index", definition="An index on more than one column, useful for queries filtering on a leftmost prefix of those columns."),
            dict(term="EXPLAIN / EXPLAIN ANALYZE", definition="A command showing the database's query execution plan; ANALYZE additionally runs the query and reports real timing and row counts."),
            dict(term="Full table scan", definition="Reading every row of a table to find matches, used when no suitable index exists or the optimizer decides a scan is cheaper."),
            dict(term="Covering index", definition="An index containing every column a query needs, letting the database satisfy the query from the index alone."),
        ],
        faq=[
            dict(q="If indexes make queries faster, why not index every column?", a="Every index adds storage overhead and slows down every INSERT/UPDATE/DELETE, since the index has to be updated too. Indexing columns that are rarely queried costs write performance for no corresponding read benefit — index deliberately, based on actual query patterns."),
            dict(q="Why isn't my query using the index I created?", a="Common reasons: the column is wrapped in a function call in WHERE, it's not the leftmost column of a composite index, the table is small enough that the optimizer decided a full scan is actually cheaper, or the table's statistics are stale after a large data change. EXPLAIN ANALYZE will show you which."),
            dict(q="Does column order in a composite index really matter that much?", a="Yes — a composite index on (a, b) generally only helps queries filtering on a alone or on a AND b together, not on b alone, the same way a phone book sorted by (last name, first name) doesn't help you search by first name."),
        ],
        quiz=[
            dict(
                question="A composite index exists on (customer_id, order_date). Which query can it NOT efficiently accelerate?",
                options=["WHERE customer_id = 5", "WHERE customer_id = 5 AND order_date > '2026-01-01'", "WHERE order_date > '2026-01-01' (with no customer_id filter)", "All of the above are equally accelerated"],
                correct=2,
                explanation="Composite indexes generally require the leftmost column (customer_id here) to be part of the query's filter to be usable — filtering on order_date alone skips the leftmost column.",
            ),
            dict(
                question="What's the main cost of adding an index?",
                options=["It makes SELECT queries slower", "It adds storage and slows down INSERT/UPDATE/DELETE operations", "It has no real cost", "It only affects queries using ORDER BY"],
                correct=1,
                explanation="Every index must be updated whenever the underlying data changes, which adds overhead to write operations, plus the index itself consumes additional storage.",
            ),
        ],
        prompts=[
            "What index would help this specific slow query, and why?",
            "Explain why column order matters in a composite index.",
            "Walk me through reading this EXPLAIN ANALYZE output.",
            "Why isn't my database using the index I just created?",
        ],
    ),
    dict(
        id="transactions-and-acid",
        title="Transactions & ACID Properties",
        hook="A bank transfer that debits one account but never credits the other because the server crashed mid-operation is exactly the failure mode transactions exist to make impossible.",
        explanation=(
            "A transaction groups multiple statements into a single all-or-nothing unit: `BEGIN;` starts it, "
            "`COMMIT;` makes every change permanent, and `ROLLBACK;` undoes every change made since `BEGIN`, "
            "as if none of them had happened. This matters whenever an operation logically requires several "
            "steps to succeed together — transferring money requires both debiting one account and crediting "
            "another, and a partial completion (debit succeeds, credit fails) would leave the data in a "
            "genuinely broken state.\n\n"
            "ACID describes the guarantees a properly implemented transactional database provides: Atomicity "
            "(all statements in the transaction succeed, or none do), Consistency (the database moves from one "
            "valid state to another, respecting all constraints), Isolation (concurrent transactions don't see "
            "each other's uncommitted changes), and Durability (once committed, changes survive a crash or "
            "power loss).\n\n"
            "Isolation levels (`READ UNCOMMITTED`, `READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`) let "
            "you tune the trade-off between strict correctness and concurrency performance — stricter "
            "isolation prevents more kinds of anomalies (dirty reads, non-repeatable reads, phantom reads) but "
            "generally costs more in locking and reduced concurrent throughput. Most databases default to "
            "`READ COMMITTED`, a reasonable middle ground for most applications.\n\n"
            "A deadlock occurs when two transactions each hold a lock the other needs, neither able to "
            "proceed — databases detect this automatically and abort one of the transactions (returning an "
            "error the application should catch and typically retry), rather than letting both wait forever."
        ),
        deep_dive=(
            "A dirty read (possible under `READ UNCOMMITTED`) means one transaction can see another "
            "transaction's uncommitted changes, which might later be rolled back — reading data that "
            "technically never 'really' existed. A non-repeatable read (possible under `READ COMMITTED`) "
            "means re-reading the same row twice within one transaction can return different values if another "
            "transaction committed a change in between. A phantom read means re-running the same query twice "
            "within one transaction can return a different *set* of rows (not just different values in "
            "existing rows) if another transaction inserted or deleted matching rows in between — "
            "`REPEATABLE READ` prevents non-repeatable reads but not necessarily phantoms in every database; "
            "`SERIALIZABLE` prevents all three at the cost of the most locking/conflict overhead.\n\n"
            "Optimistic locking (checking a version number or timestamp column hasn't changed before "
            "committing an update, and retrying if it has) and pessimistic locking (`SELECT ... FOR UPDATE`, "
            "explicitly locking rows before reading them so no other transaction can modify them until yours "
            "commits) are two different strategies for handling concurrent modification of the same data, "
            "trading off contention overhead against the risk of needing to retry a failed optimistic update.\n\n"
            "Not every database or storage engine supports full ACID guarantees by default — some NoSQL "
            "databases and even some SQL storage engines historically traded strict ACID compliance for higher "
            "write throughput, which is a genuine, deliberate design trade-off worth knowing about a system "
            "before relying on it for financial or otherwise correctness-critical data."
        ),
        code=dict(
            lang="sql",
            label="A transaction ensuring an all-or-nothing transfer",
            src=(
                "BEGIN;\n\n"
                "UPDATE accounts SET balance = balance - 100 WHERE id = 1;\n"
                "UPDATE accounts SET balance = balance + 100 WHERE id = 2;\n\n"
                "-- If anything fails above (constraint violation, crash), neither change is kept\n"
                "COMMIT;\n\n"
                "-- Or, to abandon both changes explicitly:\n"
                "-- ROLLBACK;"
            ),
        ),
        advanced_code=dict(
            lang="sql",
            label="Pessimistic locking with SELECT FOR UPDATE",
            src=(
                "BEGIN;\n\n"
                "-- Locks this row, blocking other transactions from modifying it until COMMIT/ROLLBACK\n"
                "SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;\n\n"
                "-- Application checks the balance is sufficient, then:\n"
                "UPDATE accounts SET balance = balance - 100 WHERE id = 1;\n\n"
                "COMMIT;   -- releases the lock"
            ),
        ),
        example=(
            "An e-commerce checkout wraps 'decrement inventory' and 'create the order record' in a single "
            "transaction — if inventory decrements successfully but the order creation fails for any reason, "
            "the entire transaction rolls back, preventing inventory from being silently lost without a "
            "corresponding order."
        ),
        best_practices=[
            "Wrap any set of statements that must succeed or fail together in an explicit transaction.",
            "Keep transactions as short as possible — long-running transactions hold locks longer, increasing contention and deadlock risk for other concurrent operations.",
            "Handle deadlock errors in application code by catching them and retrying the transaction, rather than treating them as unexpected failures.",
            "Choose an isolation level deliberately based on the specific correctness needs of each operation, rather than always accepting the database's default.",
        ],
        pitfalls=[
            "Performing a multi-step operation (like a transfer) without a transaction, risking a partially completed, inconsistent state if a failure occurs mid-operation.",
            "Holding a transaction open for a long time (waiting on user input, an external API call) while it holds locks, increasing contention for other operations.",
            "Assuming all databases and storage engines provide full ACID guarantees by default without checking the specific system's actual behavior.",
        ],
        glossary=[
            dict(term="Transaction", definition="A group of statements executed as a single all-or-nothing unit, ended with COMMIT (keep changes) or ROLLBACK (undo changes)."),
            dict(term="ACID", definition="Atomicity, Consistency, Isolation, Durability — the guarantees a properly implemented transactional database provides."),
            dict(term="Isolation level", definition="A setting controlling how much concurrent transactions can see of each other's in-progress changes, trading correctness guarantees against concurrency performance."),
            dict(term="Deadlock", definition="A situation where two transactions each hold a lock the other needs, resolved by the database aborting one of them."),
        ],
        faq=[
            dict(q="Do I need an explicit transaction for a single UPDATE statement?", a="Most databases wrap every individual statement in an implicit transaction automatically, so a single statement is already atomic by default. Explicit BEGIN/COMMIT matters once you have multiple statements that must succeed or fail together as one unit."),
            dict(q="What's the practical difference between optimistic and pessimistic locking?", a="Pessimistic locking (SELECT FOR UPDATE) blocks other transactions from touching a row immediately, avoiding conflicts but reducing concurrency. Optimistic locking lets transactions proceed without locking, checking for conflicts only at commit time and retrying if a conflict occurred — better concurrency, but requires handling retries."),
            dict(q="Why did my transaction fail with a deadlock error?", a="Another transaction was holding a lock your transaction needed, while it was simultaneously waiting on a lock your transaction held — the database detected the cycle and aborted one side. The application should catch this and retry the transaction."),
        ],
        quiz=[
            dict(
                question="What does the 'A' in ACID stand for, and what does it guarantee?",
                options=["Availability -- the database is always reachable", "Atomicity -- all statements in a transaction succeed together, or none do", "Accuracy -- results are always numerically correct", "Authentication -- users must log in"],
                correct=1,
                explanation="Atomicity means a transaction is all-or-nothing: if any part fails, the entire transaction is rolled back as if none of it happened.",
            ),
        ],
        prompts=[
            "Why should this multi-step operation be wrapped in a transaction?",
            "Explain the difference between optimistic and pessimistic locking with an example.",
            "What isolation level should I use for this specific scenario?",
            "Why did my transaction fail with a deadlock, and how should my application handle it?",
        ],
    ),
    dict(
        id="normalization",
        title="Database Normalization",
        hook="Normalization isn't an academic exercise — it's a set of rules for organizing tables so that every fact is stored exactly once, which is the difference between updating one row and hunting down five inconsistent copies of the same data.",
        explanation=(
            "Normalization organizes a database schema to reduce data redundancy and prevent update anomalies "
            "— situations where the same fact stored in multiple places can drift out of sync. It's expressed "
            "as a series of 'normal forms,' each building on the last with a stricter rule about how data "
            "should be organized.\n\n"
            "First Normal Form (1NF) requires atomic values — no repeating groups or comma-separated lists "
            "crammed into a single column (`tags: \"red,large,sale\"` violates 1NF; a separate `product_tags` "
            "table with one row per tag doesn't). Second Normal Form (2NF) requires every non-key column to "
            "depend on the *entire* primary key, not just part of it — relevant specifically for tables with "
            "composite primary keys. Third Normal Form (3NF) requires every non-key column to depend only on "
            "the primary key, not on another non-key column (a customer's city shouldn't live in an orders "
            "table just because an order references a customer whose city can be looked up).\n\n"
            "In practice, most well-designed application databases target 3NF as a solid default: each table "
            "represents one clear entity, and facts about that entity live in exactly one place, referenced by "
            "foreign key from anywhere else that needs them.\n\n"
            "Denormalization — deliberately duplicating some data for read performance — is a legitimate, "
            "conscious trade-off in specific cases (like a reporting table pre-joining and pre-aggregating "
            "data for a dashboard), but should be a deliberate choice made after understanding the normalized "
            "design, not a default starting point born from not understanding normalization at all."
        ),
        deep_dive=(
            "Update anomalies are the concrete cost of under-normalized data: if a customer's email is stored "
            "redundantly in both a `customers` table and duplicated into every `orders` row, updating that "
            "email requires finding and updating every order row too — miss one, and the data is now silently "
            "inconsistent, with different orders showing different emails for the same customer.\n\n"
            "Boyce-Codd Normal Form (BCNF) is a slightly stricter version of 3NF handling certain edge cases "
            "with overlapping candidate keys, and higher normal forms (4NF, 5NF) address multi-valued and "
            "join dependencies — these are less commonly relevant to everyday application schema design and "
            "mostly matter for genuinely complex, unusual data relationships.\n\n"
            "The practical skill isn't reciting normal form definitions, but recognizing the smell of "
            "under-normalized data: a column that could be derived from other columns instead of stored "
            "independently (and can drift out of sync), a column storing a comma-separated list that should "
            "be its own table, or a column that depends on a different entity than the one the table "
            "represents."
        ),
        code=dict(
            lang="sql",
            label="Un-normalized vs. normalized schema",
            src=(
                "-- BEFORE: violates 1NF (comma-separated list) and duplicates customer_email\n"
                "-- orders(id, customer_email, customer_city, product_names)\n\n"
                "-- AFTER: normalized into separate, single-purpose tables\n"
                "CREATE TABLE customers (\n"
                "    id SERIAL PRIMARY KEY,\n"
                "    email TEXT UNIQUE NOT NULL,\n"
                "    city TEXT\n"
                ");\n\n"
                "CREATE TABLE orders (\n"
                "    id SERIAL PRIMARY KEY,\n"
                "    customer_id INTEGER REFERENCES customers(id)\n"
                ");\n\n"
                "CREATE TABLE order_items (\n"
                "    order_id INTEGER REFERENCES orders(id),\n"
                "    product_name TEXT NOT NULL\n"
                ");"
            ),
        ),
        advanced_code=dict(
            lang="sql",
            label="A deliberate, documented denormalization for reporting",
            src=(
                "-- Normalized tables remain the source of truth for writes\n"
                "-- This summary table is refreshed periodically, purely for fast reads\n"
                "CREATE TABLE daily_revenue_summary (\n"
                "    report_date DATE PRIMARY KEY,\n"
                "    total_revenue NUMERIC,\n"
                "    order_count INTEGER,\n"
                "    unique_customers INTEGER\n"
                ");\n\n"
                "-- Refreshed on a schedule, e.g. via a nightly job:\n"
                "-- INSERT INTO daily_revenue_summary SELECT ... FROM orders GROUP BY DATE(order_date);"
            ),
        ),
        example=(
            "A support team noticed customer addresses shown on invoices sometimes didn't match the address on "
            "file — the root cause was the address being copied into each invoice row at creation time instead "
            "of referenced from a normalized customers table, so a customer's later address update never "
            "propagated to old (or even recent) invoice records."
        ),
        best_practices=[
            "Design new schemas to at least 3NF by default — one table per clear entity, facts stored once, referenced by foreign key elsewhere.",
            "Store a comma-separated or repeating list of values as its own related table instead of cramming it into a single column.",
            "Treat denormalization as a deliberate, documented performance optimization applied after understanding the normalized design, not a shortcut taken from the start.",
            "When denormalizing for read performance, be explicit about how and when the duplicated data gets refreshed, to avoid silent staleness.",
        ],
        pitfalls=[
            "Storing the same fact (like a customer's email) in multiple tables without a clear, enforced synchronization strategy, letting copies drift out of sync over time.",
            "Cramming a list of values into a single comma-separated text column instead of a proper related table, making that data hard to query, index, or validate.",
            "Denormalizing prematurely, before actually measuring that the normalized design is a genuine performance problem.",
        ],
        glossary=[
            dict(term="Normalization", definition="Organizing a database schema to reduce data redundancy and prevent update anomalies, expressed as a series of normal forms."),
            dict(term="Update anomaly", definition="A bug where the same fact, stored redundantly in multiple places, can be updated in one place but not another, leaving inconsistent data."),
            dict(term="3NF (Third Normal Form)", definition="A schema design level where every non-key column depends only on the table's primary key, not on other non-key columns."),
            dict(term="Denormalization", definition="Deliberately duplicating or pre-aggregating data to improve read performance, at the cost of some redundancy."),
        ],
        faq=[
            dict(q="Do I always need to fully normalize my database?", a="Aim for 3NF as a solid default for the core, write-facing schema. Deliberate denormalization for specific read-heavy use cases (like a reporting table) is a legitimate, common optimization — the key word is deliberate, made after understanding what you're trading away."),
            dict(q="What's a concrete sign my schema isn't normalized enough?", a="If updating one real-world fact (like a customer's address) requires updating more than one row or table, or if you're storing a comma-separated list in a single column, those are classic signs of under-normalization."),
            dict(q="Is denormalization ever a good idea?", a="Yes, when done deliberately for a specific, measured performance need — like a summary table that's refreshed on a schedule specifically to make dashboard queries fast, with the normalized tables remaining the source of truth."),
        ],
        quiz=[
            dict(
                question="What core problem does normalization aim to prevent?",
                options=["Slow queries", "Data redundancy leading to update anomalies where copies of the same fact drift out of sync", "Running out of storage space", "SQL injection attacks"],
                correct=1,
                explanation="Normalization's main goal is ensuring each fact is stored in exactly one place, so updating it doesn't require finding and updating multiple, possibly-missed copies.",
            ),
        ],
        prompts=[
            "Is this schema properly normalized? Point out any issues.",
            "Explain the difference between 1NF, 2NF, and 3NF with a concrete example.",
            "When is denormalization actually a good idea?",
            "Redesign this flat table into a normalized schema.",
        ],
    ),
    dict(
        id="null-handling-coalesce",
        title="NULL Handling: COALESCE, NULLIF & Three-Valued Logic",
        hook="SQL doesn't have just true and false — it has a third value, unknown, and NULL is how that shows up, which quietly changes how AND, OR, and NOT behave compared to any language with plain booleans.",
        explanation=(
            "NULL represents a missing or unknown value, not zero, not an empty string, and not false — it's "
            "its own distinct concept. Any arithmetic or comparison involving NULL generally produces NULL: "
            "`5 + NULL` is NULL, `NULL = NULL` is NULL (not true), which is why `IS NULL`/`IS NOT NULL` exist "
            "as dedicated operators rather than relying on `=`.\n\n"
            "SQL's logic is technically three-valued: true, false, and unknown (NULL). `AND` returns unknown "
            "if either side is unknown and the other isn't false; `OR` returns unknown if either side is "
            "unknown and the other isn't true; `NOT unknown` is still unknown. In a `WHERE` clause, only rows "
            "where the condition evaluates to true are kept — both false and unknown rows are excluded, which "
            "is why NULLs can silently vanish from results in ways that surprise people expecting NULL to "
            "behave like Python's `None` or JavaScript's `null` in a boolean context.\n\n"
            "`COALESCE(value1, value2, ...)` returns the first non-null argument, a clean way to provide a "
            "fallback: `COALESCE(nickname, first_name, 'Anonymous')` shows a nickname if set, otherwise the "
            "first name, otherwise a hardcoded default. `NULLIF(a, b)` returns NULL if `a` equals `b`, "
            "otherwise returns `a` — useful for converting a sentinel 'no value' marker (like an empty string "
            "or a placeholder number) into a genuine NULL for cleaner downstream handling.\n\n"
            "Aggregate functions generally ignore NULLs rather than treating them as zero — `AVG(column)` "
            "divides by the count of non-null values, not the total row count, which means a column with some "
            "NULLs can produce a different average than you'd get by first replacing NULLs with zero."
        ),
        deep_dive=(
            "`NOT IN` with a subquery that could return NULL is a classic, dangerous trap: `WHERE id NOT IN "
            "(SELECT customer_id FROM banned_customers)` returns *zero rows* if even one row in "
            "`banned_customers.customer_id` is NULL, because `NOT IN` is really a chain of `<>` comparisons "
            "joined with `AND`, and any comparison against NULL makes the whole chain unknown rather than "
            "true. The safe fix is `NOT EXISTS` (which doesn't have this failure mode) or explicitly filtering "
            "out NULLs from the subquery first.\n\n"
            "`UNIQUE` constraints generally allow multiple NULL values in most databases (though this varies "
            "slightly — check your specific database), since NULL is treated as 'unknown, possibly different "
            "from every other unknown value' rather than as a value that could duplicate another NULL.\n\n"
            "`COALESCE` is technically a standard SQL construct built on top of the more general `CASE WHEN`, "
            "and understanding that equivalence helps when you need slightly more complex fallback logic than "
            "COALESCE's simple 'first non-null' behavior can express directly."
        ),
        code=dict(
            lang="sql",
            label="COALESCE and NULLIF for clean fallback logic",
            src=(
                "SELECT\n"
                "    name,\n"
                "    COALESCE(phone, email, 'No contact info') AS contact,\n"
                "    NULLIF(discount_code, '') AS discount_code   -- '' becomes NULL for consistency\n"
                "FROM customers;\n\n"
                "-- Aggregate functions ignore NULLs\n"
                "SELECT AVG(rating) FROM reviews;   -- averages only the non-null ratings"
            ),
        ),
        advanced_code=dict(
            lang="sql",
            label="The NOT IN with NULL trap, and the safe fix",
            src=(
                "-- DANGEROUS: returns ZERO rows if banned_customers.customer_id has any NULL\n"
                "SELECT * FROM customers\n"
                "WHERE id NOT IN (SELECT customer_id FROM banned_customers);\n\n"
                "-- SAFE: NOT EXISTS doesn't have this failure mode\n"
                "SELECT * FROM customers c\n"
                "WHERE NOT EXISTS (\n"
                "    SELECT 1 FROM banned_customers b WHERE b.customer_id = c.id\n"
                ");"
            ),
        ),
        example=(
            "A report silently returning zero results for weeks traced back to a single NULL that crept into "
            "an exclusion list used inside a `NOT IN` subquery — switching to `NOT EXISTS` fixed the query "
            "permanently and made it immune to this entire class of bug regardless of future NULLs in that "
            "list."
        ),
        best_practices=[
            "Use COALESCE for fallback values instead of a CASE WHEN column IS NULL THEN ... construct when the logic is a simple 'first non-null' choice.",
            "Prefer NOT EXISTS over NOT IN when the subquery's result could ever contain a NULL value.",
            "Remember that aggregate functions ignore NULLs by default — be explicit (with COALESCE) if you actually want NULLs treated as zero for a specific calculation.",
            "Test WHERE clauses involving NULL-able columns explicitly against rows containing NULL, since three-valued logic can silently exclude them.",
        ],
        pitfalls=[
            "Using NOT IN with a subquery that can return NULL, silently returning zero rows instead of the expected exclusion.",
            "Assuming NULL = NULL evaluates to true — it evaluates to unknown, which behaves like false for filtering purposes.",
            "Forgetting that AVG(), SUM(), and similar aggregates skip NULLs rather than treating them as zero, which can shift a computed average unexpectedly.",
        ],
        glossary=[
            dict(term="Three-valued logic", definition="SQL's logic system of true, false, and unknown (NULL), which changes how AND/OR/NOT and WHERE filtering behave compared to two-valued boolean logic."),
            dict(term="COALESCE", definition="Returns the first non-null value from a list of arguments, commonly used for fallback/default values."),
            dict(term="NULLIF", definition="Returns NULL if two arguments are equal, otherwise returns the first argument — useful for converting sentinel values into true NULLs."),
        ],
        faq=[
            dict(q="Why did my NOT IN query return zero rows when I know there should be matches?", a="Almost certainly because the subquery's result set contains at least one NULL. NOT IN effectively becomes a chain of AND-ed inequality checks, and any comparison against NULL makes the entire chain evaluate to unknown, excluding every row. Use NOT EXISTS instead."),
            dict(q="Does AVG() treat NULL as zero?", a="No — AVG() (and most aggregate functions) simply ignore NULL values, computing the average over only the non-null rows. If you want NULLs treated as zero, wrap the column in COALESCE(column, 0) first."),
            dict(q="Can a UNIQUE constraint have multiple NULL values in the same column?", a="In most databases, yes — NULL is treated as unknown rather than a specific duplicable value, so multiple NULLs typically don't violate a UNIQUE constraint. This does vary slightly by database, so it's worth confirming for your specific system."),
        ],
        quiz=[
            dict(
                question="Why is NOT IN dangerous when the subquery might return NULL?",
                options=["It causes a syntax error", "It silently returns zero rows instead of the expected results", "It's actually perfectly safe", "It only affects performance, not correctness"],
                correct=1,
                explanation="NOT IN effectively ANDs together inequality checks against every value in the subquery; a NULL among them makes the whole condition evaluate to unknown for every row, excluding all of them.",
            ),
        ],
        prompts=[
            "Why did my NOT IN query return no results even though I expected matches?",
            "Show me how to use COALESCE to provide a fallback contact method.",
            "Explain three-valued logic in SQL with a concrete WHERE clause example.",
            "Does SUM() treat NULL values as zero or skip them?",
        ],
    ),
    dict(
        id="set-operations",
        title="Set Operations: UNION, INTERSECT & EXCEPT",
        hook="These three operators combine the results of two separate queries the way set theory combines groups — union, intersection, and difference — as long as both queries return the same shape.",
        explanation=(
            "`UNION` combines the results of two queries into one result set, removing duplicate rows by "
            "default; `UNION ALL` does the same but keeps duplicates, and is meaningfully faster since it "
            "skips the deduplication step — use `UNION ALL` whenever you know the two queries can't produce "
            "overlapping rows, or don't care about duplicates. `INTERSECT` returns only rows present in "
            "*both* queries' results. `EXCEPT` (called `MINUS` in some databases like Oracle) returns rows "
            "present in the first query but not the second.\n\n"
            "All three require the combined queries to have the same number of columns, in compatible data "
            "types, in the same order — column names in the final result come from the first query, "
            "regardless of what the second query's columns are named.\n\n"
            "A common, genuinely useful pattern is combining data from structurally similar tables — "
            "`SELECT name, 'customer' AS type FROM customers UNION ALL SELECT name, 'vendor' AS type FROM "
            "vendors` merges two different entity tables into one unified list, tagged by source, for a "
            "combined search or report.\n\n"
            "`INTERSECT` and `EXCEPT` are frequently expressible as equivalent JOIN or `EXISTS`/`NOT EXISTS` "
            "queries instead — which approach reads more clearly, and which performs better, depends on the "
            "specific database and data, making it worth comparing both when performance matters."
        ),
        deep_dive=(
            "`UNION`'s automatic deduplication considers the *entire row* across all selected columns — two "
            "rows are only removed as duplicates if every column matches exactly, which is different from "
            "deduplicating based on just one 'key' column the way `DISTINCT ON` (in PostgreSQL) or a "
            "window-function-based approach might.\n\n"
            "Ordering a `UNION`'s combined result requires a single `ORDER BY` at the very end of the whole "
            "statement, not one per individual query — SQL doesn't let you meaningfully order each half "
            "separately and then just concatenate them, since the union operation itself doesn't preserve "
            "input order.\n\n"
            "`INTERSECT` and `EXCEPT` treat NULL as equal to NULL for the purposes of matching rows between "
            "the two queries, which is a deliberate exception to SQL's usual three-valued NULL logic (where "
            "`NULL = NULL` is unknown) — this makes set operations behave more intuitively for the specific "
            "job of comparing whole rows for equality."
        ),
        code=dict(
            lang="sql",
            label="UNION combining structurally similar tables",
            src=(
                "SELECT name, email, 'customer' AS source FROM customers\n"
                "UNION ALL\n"
                "SELECT name, email, 'vendor' AS source FROM vendors\n"
                "ORDER BY name;\n\n"
                "-- Customers who are ALSO vendors (same email used for both)\n"
                "SELECT email FROM customers\n"
                "INTERSECT\n"
                "SELECT email FROM vendors;"
            ),
        ),
        advanced_code=dict(
            lang="sql",
            label="EXCEPT to find rows in one table but not another",
            src=(
                "-- Products that exist in the catalog but have never been ordered\n"
                "SELECT id FROM products\n"
                "EXCEPT\n"
                "SELECT DISTINCT product_id FROM order_items;\n\n"
                "-- Equivalent, often faster, LEFT JOIN version\n"
                "SELECT p.id\n"
                "FROM products p\n"
                "LEFT JOIN order_items oi ON p.id = oi.product_id\n"
                "WHERE oi.product_id IS NULL;"
            ),
        ),
        example=(
            "A data quality check comparing two systems' customer lists uses `EXCEPT` in both directions — "
            "`system_a EXCEPT system_b` finds customers missing from system B, and `system_b EXCEPT system_a` "
            "finds the reverse — a two-line reconciliation report instead of a manual comparison."
        ),
        best_practices=[
            "Use UNION ALL instead of UNION whenever you know the results can't overlap, or duplicates are acceptable — it skips an unnecessary deduplication step.",
            "Add a literal 'source' column when combining structurally similar tables with UNION, so the origin of each row remains identifiable in the combined result.",
            "Compare a set-operation query against an equivalent JOIN/EXISTS rewrite when performance matters — one often outperforms the other depending on the database and data.",
            "Put ORDER BY once, at the very end of the whole combined statement, not inside each individual SELECT being unioned.",
        ],
        pitfalls=[
            "Using UNION when UNION ALL was intended, paying an unnecessary deduplication cost on large result sets that couldn't have overlapping rows anyway.",
            "Combining queries with mismatched column counts or incompatible types, which raises an error rather than silently working.",
            "Forgetting that UNION's deduplication compares entire rows, not just a 'key' column, when a different kind of deduplication was actually intended.",
        ],
        glossary=[
            dict(term="UNION", definition="Combines two queries' results into one set, removing duplicate rows by default."),
            dict(term="UNION ALL", definition="Combines two queries' results into one set, keeping all duplicates, and generally faster than UNION."),
            dict(term="INTERSECT", definition="Returns only rows present in both queries' results."),
            dict(term="EXCEPT / MINUS", definition="Returns rows present in the first query's results but not the second's."),
        ],
        faq=[
            dict(q="What's the actual performance difference between UNION and UNION ALL?", a="UNION has to deduplicate the combined result, which typically requires an extra sort or hash step over the whole result set. UNION ALL skips that entirely, making it meaningfully cheaper whenever you don't need (or know you won't have) duplicate rows."),
            dict(q="Can I use ORDER BY inside each query being combined with UNION?", a="No — a single ORDER BY at the very end of the entire UNION statement is required to order the final combined result; SQL doesn't preserve or care about any ordering applied to the individual queries being combined."),
            dict(q="Is EXCEPT the same as a LEFT JOIN with a NULL check?", a="They frequently produce the same logical result, and which one performs better depends on the specific database and data — it's worth testing both when this kind of query becomes a performance bottleneck."),
        ],
        quiz=[
            dict(
                question="What's the main practical difference between UNION and UNION ALL?",
                options=["UNION is faster", "UNION removes duplicate rows, UNION ALL keeps them (and is typically faster)", "They are identical in every way", "UNION ALL only works with two tables"],
                correct=1,
                explanation="UNION performs deduplication across the combined result, which costs extra work; UNION ALL skips that step and keeps every row, including duplicates.",
            ),
        ],
        prompts=[
            "Combine these two structurally similar tables into one report with a source column.",
            "Show me an EXCEPT query, and an equivalent LEFT JOIN version, for the same result.",
            "When should I use UNION ALL instead of UNION?",
            "Why did my UNION query error out with a column count mismatch?",
        ],
    ),
    dict(
        id="views-and-stored-procedures",
        title="Views & Stored Procedures",
        hook="A view is a saved query you can treat like a table; a stored procedure is saved logic you can treat like a function — both exist to keep repeated SQL in one place instead of copy-pasted everywhere it's needed.",
        explanation=(
            "A view (`CREATE VIEW active_customers AS SELECT * FROM customers WHERE status = 'active';`) "
            "saves a query under a name you can then `SELECT FROM` like a regular table. It doesn't store data "
            "itself (unless it's a materialized view) — every time you query the view, the underlying query "
            "runs fresh. Views are useful for hiding complexity (a complicated multi-join query becomes a "
            "simple `SELECT * FROM sales_summary`), enforcing consistent business logic (every place checking "
            "for 'active' customers uses the same definition), and restricting access (exposing only certain "
            "columns or rows to a group of users without granting access to the full underlying table).\n\n"
            "A materialized view is similar but *does* store its result physically, computed once and then "
            "refreshed periodically (`REFRESH MATERIALIZED VIEW ...`) rather than recomputed on every query — "
            "trading data freshness for query speed, appropriate for expensive aggregations that don't need "
            "to reflect the absolute latest data every single time they're read.\n\n"
            "A stored procedure is a named, saved block of procedural logic (loops, conditionals, multiple "
            "statements) stored inside the database itself and invoked with `CALL procedure_name(args)`. "
            "Unlike a view (which is just a saved SELECT), a procedure can perform multiple operations, "
            "including inserts, updates, and deletes, and can contain control flow that plain SQL statements "
            "can't express on their own.\n\n"
            "A function (as distinct from a procedure in most databases) returns a value and can be used "
            "inside an expression, like `SELECT calculate_tax(total) FROM orders;`, whereas a procedure is "
            "invoked as a standalone statement and typically used for actions rather than value computation."
        ),
        deep_dive=(
            "Putting business logic in stored procedures moves it into the database layer, which has real "
            "trade-offs: it guarantees the logic runs identically regardless of which application or language "
            "calls it, and can reduce network round-trips for multi-step operations — but it also makes that "
            "logic harder to version-control, test, and review compared to application code in a typical "
            "software engineering workflow, and ties your logic more tightly to a specific database vendor's "
            "procedural language (PL/pgSQL, T-SQL, PL/SQL are all different, mutually incompatible dialects).\n\n"
            "Views can be updatable in some cases — a simple view over a single table with no aggregation can "
            "often accept `INSERT`/`UPDATE`/`DELETE` statements that pass through to the underlying table, but "
            "a view involving a join, `GROUP BY`, or `DISTINCT` generally cannot, since there's no "
            "unambiguous way to map a change back to the underlying rows.\n\n"
            "Row-level security (supported natively by some databases like PostgreSQL) is a more modern "
            "alternative to using views purely for access control — it lets you define policies directly on a "
            "table that automatically filter which rows a given user can see or modify, without needing a "
            "separate view object for every access pattern."
        ),
        code=dict(
            lang="sql",
            label="A view simplifying a repeated complex query",
            src=(
                "CREATE VIEW customer_order_summary AS\n"
                "SELECT\n"
                "    c.id,\n"
                "    c.name,\n"
                "    COUNT(o.id) AS order_count,\n"
                "    COALESCE(SUM(o.total), 0) AS lifetime_value\n"
                "FROM customers c\n"
                "LEFT JOIN orders o ON c.id = o.customer_id\n"
                "GROUP BY c.id, c.name;\n\n"
                "-- Now anyone can just:\n"
                "SELECT * FROM customer_order_summary WHERE lifetime_value > 1000;"
            ),
        ),
        advanced_code=dict(
            lang="sql",
            label="A stored procedure performing a multi-step operation (PostgreSQL syntax)",
            src=(
                "CREATE OR REPLACE PROCEDURE transfer_funds(\n"
                "    from_account INT, to_account INT, amount NUMERIC\n"
                ")\n"
                "LANGUAGE plpgsql\n"
                "AS $$\n"
                "BEGIN\n"
                "    IF (SELECT balance FROM accounts WHERE id = from_account) < amount THEN\n"
                "        RAISE EXCEPTION 'Insufficient funds';\n"
                "    END IF;\n\n"
                "    UPDATE accounts SET balance = balance - amount WHERE id = from_account;\n"
                "    UPDATE accounts SET balance = balance + amount WHERE id = to_account;\n"
                "END;\n"
                "$$;\n\n"
                "CALL transfer_funds(1, 2, 100);"
            ),
        ),
        example=(
            "A company exposes a `public_employee_directory` view showing only name, department, and office "
            "location — deliberately excluding salary and other sensitive columns present in the underlying "
            "`employees` table — so a broad group of internal tools can query the view safely without ever "
            "being granted direct access to the sensitive columns."
        ),
        best_practices=[
            "Use views to hide complex, repeated query logic behind a simple, stable name that consuming code can rely on.",
            "Reach for a materialized view when a query is expensive and doesn't need to reflect the absolute latest data on every read.",
            "Keep stored procedures focused on genuinely multi-step, transactional operations rather than logic that would be just as clear (and easier to test) in application code.",
            "Use views deliberately for access control when you need to expose a restricted subset of columns or rows without duplicating the underlying table.",
        ],
        pitfalls=[
            "Building views on top of other views several layers deep, making the actual underlying query nearly impossible to reason about or optimize.",
            "Putting substantial business logic in stored procedures without the same version control, testing, and review discipline applied to application code.",
            "Assuming a materialized view is always up to date — it only reflects data as of its last refresh, which can be stale if not refreshed on an appropriate schedule.",
        ],
        glossary=[
            dict(term="View", definition="A saved, named query that can be queried like a table; recomputed fresh on every read unless it's a materialized view."),
            dict(term="Materialized view", definition="A view whose result is physically stored and refreshed periodically, trading data freshness for query speed."),
            dict(term="Stored procedure", definition="A named, saved block of procedural SQL logic (potentially with loops, conditionals, multiple statements) stored and executed inside the database."),
        ],
        faq=[
            dict(q="Does querying a view re-run the underlying query every time?", a="For a regular (non-materialized) view, yes — it's essentially a saved alias for the query, executed fresh on each SELECT. A materialized view instead stores the result physically and only updates it when explicitly refreshed."),
            dict(q="When should business logic live in a stored procedure instead of application code?", a="When an operation genuinely needs to be atomic and multi-step at the database level (like a fund transfer), or must run identically regardless of which application calls it. For most everyday logic, application code is easier to test, version, and review."),
            dict(q="Can I always update data through a view?", a="Only for relatively simple views over a single table with no aggregation, joins, or DISTINCT — anything more complex generally can't be unambiguously mapped back to a change in the underlying table(s)."),
        ],
        quiz=[
            dict(
                question="What's the key difference between a regular view and a materialized view?",
                options=["Regular views are faster", "A materialized view physically stores its result, refreshed periodically; a regular view recomputes on every query", "Materialized views can't be queried with SELECT", "There is no real difference"],
                correct=1,
                explanation="A materialized view trades data freshness for speed by storing its result physically instead of recomputing the underlying query on every read.",
            ),
        ],
        prompts=[
            "Should this repeated query be a view or a materialized view?",
            "Write a stored procedure that safely transfers funds between two accounts.",
            "When does it make sense to put logic in a stored procedure instead of application code?",
            "Can I insert data through this specific view, and why or why not?",
        ],
    ),
    dict(
        id="data-types-and-constraints",
        title="Data Types & Constraints",
        hook="Choosing the right column type and constraints upfront is cheap; discovering a wrong one after a table has a billion rows and production traffic depending on it is not.",
        explanation=(
            "Common SQL data types include integer variants (`SMALLINT`, `INTEGER`, `BIGINT`, differing in "
            "storage size and maximum value), floating-point and exact decimal types (`FLOAT`/`REAL` for "
            "approximate values, `NUMERIC`/`DECIMAL(precision, scale)` for exact values like currency, where "
            "floating-point rounding errors are unacceptable), text types (`VARCHAR(n)` with a length limit, "
            "`TEXT` generally unlimited), and temporal types (`DATE`, `TIME`, `TIMESTAMP`, `TIMESTAMP WITH "
            "TIME ZONE`).\n\n"
            "Constraints enforce rules the database itself guarantees, regardless of which application or "
            "person writes to the table: `NOT NULL` forbids missing values, `UNIQUE` forbids duplicate values "
            "in a column (or combination of columns), `PRIMARY KEY` combines `NOT NULL` and `UNIQUE` to "
            "identify each row uniquely, `FOREIGN KEY` ensures a column's value matches an existing row in "
            "another table (referential integrity), and `CHECK` enforces an arbitrary boolean condition "
            "(`CHECK (price >= 0)`).\n\n"
            "Enforcing rules at the database level with constraints is meaningfully more reliable than only "
            "validating in application code, because the database is the last line of defense against *any* "
            "write path — a buggy script, a different application, or direct manual access all still have to "
            "satisfy the constraints, while application-level validation only protects the specific code path "
            "that includes it.\n\n"
            "Choosing `NUMERIC(10, 2)` over `FLOAT` for a money column isn't a stylistic preference — "
            "floating-point types can't represent many decimal fractions exactly (the same reason `0.1 + 0.2` "
            "doesn't equal `0.3` exactly in most programming languages), which can accumulate into real "
            "financial discrepancies over many transactions."
        ),
        deep_dive=(
            "Foreign key constraints support different `ON DELETE` behaviors for what happens to child rows "
            "when a referenced parent row is deleted: `CASCADE` deletes the child rows too, `SET NULL` sets "
            "the foreign key column to NULL, `RESTRICT` (or the default in many databases) prevents the "
            "delete entirely while child rows still reference that parent. Choosing the wrong one is a common "
            "source of either unexpected data loss (`CASCADE` where it wasn't intended) or unexpected delete "
            "failures (`RESTRICT` where cascading was actually wanted).\n\n"
            "`CHECK` constraints let you encode business rules directly into the schema — `CHECK (end_date > "
            "start_date)`, `CHECK (status IN ('pending', 'shipped', 'delivered'))` — catching invalid data at "
            "the moment of insertion rather than discovering it later during analysis or reporting, when the "
            "source of the bad data may be long gone or hard to trace.\n\n"
            "Choosing between `VARCHAR(n)` and `TEXT` is largely a non-issue in modern PostgreSQL (both are "
            "stored the same way internally, with `VARCHAR(n)` just adding a length check), though it still "
            "matters in some other databases where `VARCHAR` and `TEXT` have genuinely different storage and "
            "performance characteristics — worth checking your specific database's documentation rather than "
            "assuming behavior carries over from a different system."
        ),
        code=dict(
            lang="sql",
            label="A table with meaningful data types and constraints",
            src=(
                "CREATE TABLE orders (\n"
                "    id BIGSERIAL PRIMARY KEY,\n"
                "    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,\n"
                "    total NUMERIC(10, 2) NOT NULL CHECK (total >= 0),\n"
                "    status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'shipped', 'delivered')),\n"
                "    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),\n"
                "    UNIQUE (customer_id, created_at)\n"
                ");"
            ),
        ),
        advanced_code=dict(
            lang="sql",
            label="Comparing ON DELETE behaviors for foreign keys",
            src=(
                "-- CASCADE: deleting a customer deletes all their orders too\n"
                "customer_id INTEGER REFERENCES customers(id) ON DELETE CASCADE\n\n"
                "-- SET NULL: deleting a customer leaves orders, but customer_id becomes NULL\n"
                "customer_id INTEGER REFERENCES customers(id) ON DELETE SET NULL\n\n"
                "-- RESTRICT (often the default): deleting a customer with existing orders FAILS\n"
                "customer_id INTEGER REFERENCES customers(id) ON DELETE RESTRICT"
            ),
        ),
        example=(
            "A financial system storing prices as `FLOAT` instead of `NUMERIC(10,2)` accumulated a few cents "
            "of rounding error across millions of transactions over a year — invisible on any single "
            "transaction, but a real, auditable discrepancy once totaled, entirely avoidable by using an exact "
            "decimal type for money from the start."
        ),
        best_practices=[
            "Use NUMERIC/DECIMAL for money and any value requiring exact decimal precision, never FLOAT/REAL.",
            "Add NOT NULL, CHECK, and FOREIGN KEY constraints at the database level for any rule that must always hold, rather than relying purely on application-level validation.",
            "Choose ON DELETE behavior for every foreign key deliberately (CASCADE, SET NULL, or RESTRICT) based on the actual desired business behavior, not the database's default.",
            "Pick integer sizes (SMALLINT/INTEGER/BIGINT) based on genuinely expected value ranges, considering long-term growth, not just what fits today.",
        ],
        pitfalls=[
            "Using FLOAT for currency values, introducing rounding errors that accumulate into real discrepancies over many transactions.",
            "Leaving a foreign key's ON DELETE behavior at the default without considering whether CASCADE or RESTRICT is actually the intended business behavior.",
            "Relying solely on application-level validation for rules that should be enforced by the database itself, leaving the data vulnerable to any write path that skips that validation.",
        ],
        glossary=[
            dict(term="NUMERIC(p, s)", definition="An exact decimal type with p total digits and s digits after the decimal point, appropriate for money and other values needing exact precision."),
            dict(term="Constraint", definition="A rule (NOT NULL, UNIQUE, CHECK, FOREIGN KEY) enforced by the database itself on every write, regardless of which application performs it."),
            dict(term="Referential integrity", definition="The guarantee that a foreign key value always matches an existing row in the referenced table, enforced automatically by a FOREIGN KEY constraint."),
            dict(term="ON DELETE CASCADE / SET NULL / RESTRICT", definition="Foreign key options controlling what happens to child rows when their referenced parent row is deleted."),
        ],
        faq=[
            dict(q="Why not just validate everything in my application code instead of using database constraints?", a="Application-level validation only protects requests that go through that specific code path. A database constraint is enforced for every write, from any application, script, or manual query — the database becomes the reliable last line of defense rather than trusting every caller to remember to validate."),
            dict(q="What's actually wrong with using FLOAT for prices?", a="Floating-point types can't represent many decimal fractions exactly in binary, the same reason 0.1 + 0.2 often doesn't equal exactly 0.3 in most languages. These tiny errors can accumulate into real, auditable discrepancies across many financial transactions — NUMERIC/DECIMAL avoids this entirely."),
            dict(q="What happens if I delete a customer row without specifying an ON DELETE behavior?", a="Most databases default to RESTRICT (or an equivalent), preventing the delete entirely if any orders still reference that customer — you'd need to either delete the orders first, or define a different ON DELETE behavior if cascading deletion is actually the intended behavior."),
        ],
        quiz=[
            dict(
                question="Why should money be stored as NUMERIC/DECIMAL instead of FLOAT?",
                options=["FLOAT takes up more storage", "FLOAT can't represent many decimal fractions exactly, risking accumulated rounding errors", "NUMERIC is always faster", "There's no real difference in modern databases"],
                correct=1,
                explanation="Floating-point binary representation can't exactly represent many decimal values, and repeated arithmetic on approximate values can accumulate into real discrepancies over many transactions.",
            ),
        ],
        prompts=[
            "What data type should I use for a column storing product prices, and why?",
            "Explain the difference between ON DELETE CASCADE, SET NULL, and RESTRICT with examples.",
            "Why should I add database constraints if I already validate input in my application?",
            "Design a table schema with appropriate types and constraints for a simple blog.",
        ],
    ),
]