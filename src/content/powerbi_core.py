"""Power BI subtopics — enriched schema."""

SUBTOPICS = [
    dict(
        id="powerbi-workflow",
        title="The Power BI Workflow: Query, Model, Visualize",
        hook="Power BI isn't one tool, it's three stages stitched together — knowing which stage a problem belongs to saves hours of hunting in the wrong pane.",
        explanation=(
            "Power BI Desktop splits work into three distinct stages, visible as separate panes: Power Query "
            "(get and clean data), Data Modeling (define relationships and calculations), and Report/Visualize "
            "(build the actual charts and dashboards). A report is only as good as the model underneath it, and "
            "a model is only as good as the query that shaped the raw data — problems compound downstream, so "
            "experienced Power BI users spend proportionally more time in Query and Model than in Visualize.\n\n"
            "Power Query uses a functional language called M to record every cleaning step (remove a column, "
            "change a type, filter rows) as a repeatable, auditable sequence rather than a one-off manual edit. "
            "The Data Model stage is where you define relationships between tables and write DAX measures. Only "
            "after both are solid does building visuals become the fast, almost mechanical last step.\n\n"
            "Every step recorded in Power Query is replayed automatically on every data refresh, which is the "
            "entire point of doing cleaning there instead of manually editing a spreadsheet before importing "
            "it — the transformation logic becomes part of the reproducible pipeline rather than a one-time, "
            "unrepeatable manual edit that has to be redone by hand every time the underlying data updates."
        ),
        deep_dive=(
            "The M language underlying Power Query is a functional, expression-based language — every applied "
            "step is actually an M function call, chained together, and visible/editable directly in the "
            "Advanced Editor for anyone who outgrows the point-and-click UI. Understanding that the UI is just "
            "a friendly front-end generating M code demystifies a lot of Power Query's behavior, especially "
            "when a step needs custom logic the UI doesn't expose directly.\n\n"
            "Query folding is an important, easy-to-miss performance concept: when your data source is a "
            "database, Power Query tries to push transformation steps (filters, column selections) back down "
            "into the source as part of the actual SQL query it generates, rather than pulling all the raw "
            "data first and filtering afterward in Power BI. Certain steps (like custom M functions) can break "
            "query folding, silently causing Power BI to pull far more raw data than necessary — a common, "
            "hard-to-notice source of slow refreshes.\n\n"
            "Import mode (data is copied into Power BI's own compressed in-memory engine) versus DirectQuery "
            "mode (Power BI queries the source live, on demand, without storing a copy) is a foundational "
            "choice affecting performance, data freshness, and available DAX functionality — Import mode is "
            "generally faster and more flexible, while DirectQuery trades some of that for always-current data "
            "against very large source systems that can't be fully imported."
        ),
        code=dict(
            lang="text",
            label="The three stages and what lives in each",
            src=(
                "1. Power Query (Get Data)\n"
                "   - Connect to sources, remove columns, fix types, unpivot, merge queries\n"
                "   - Language: M\n\n"
                "2. Data Model (Model view)\n"
                "   - Define relationships (1:many), write DAX measures and calculated columns\n"
                "   - Language: DAX\n\n"
                "3. Report (Report view)\n"
                "   - Drag fields onto visuals, add slicers, arrange pages"
            ),
        ),
        advanced_code=dict(
            lang="text",
            label="Import mode vs. DirectQuery — the key trade-off",
            src=(
                "Import mode:\n"
                "  + Fast (data compressed, held in memory)\n"
                "  + Full DAX function support\n"
                "  - Data only as current as the last refresh\n"
                "  - Limited by available memory for very large datasets\n\n"
                "DirectQuery mode:\n"
                "  + Always queries live, current data\n"
                "  + Can handle datasets far larger than memory allows\n"
                "  - Slower (every visual interaction re-queries the source)\n"
                "  - Some DAX functions unavailable or behave differently"
            ),
        ),
        example=(
            "A sales dashboard that looks broken (totals don't add up, dates display wrong) is almost always a "
            "modeling or query problem wearing a visualization costume — fixing a wrong data type in Power Query "
            "or a missing relationship in the model resolves it, not tweaking the chart itself."
        ),
        best_practices=[
            "Fix data quality issues in Power Query, not with DAX workarounds in the model — clean once at the source, not repeatedly in every measure.",
            "Build a star schema (one fact table, several dimension tables) rather than one giant flat table — it's dramatically easier to write correct DAX against.",
            "Name your queries, tables, and measures clearly and consistently from the start; renaming later breaks every visual referencing the old name.",
            "Check whether query folding is happening for database sources, especially after adding custom M logic — it's a common, invisible performance killer.",
        ],
        pitfalls=[
            "Importing a huge flat Excel export as-is instead of splitting it into fact and dimension tables during Power Query.",
            "Applying the same cleaning step manually every time you refresh instead of encoding it once in the Power Query steps.",
            "Choosing DirectQuery by default without understanding its performance and DAX limitations compared to Import mode.",
        ],
        glossary=[
            dict(term="M language", definition="The functional, expression-based language underlying every Power Query step, generated automatically by the UI or editable directly."),
            dict(term="Query folding", definition="Power Query pushing transformation steps back into the source database's own query, rather than pulling raw data and transforming it afterward — important for refresh performance."),
            dict(term="Import mode", definition="Power BI's default mode, copying data into its own compressed in-memory engine for fast querying, refreshed on a schedule."),
            dict(term="DirectQuery mode", definition="Power BI querying the data source live for every interaction, keeping data always current at the cost of speed and some DAX limitations."),
        ],
        faq=[
            dict(q="Why does a star schema make DAX easier to write than a flat table?", a="A star schema lets relationships automatically propagate filters from dimension tables to the fact table, so DAX measures can rely on that automatic filtering instead of manually re-deriving relationships inside every formula — a flat table forces you to encode that logic repeatedly and error-pronely in DAX itself."),
            dict(q="Walk through cleaning a messy CSV export in Power Query step by step.", a="Typical steps: promote the first row to headers, fix column data types, remove unnecessary columns, filter out blank/invalid rows, split or merge columns as needed, and rename columns for clarity — each step recorded and replayed automatically on every future refresh."),
            dict(q="What's the difference between a calculated column and a measure, and when do I use each?", a="See the DAX Fundamentals lesson for the full explanation — briefly, a calculated column computes once per row at refresh time and is stored; a measure computes dynamically at query time based on the current filter context and is never stored."),
        ],
        quiz=[
            dict(
                question="What does 'query folding' refer to in Power Query?",
                options=["Combining two queries into one visually", "Pushing transformation steps back into the source database's own query for performance", "Collapsing the Power Query pane in the UI", "A DAX function for aggregating data"],
                correct=1,
                explanation="Query folding lets Power BI push filters and transformations down into the source system's actual query, avoiding pulling more raw data than necessary — breaking it can silently hurt refresh performance.",
            ),
        ],
        prompts=[
            "Why does a star schema make DAX easier to write than a flat table?",
            "Walk through cleaning a messy CSV export in Power Query step by step.",
            "What's the difference between a calculated column and a measure, and when do I use each?",
            "Should this specific data source use Import mode or DirectQuery?",
        ],
    ),
    dict(
        id="data-modeling-relationships",
        title="Data Modeling & Relationships",
        hook="A wrong relationship (or a missing one) is the single most common reason a Power BI number 'just looks wrong' — get this right and half your DAX problems disappear.",
        explanation=(
            "A relationship connects two tables through a shared column, most often a one-to-many relationship "
            "from a dimension table (like `Customers`, one row per customer) to a fact table (like `Orders`, "
            "many rows per customer). Power BI uses these relationships to automatically filter related tables "
            "when you slice by any field — pick a customer in a slicer, and their orders filter automatically "
            "because the relationship propagates that filter.\n\n"
            "Relationships have a cardinality (one-to-many is the healthiest default) and a cross-filter "
            "direction (single, the default, versus bidirectional). Bidirectional filtering looks convenient but "
            "can quietly create ambiguous filter paths in more complex models, which is why experienced modelers "
            "reach for it deliberately rather than by default.\n\n"
            "A star schema — one central fact table surrounded by several dimension tables, each connected "
            "directly to the fact table rather than to each other — is the standard, recommended shape for a "
            "Power BI model, deliberately different from a fully normalized relational database schema. This "
            "shape keeps filter propagation simple and predictable, and DAX's engine is specifically optimized "
            "to perform well against it."
        ),
        deep_dive=(
            "A snowflake schema (where dimension tables are further normalized into sub-dimension tables, "
            "connected to each other rather than all connecting directly to the fact table) is technically "
            "possible in Power BI but generally discouraged compared to a flatter star schema — the extra "
            "normalization that helps a transactional database saves storage space, but it adds unnecessary "
            "relationship hops that complicate DAX and can hurt query performance in an analytical model where "
            "storage is comparatively cheap and query simplicity matters more.\n\n"
            "Many-to-many relationships (where neither side has a unique key matching the relationship column) "
            "require special handling — either an intermediate bridge table breaking the relationship into two "
            "proper one-to-many relationships, or Power BI's native many-to-many relationship support (which "
            "carries its own performance and ambiguity considerations) — a naive direct many-to-many "
            "relationship is a common source of unexpectedly inflated totals.\n\n"
            "Inactive relationships (a second relationship between two tables, marked inactive since only one "
            "relationship between a pair of tables can be active by default) can be explicitly activated within "
            "a specific DAX measure using `USERELATIONSHIP()`, which is the standard technique for modeling "
            "something like an order having both an 'order date' and a 'ship date' relationship to the same "
            "date dimension table, using whichever one a specific measure needs."
        ),
        code=dict(
            lang="text",
            label="A simple star schema",
            src=(
                "Dim_Customer (CustomerID, Name, Region)\n"
                "Dim_Product  (ProductID, Category, Price)\n"
                "Dim_Date     (Date, Year, Month, Quarter)\n"
                "        \\         |         /\n"
                "         \\        |        /\n"
                "        Fact_Sales (OrderID, CustomerID, ProductID, Date, Amount)\n\n"
                "Each Dim table has a 1:many relationship into Fact_Sales."
            ),
        ),
        advanced_code=dict(
            lang="text",
            label="Using an inactive relationship with USERELATIONSHIP",
            src=(
                "-- Fact_Sales has TWO date relationships to Dim_Date:\n"
                "-- OrderDate (active) and ShipDate (inactive)\n\n"
                "Shipped Revenue by Ship Date =\n"
                "CALCULATE(\n"
                "    [Total Revenue],\n"
                "    USERELATIONSHIP(Fact_Sales[ShipDate], Dim_Date[Date])\n"
                ")\n"
                "-- Activates the ShipDate relationship for THIS measure only"
            ),
        ),
        example=(
            "Filtering a report to `Region = East Africa` on the customer dimension automatically filters the "
            "sales fact table down to only orders from customers in that region, purely because of the "
            "relationship — no DAX filtering logic needed for that basic case."
        ),
        best_practices=[
            "Keep relationships single-directional unless you have a specific, well-understood reason to make one bidirectional.",
            "Build a dedicated Date dimension table rather than relying on dates buried inside the fact table, especially for time-intelligence functions.",
            "Hide foreign key columns from the report view once relationships are built — they're for modeling, not for dragging onto visuals.",
            "Prefer a flat star schema over a snowflake schema for analytical models, even if it means some denormalization compared to a transactional database design.",
        ],
        pitfalls=[
            "Making every relationship bidirectional 'to be safe,' which often produces ambiguous or inflated totals instead.",
            "Building relationships on a text column with inconsistent casing or whitespace, silently dropping unmatched rows.",
            "Creating a naive direct many-to-many relationship without a bridge table, inflating totals unexpectedly.",
        ],
        glossary=[
            dict(term="Star schema", definition="A model shape with one central fact table connected directly to several surrounding dimension tables, the recommended default for Power BI."),
            dict(term="Snowflake schema", definition="A further-normalized variant where dimension tables connect to sub-dimension tables rather than all connecting directly to the fact table, generally discouraged in Power BI."),
            dict(term="USERELATIONSHIP", definition="A DAX function that activates a specific inactive relationship for the scope of one measure's calculation."),
            dict(term="Bridge table", definition="An intermediate table used to properly model a many-to-many relationship as two one-to-many relationships."),
        ],
        faq=[
            dict(q="What's the difference between single and bidirectional cross-filtering?", a="Single (the default) lets a dimension table's filter propagate to the fact table, but not the reverse. Bidirectional also lets the fact table's filter propagate back to the dimension table — convenient in specific cases, but can create ambiguous filter paths in more complex models with multiple related tables."),
            dict(q="Why do I need a separate Date table instead of using the dates already in my Sales table?", a="A dedicated Date dimension table gives you a complete, gap-free calendar to relate to, which is required for Power BI's time intelligence DAX functions (YTD, same period last year, etc.) to work correctly, and lets multiple fact tables share one consistent date dimension."),
            dict(q="How do I diagnose an ambiguous relationship path in my model?", a="Power BI will often flag this directly with an error when you try to create a relationship that would create ambiguity. The Model view's diagram layout, showing all relationships visually, is the best tool for spotting unintended bidirectional paths or redundant relationships causing the issue."),
        ],
        quiz=[
            dict(
                question="Why is a star schema generally preferred over a snowflake schema in Power BI?",
                options=["Star schemas use less storage always", "Star schemas keep filter propagation simpler and are optimized for by the DAX engine", "Snowflake schemas aren't supported at all", "There's no real difference"],
                correct=1,
                explanation="A flatter star schema keeps relationship paths short and filter propagation predictable, and Power BI's engine is specifically optimized to perform well against this shape, unlike the extra relationship hops a snowflake schema introduces.",
            ),
        ],
        prompts=[
            "What's the difference between single and bidirectional cross-filtering?",
            "Why do I need a separate Date table instead of using the dates already in my Sales table?",
            "How do I diagnose an ambiguous relationship path in my model?",
            "How would I model a many-to-many relationship correctly in Power BI?",
        ],
    ),
    dict(
        id="dax-fundamentals",
        title="DAX Fundamentals: Measures vs. Calculated Columns",
        hook="The single most common DAX bug is using a calculated column when you needed a measure, or the reverse — they look similar but behave completely differently.",
        explanation=(
            "DAX (Data Analysis Expressions) is Power BI's formula language. A calculated column computes a "
            "value row-by-row at data refresh time and is stored physically in the model, like adding a column "
            "in Excel. A measure computes its value dynamically at query time, based on whatever filter context "
            "is currently applied (the slicers, the row/column in the visual) — it's never stored, always "
            "recalculated live.\n\n"
            "This distinction matters because measures automatically respond to filtering and aggregate "
            "correctly across any grouping, while calculated columns don't — a calculated column computed as "
            "`Price * Quantity` per row can't turn itself into a correct grand total the way a `SUM()` measure "
            "can. As a rule of thumb: if the calculation should change depending on what's selected on the "
            "report, it should almost always be a measure.\n\n"
            "Implicit measures (created automatically when you drag a numeric column directly onto a visual "
            "and Power BI auto-aggregates it) are convenient for quick exploration but generally discouraged "
            "for production reports, since they're harder to reuse consistently across multiple visuals and "
            "don't show up in a central, auditable list of defined measures the way explicit measures do."
        ),
        deep_dive=(
            "Variables (`VAR`) inside a measure are evaluated exactly once, in the original context the "
            "measure was called in, and then reused as many times as needed within that measure's formula — "
            "this both improves readability (naming intermediate results) and can meaningfully improve "
            "performance by avoiding recomputing the same sub-expression multiple times within one measure.\n\n"
            "DAX has both row context (present inside calculated columns and iterator functions like SUMX, "
            "meaning 'you're currently evaluating this specific row') and filter context (present in measures, "
            "meaning 'these are the currently active filters from slicers/visuals'), and understanding which "
            "context you're in at any point in a formula is the single most important mental model for writing "
            "correct DAX — many confusing DAX bugs trace back to a misunderstanding of which context applies "
            "at a given point in the expression.\n\n"
            "`DIVIDE(numerator, denominator, alternate_result)` is preferred over the plain `/` operator "
            "specifically because it handles division by zero gracefully, returning the alternate result "
            "(default blank) instead of an error that would otherwise break the entire visual it's used in."
        ),
        code=dict(
            lang="text",
            label="Calculated column vs. measure",
            src=(
                "-- Calculated column: one value per row, computed at refresh\n"
                "Line Total = Fact_Sales[Quantity] * Fact_Sales[UnitPrice]\n\n"
                "-- Measure: one value per filter context, computed at query time\n"
                "Total Revenue = SUM(Fact_Sales[Quantity] * Fact_Sales[UnitPrice])\n\n"
                "-- Measure using VAR for readability\n"
                "Avg Order Value =\n"
                "VAR TotalRevenue = [Total Revenue]\n"
                "VAR OrderCount = DISTINCTCOUNT(Fact_Sales[OrderID])\n"
                "RETURN DIVIDE(TotalRevenue, OrderCount)"
            ),
        ),
        advanced_code=dict(
            lang="text",
            label="Row context vs. filter context, demonstrated",
            src=(
                "-- Calculated column: ROW CONTEXT -- 'this specific row'\n"
                "Margin % = DIVIDE(\n"
                "    Fact_Sales[Revenue] - Fact_Sales[Cost],\n"
                "    Fact_Sales[Revenue]\n"
                ")   -- computed independently for every row\n\n"
                "-- Measure: FILTER CONTEXT -- 'whatever is currently filtered/sliced'\n"
                "Total Margin % =\n"
                "DIVIDE(\n"
                "    SUM(Fact_Sales[Revenue]) - SUM(Fact_Sales[Cost]),\n"
                "    SUM(Fact_Sales[Revenue])\n"
                ")   -- recalculated for whatever rows are currently in scope"
            ),
        ),
        example=(
            "A KPI card showing 'Total Revenue' that's wired to a calculated column will show the sum of a "
            "column that was already 'locked in' at refresh time, ignoring any slicer selections, while the same "
            "card wired to a measure recalculates correctly the instant a user filters by region or date."
        ),
        best_practices=[
            "Default to measures for anything that will be aggregated, filtered, or shown in a visual — reserve calculated columns for values you need to slice/group BY.",
            "Use `VAR` to name intermediate results inside a measure; it avoids recomputing the same sub-expression twice and makes complex DAX readable.",
            "Wrap division in `DIVIDE()` instead of the `/` operator — it handles divide-by-zero gracefully and won't error out your visual.",
            "Prefer explicit, named measures over relying on implicit auto-aggregated measures for anything used in more than one place.",
        ],
        pitfalls=[
            "Writing a calculated column when a measure was needed, then being confused why totals don't match the visual's context.",
            "Using `/` instead of `DIVIDE()` and having a report crash or show an error when a denominator happens to be zero.",
            "Confusing row context and filter context, leading to formulas that behave correctly at one grouping level but wrong at another.",
        ],
        glossary=[
            dict(term="Measure", definition="A DAX calculation computed dynamically at query time based on the current filter context, never stored."),
            dict(term="Calculated column", definition="A DAX calculation computed once per row at data refresh time and stored physically in the model."),
            dict(term="Row context", definition="The 'currently evaluating this specific row' context present in calculated columns and iterator functions like SUMX."),
            dict(term="Filter context", definition="The set of currently active filters (from slicers, visuals, or CALCULATE) that a measure's calculation responds to."),
        ],
        faq=[
            dict(q="Is this specific calculation a measure or a calculated column: year-over-year growth percentage?", a="A measure — it needs to respond dynamically to whatever date range or grouping is currently selected on the report, which is exactly what a measure (recalculated per filter context) provides and a calculated column (fixed per row at refresh) cannot."),
            dict(q="Rewrite this nested DAX expression using VAR for readability.", a="Identify each distinct sub-calculation being repeated or that would benefit from a clear name, assign each to a VAR, and use RETURN with the final expression referencing those named variables instead of repeating the full sub-expressions inline."),
            dict(q="Explain filter context versus row context with a concrete DAX example.", a="A calculated column like `Margin = Revenue - Cost` operates in row context, computing independently for each row. A measure like `Total Margin = SUM(Revenue) - SUM(Cost)` operates in filter context, recalculating based on whatever rows are currently visible given the active slicers and visual groupings."),
        ],
        quiz=[
            dict(
                question="Why does DIVIDE() get recommended over the plain / operator in DAX?",
                options=["DIVIDE is faster in every case", "DIVIDE handles division by zero gracefully instead of erroring out the visual", "The / operator doesn't exist in DAX", "DIVIDE only works inside calculated columns"],
                correct=1,
                explanation="DIVIDE() returns a specified alternate result (blank by default) when the denominator is zero, avoiding the error that the plain / operator would produce and that would otherwise break the entire visual using it.",
            ),
        ],
        prompts=[
            "Is this specific calculation a measure or a calculated column: year-over-year growth percentage?",
            "Rewrite this nested DAX expression using VAR for readability.",
            "Explain filter context versus row context with a concrete DAX example.",
            "Why is DIVIDE() preferred over the plain division operator in DAX?",
        ],
    ),
    dict(
        id="context-transition",
        title="Context Transition & CALCULATE",
        hook="This is the single trickiest DAX concept, and also the most powerful — most 'why is my total wrong at this level' bugs trace straight back to it.",
        explanation=(
            "DAX has two kinds of context: row context (you're inside a specific row, like in a calculated "
            "column or an iterator function like `SUMX`) and filter context (the current combination of slicers, "
            "rows, and columns in a visual). `CALCULATE()` is the function that changes filter context, and using "
            "it inside a row context — such as inside `SUMX` — triggers something called context transition: the "
            "current row is turned into an equivalent filter, as if you'd clicked that exact row's values as a "
            "slicer.\n\n"
            "This is powerful because it lets you compute something 'as if only this row existed,' which is "
            "exactly what running totals, rankings, and row-level comparisons need. It's also the source of most "
            "confusing bugs, because it happens implicitly any time `CALCULATE` (or a measure, which implicitly "
            "wraps in `CALCULATE`) is called inside row context.\n\n"
            "`CALCULATE()`'s second and later arguments are filter modifiers — additional conditions (`CALCULATE"
            "([Total Revenue], Dim_Product[Category] = \"Electronics\")`) that get combined with whatever filter "
            "context already exists, rather than replacing it entirely, unless you specifically use `ALL()` or "
            "similar functions to remove existing filters first."
        ),
        deep_dive=(
            "Every plain measure reference (like `[Total Revenue]`) inside another DAX expression is implicitly "
            "wrapped in `CALCULATE()` by DAX itself — this is why context transition can happen even when you "
            "never typed the word `CALCULATE` explicitly; referencing a measure from inside an iterator triggers "
            "it just the same as an explicit `CALCULATE()` call would.\n\n"
            "`ALL()` removes filters from a table or column entirely, which combined with `CALCULATE` is the "
            "standard technique for computing a 'percent of total' style measure — calculating a grand total "
            "that deliberately ignores the currently active filters (like the current row's category) while "
            "keeping the row-level or currently-filtered value to compare it against.\n\n"
            "Understanding context transition well enough to predict its behavior generally comes from tracing "
            "through a formula step by step at a specific grouping level (like a single product row versus a "
            "category subtotal versus the grand total) and asking, at each point, exactly what filter context "
            "is active — a mental exercise experienced DAX authors do routinely when debugging an unexpected "
            "number."
        ),
        code=dict(
            lang="text",
            label="Context transition inside SUMX",
            src=(
                "Total Margin =\n"
                "SUMX(\n"
                "    Fact_Sales,\n"
                "    VAR RowCost =\n"
                "        CALCULATE(SUM(Fact_Costs[Cost]))  -- context transition happens here\n"
                "    RETURN Fact_Sales[Revenue] - RowCost\n"
                ")\n\n"
                "-- CALCULATE turns the current Fact_Sales row into filters,\n"
                "-- so Fact_Costs[Cost] is filtered to match that row's context."
            ),
        ),
        advanced_code=dict(
            lang="text",
            label="Percent of total using ALL() to remove filters",
            src=(
                "% of Category Total =\n"
                "VAR CurrentRowRevenue = [Total Revenue]\n"
                "VAR CategoryTotal =\n"
                "    CALCULATE(\n"
                "        [Total Revenue],\n"
                "        ALL(Dim_Product[ProductName])   -- ignore product filter, keep category\n"
                "    )\n"
                "RETURN DIVIDE(CurrentRowRevenue, CategoryTotal)"
            ),
        ),
        example=(
            "A 'Rank within Category' measure works by wrapping a row's sales total in `CALCULATE`, which forces "
            "the current product's category to become an active filter, letting the measure compare that one "
            "product against only its category peers instead of the whole table."
        ),
        best_practices=[
            "Assign anything you don't want re-filtered to a VAR before calling CALCULATE, since VARs are evaluated once in the original context.",
            "Remember that every plain measure reference (like `[Total Revenue]`) is implicitly wrapped in CALCULATE — context transition can happen even without typing CALCULATE explicitly.",
            "Test measures at multiple grouping levels (product, category, grand total) — context transition bugs often only appear at one specific level.",
            "Use ALL() deliberately and narrowly (on specific columns, not entire tables, when possible) to avoid accidentally removing more filter context than intended.",
        ],
        pitfalls=[
            "Assuming a measure referenced inside an iterator behaves like a simple row-by-row value, forgetting it silently triggers CALCULATE.",
            "Nesting CALCULATE calls without understanding which filters are being layered versus replaced, producing numbers that are subtly wrong.",
            "Using ALL() on an entire table when only a specific column's filter needed to be removed, unintentionally clearing more context than intended.",
        ],
        glossary=[
            dict(term="Context transition", definition="The conversion of row context into an equivalent filter context, triggered whenever CALCULATE (explicit or implicit) is called inside row context."),
            dict(term="CALCULATE", definition="The DAX function that modifies filter context, combining new filter arguments with whatever context already exists."),
            dict(term="ALL()", definition="A DAX function that removes existing filters from a specified table or column, commonly used for percent-of-total calculations."),
        ],
        faq=[
            dict(q="Explain context transition using a step-by-step trace through this SUMX example.", a="SUMX iterates row by row over Fact_Sales. For each row, the VAR's CALCULATE call triggers context transition: the current row's column values become an implicit filter, so SUM(Fact_Costs[Cost]) is evaluated as if filtered to match that specific row's context, giving a per-row cost even though Fact_Costs is a separate table."),
            dict(q="Why does referencing a measure inside SUMX behave differently than referencing a column?", a="A measure reference is implicitly wrapped in CALCULATE by DAX, which triggers context transition when used inside row context (like inside SUMX) — a plain column reference doesn't trigger this, since it's just reading that row's stored value directly, no filter context change involved."),
            dict(q="Write a DAX measure that ranks products within their category.", a="Use CALCULATE combined with RANKX, restricting the ranking's comparison set to the current category using a filter like `ALLEXCEPT(Dim_Product, Dim_Product[Category])` so each product is only ranked against others in the same category."),
        ],
        quiz=[
            dict(
                question="What triggers context transition in DAX?",
                options=["Any SUM() function call", "CALCULATE (explicit or implicit via a measure reference) used inside row context", "Adding a slicer to a report", "Creating a relationship between two tables"],
                correct=1,
                explanation="Context transition happens specifically when CALCULATE runs inside row context, converting the current row's values into an equivalent filter — this happens explicitly with a written CALCULATE call, or implicitly whenever a measure is referenced inside an iterator.",
            ),
        ],
        prompts=[
            "Explain context transition using a step-by-step trace through this SUMX example.",
            "Why does referencing a measure inside SUMX behave differently than referencing a column?",
            "Write a DAX measure that ranks products within their category.",
            "How does ALL() interact with CALCULATE for a percent-of-total calculation?",
        ],
    ),
    dict(
        id="time-intelligence",
        title="Time Intelligence: YoY, MTD & Rolling Averages",
        hook="Comparing 'this period vs. last period' is one of the most common business questions — and DAX has purpose-built functions for it that beat writing the date math by hand.",
        explanation=(
            "Time intelligence functions (`TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATEADD`, `DATESINPERIOD`) let you "
            "compute period comparisons without manually filtering date ranges. They rely on having a proper "
            "Date dimension table marked as a date table in the model, with one row per calendar date and no "
            "gaps — without that, these functions produce silently wrong results.\n\n"
            "The general pattern is: take a base measure (like `Total Revenue`), and wrap it in a time "
            "intelligence function inside `CALCULATE` to shift or accumulate the filter context over the date "
            "dimension. This composability means you write the aggregation logic once and reuse it across many "
            "time-based variants.\n\n"
            "`SAMEPERIODLASTYEAR` and `DATEADD` both shift a date range back in time, but differ subtly: "
            "`SAMEPERIODLASTYEAR` specifically shifts back exactly one year, while `DATEADD` is more general "
            "and can shift by any number of days, months, quarters, or years, making it the more flexible tool "
            "once you need something beyond a straightforward year-over-year comparison."
        ),
        deep_dive=(
            "Storing and comparing datetimes as naive local time is a common source of subtle bugs once an "
            "application spans multiple timezones or servers — the standard, strongly recommended practice is "
            "to store all datetimes in UTC internally and convert to a specific local timezone only at the "
            "point of display to a user (this general principle from software applies equally to how a Power "
            "BI model's Date table should be built consistently, avoiding mixed timezone assumptions across "
            "data sources).\n\n"
            "`DATESYTD`, `DATESMTD`, and `DATESQTD` return a table of dates from the start of the year/month/"
            "quarter through the last date in the current filter context, which is what `TOTALYTD` (and "
            "similar functions) use internally — understanding that these are really returning a *table of "
            "dates* that then gets used to filter a `CALCULATE` clarifies what's actually happening rather "
            "than treating these functions as unexplainable magic.\n\n"
            "For non-standard fiscal years (a fiscal year not starting January 1st), most time intelligence "
            "functions accept an optional year-end date parameter (`TOTALYTD([Total Revenue], Dim_Date[Date], "
            "\"06/30\")` for a fiscal year ending in June), letting the same functions handle organizations "
            "with a fiscal calendar different from the standard calendar year."
        ),
        code=dict(
            lang="text",
            label="Common time-intelligence measures",
            src=(
                "Revenue YTD =\n"
                "CALCULATE([Total Revenue], DATESYTD(Dim_Date[Date]))\n\n"
                "Revenue Same Period Last Year =\n"
                "CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))\n\n"
                "Revenue YoY % =\n"
                "VAR Current = [Total Revenue]\n"
                "VAR PriorYear = [Revenue Same Period Last Year]\n"
                "RETURN DIVIDE(Current - PriorYear, PriorYear)"
            ),
        ),
        advanced_code=dict(
            lang="text",
            label="A rolling 3-month average, and a fiscal-year YTD",
            src=(
                "Rolling 3-Month Avg Revenue =\n"
                "AVERAGEX(\n"
                "    DATESINPERIOD(Dim_Date[Date], MAX(Dim_Date[Date]), -3, MONTH),\n"
                "    [Total Revenue]\n"
                ")\n\n"
                "-- Fiscal year ending June 30\n"
                "Revenue Fiscal YTD =\n"
                "CALCULATE([Total Revenue], DATESYTD(Dim_Date[Date], \"06/30\"))"
            ),
        ),
        example=(
            "An executive dashboard showing 'Revenue is up 12% YoY' is powered by exactly the pattern above — one "
            "base measure, one time-shifted variant, and a DIVIDE to turn the difference into a clean percentage "
            "that updates automatically as the report's date filter changes."
        ),
        best_practices=[
            "Mark a proper Date table as the model's official date table (Model view → right-click → Mark as Date Table) before using any time intelligence function.",
            "Make sure the Date table has no gaps and spans the full range of your fact data, including into the current, incomplete period.",
            "Build YoY/MTD measures as small, composable layers on top of a single base measure rather than duplicating aggregation logic in each one.",
            "Pass the fiscal year-end parameter to time intelligence functions explicitly for any organization not using a standard January-start calendar year.",
        ],
        pitfalls=[
            "Using time intelligence functions against a date column that has gaps or doesn't cover the full fact table's range.",
            "Forgetting to mark the Date table explicitly, which causes some time intelligence functions to behave inconsistently.",
            "Confusing SAMEPERIODLASTYEAR (always exactly one year back) with DATEADD (flexible shift amount) and using the wrong one for a non-annual comparison.",
        ],
        glossary=[
            dict(term="Date table", definition="A dedicated table with one row per calendar date and no gaps, explicitly marked as the model's date table to enable time intelligence functions."),
            dict(term="SAMEPERIODLASTYEAR", definition="A DAX time intelligence function returning the same date range shifted back exactly one year."),
            dict(term="DATEADD", definition="A more general DAX time intelligence function shifting a date range by any number of days, months, quarters, or years."),
        ],
        faq=[
            dict(q="What exactly does marking a table as a Date Table change in the model?", a="It tells Power BI's engine that this table represents a proper, continuous calendar, enabling full and correct support for time intelligence functions — without this explicit marking, some time intelligence functions may not work correctly or at all."),
            dict(q="Write a rolling 3-month average measure in DAX.", a="Use AVERAGEX over DATESINPERIOD(Dim_Date[Date], MAX(Dim_Date[Date]), -3, MONTH), which builds a rolling 3-month window ending at the current filter context's last date, then averages the base measure across that window."),
            dict(q="Why did my YTD measure return a blank for the current month?", a="Common causes: the Date table doesn't extend far enough to cover the current period, there's a gap in the date sequence, or the table hasn't been explicitly marked as the model's date table — check all three."),
        ],
        quiz=[
            dict(
                question="What's required before time intelligence DAX functions will work correctly?",
                options=["A bidirectional relationship on every table", "A dedicated, gap-free Date table explicitly marked as the model's date table", "DirectQuery mode must be enabled", "Every measure must use VAR"],
                correct=1,
                explanation="Time intelligence functions depend on a proper, continuous calendar table marked as the date table — without it, results can be silently incorrect or the functions may not work at all.",
            ),
        ],
        prompts=[
            "What exactly does marking a table as a Date Table change in the model?",
            "Write a rolling 3-month average measure in DAX.",
            "Why did my YTD measure return a blank for the current month?",
            "How do I adapt a YTD measure for a fiscal year that doesn't start in January?",
        ],
    ),
]