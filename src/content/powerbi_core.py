"""Power BI subtopics."""

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
            "after both are solid does building visuals become the fast, almost mechanical last step."
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
        example=(
            "A sales dashboard that looks broken (totals don't add up, dates display wrong) is almost always a "
            "modeling or query problem wearing a visualization costume — fixing a wrong data type in Power Query "
            "or a missing relationship in the model resolves it, not tweaking the chart itself."
        ),
        best_practices=[
            "Fix data quality issues in Power Query, not with DAX workarounds in the model — clean once at the source, not repeatedly in every measure.",
            "Build a star schema (one fact table, several dimension tables) rather than one giant flat table — it's dramatically easier to write correct DAX against.",
            "Name your queries, tables, and measures clearly and consistently from the start; renaming later breaks every visual referencing the old name.",
        ],
        pitfalls=[
            "Importing a huge flat Excel export as-is instead of splitting it into fact and dimension tables during Power Query.",
            "Applying the same cleaning step manually every time you refresh instead of encoding it once in the Power Query steps.",
        ],
        prompts=[
            "Why does a star schema make DAX easier to write than a flat table?",
            "Walk through cleaning a messy CSV export in Power Query step by step.",
            "What's the difference between a calculated column and a measure, and when do I use each?",
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
            "reach for it deliberately rather than by default."
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
        example=(
            "Filtering a report to `Region = East Africa` on the customer dimension automatically filters the "
            "sales fact table down to only orders from customers in that region, purely because of the "
            "relationship — no DAX filtering logic needed for that basic case."
        ),
        best_practices=[
            "Keep relationships single-directional unless you have a specific, well-understood reason to make one bidirectional.",
            "Build a dedicated Date dimension table rather than relying on dates buried inside the fact table, especially for time-intelligence functions.",
            "Hide foreign key columns from the report view once relationships are built — they're for modeling, not for dragging onto visuals.",
        ],
        pitfalls=[
            "Making every relationship bidirectional 'to be safe,' which often produces ambiguous or inflated totals instead.",
            "Building relationships on a text column with inconsistent casing or whitespace, silently dropping unmatched rows.",
        ],
        prompts=[
            "What's the difference between single and bidirectional cross-filtering?",
            "Why do I need a separate Date table instead of using the dates already in my Sales table?",
            "How do I diagnose an ambiguous relationship path in my model?",
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
            "report, it should almost always be a measure."
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
        example=(
            "A KPI card showing 'Total Revenue' that's wired to a calculated column will show the sum of a "
            "column that was already 'locked in' at refresh time, ignoring any slicer selections, while the same "
            "card wired to a measure recalculates correctly the instant a user filters by region or date."
        ),
        best_practices=[
            "Default to measures for anything that will be aggregated, filtered, or shown in a visual — reserve calculated columns for values you need to slice/group BY.",
            "Use `VAR` to name intermediate results inside a measure; it avoids recomputing the same sub-expression twice and makes complex DAX readable.",
            "Wrap division in `DIVIDE()` instead of the `/` operator — it handles divide-by-zero gracefully and won't error out your visual.",
        ],
        pitfalls=[
            "Writing a calculated column when a measure was needed, then being confused why totals don't match the visual's context.",
            "Using `/` instead of `DIVIDE()` and having a report crash or show an error when a denominator happens to be zero.",
        ],
        prompts=[
            "Is this specific calculation a measure or a calculated column: year-over-year growth percentage?",
            "Rewrite this nested DAX expression using VAR for readability.",
            "Explain filter context versus row context with a concrete DAX example.",
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
            "wraps in `CALCULATE`) is called inside row context."
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
        example=(
            "A 'Rank within Category' measure works by wrapping a row's sales total in `CALCULATE`, which forces "
            "the current product's category to become an active filter, letting the measure compare that one "
            "product against only its category peers instead of the whole table."
        ),
        best_practices=[
            "Assign anything you don't want re-filtered to a VAR before calling CALCULATE, since VARs are evaluated once in the original context.",
            "Remember that every plain measure reference (like `[Total Revenue]`) is implicitly wrapped in CALCULATE — context transition can happen even without typing CALCULATE explicitly.",
            "Test measures at multiple grouping levels (product, category, grand total) — context transition bugs often only appear at one specific level.",
        ],
        pitfalls=[
            "Assuming a measure referenced inside an iterator behaves like a simple row-by-row value, forgetting it silently triggers CALCULATE.",
            "Nesting CALCULATE calls without understanding which filters are being layered versus replaced, producing numbers that are subtly wrong.",
        ],
        prompts=[
            "Explain context transition using a step-by-step trace through this SUMX example.",
            "Why does referencing a measure inside SUMX behave differently than referencing a column?",
            "Write a DAX measure that ranks products within their category.",
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
            "time-based variants."
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
        example=(
            "An executive dashboard showing 'Revenue is up 12% YoY' is powered by exactly the pattern above — one "
            "base measure, one time-shifted variant, and a DIVIDE to turn the difference into a clean percentage "
            "that updates automatically as the report's date filter changes."
        ),
        best_practices=[
            "Mark a proper Date table as the model's official date table (Model view → right-click → Mark as Date Table) before using any time intelligence function.",
            "Make sure the Date table has no gaps and spans the full range of your fact data, including into the current, incomplete period.",
            "Build YoY/MTD measures as small, composable layers on top of a single base measure rather than duplicating aggregation logic in each one.",
        ],
        pitfalls=[
            "Using time intelligence functions against a date column that has gaps or doesn't cover the full fact table's range.",
            "Forgetting to mark the Date table explicitly, which causes some time intelligence functions to behave inconsistently.",
        ],
        prompts=[
            "What exactly does marking a table as a Date Table change in the model?",
            "Write a rolling 3-month average measure in DAX.",
            "Why did my YTD measure return a blank for the current month?",
        ],
    ),
]
