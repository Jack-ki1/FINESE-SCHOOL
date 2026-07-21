"""Data Visualization subtopics — enriched schema."""

SUBTOPICS = [
    dict(
        id="choosing-the-right-chart",
        title="Choosing the Right Chart Type",
        hook="Most bad charts aren't badly styled — they're the wrong chart type for the comparison being made, and no amount of color fixes that.",
        explanation=(
            "Every chart type is optimized for a specific kind of visual comparison, and the human visual system "
            "is measurably better at some comparisons than others. Position along a common axis (a bar chart, a "
            "dot plot) is the easiest comparison for people to make accurately. Length is next. Angle and area — "
            "the building blocks of a pie chart — are among the hardest, which is why a pie chart with more than "
            "three or four slices routinely gets misread.\n\n"
            "The chart choice should follow directly from the question being answered: comparing categories "
            "wants a bar chart, showing change over time wants a line chart, showing the relationship between "
            "two numeric variables wants a scatter plot, and showing distribution wants a histogram or box plot. "
            "Picking the chart first and forcing the data to fit it is backward — the question should choose the chart.\n\n"
            "This ranking of visual perception accuracy comes from foundational research by statisticians "
            "William Cleveland and Robert McGill in the 1980s, who empirically tested how accurately people "
            "could judge different visual encodings — their findings still directly inform modern chart "
            "design guidance and explain, with actual measured evidence, why some intuitive-seeming chart "
            "choices (like pie charts for many categories) reliably underperform simpler alternatives."
        ),
        deep_dive=(
            "Small multiples (a grid of many small, identically-scaled charts, one per category or time "
            "period) are frequently a superior alternative to cramming many series onto one overcrowded chart "
            "— they let a viewer compare shapes and patterns across categories at a glance, using the "
            "consistent, repeated layout to make comparison easy, rather than trying to decode overlapping "
            "lines or bars in different colors on a single crowded chart.\n\n"
            "Dual-axis charts (two different y-axes on the same chart, often for two variables with very "
            "different scales) are widely considered a design anti-pattern in most data visualization "
            "guidance, since the choice of which axis's scale to use can visually imply a relationship or "
            "correlation between the two series that isn't actually present in the underlying data — a "
            "genuine risk of misleading the viewer, intentionally or not.\n\n"
            "The right chart also depends on audience and context, not just the data's shape — a chart for a "
            "quick internal Slack update can be simpler and rougher than one going into a polished external "
            "report, and a chart meant to be read in five seconds on a dashboard needs a much clearer, "
            "simpler visual hierarchy than one accompanying a detailed written analysis where the reader has "
            "more time to study it."
        ),
        code=dict(
            lang="python",
            label="Same data, chart chosen to fit the question",
            src=(
                "import plotly.express as px\n\n"
                "# Question: how do categories compare? -> bar chart, sorted\n"
                "fig1 = px.bar(df.sort_values(\"revenue\"), x=\"revenue\", y=\"region\", orientation=\"h\")\n\n"
                "# Question: how did revenue change over time? -> line chart\n"
                "fig2 = px.line(df_ts, x=\"month\", y=\"revenue\")\n\n"
                "# Question: is there a relationship between ad spend and revenue? -> scatter\n"
                "fig3 = px.scatter(df, x=\"ad_spend\", y=\"revenue\", trendline=\"ols\")"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Small multiples instead of one overcrowded chart",
            src=(
                "import plotly.express as px\n\n"
                "# Instead of one chart with 8 overlapping region lines:\n"
                "fig = px.line(\n"
                "    df, x=\"month\", y=\"revenue\", facet_col=\"region\", facet_col_wrap=4\n"
                ")\n"
                "# Produces a grid of small, identically-scaled charts, one per region --\n"
                "# far easier to compare shapes than 8 overlapping colored lines"
            ),
        ),
        example=(
            "A dashboard replacing a seven-slice pie chart of 'traffic source' with a sorted horizontal bar chart "
            "made the exact same underlying data readable at a glance instead of requiring the viewer to compare "
            "wedge angles — a purely structural fix, with zero new data or styling."
        ),
        best_practices=[
            "Start from the question ('compare categories', 'show a trend', 'show a relationship') and let it determine the chart type.",
            "Sort categorical bar charts by value rather than alphabetically, unless the category order itself carries meaning (like days of the week).",
            "Reserve pie charts for two or three slices at most, if you use them at all — a bar chart almost always communicates the same comparison more clearly.",
            "Consider small multiples instead of a single overcrowded chart when comparing more than 4-5 series.",
        ],
        pitfalls=[
            "Defaulting to a pie chart out of habit for any categorical breakdown, regardless of how many categories there are.",
            "Using a line chart to connect points that aren't actually sequential or continuous, implying a trend that doesn't exist.",
            "Using a dual-axis chart that visually implies a correlation between two series that isn't actually present in the data.",
        ],
        glossary=[
            dict(term="Cleveland-McGill hierarchy", definition="An empirically-derived ranking of how accurately people perceive different visual encodings (position, length, angle, area, color), foundational to modern chart design guidance."),
            dict(term="Small multiples", definition="A grid of many small, identically-scaled charts, one per category, making comparison across categories easier than overlaying them on one chart."),
            dict(term="Dual-axis chart", definition="A chart with two different y-axis scales, often considered a design anti-pattern since it can visually imply a false relationship between two series."),
        ],
        faq=[
            dict(q="What chart type fits comparing five products' monthly sales trends?", a="A line chart with one line per product (if 5 is manageable to distinguish by color) or a small-multiples grid of 5 individual line charts if distinguishing overlapping lines becomes visually cluttered."),
            dict(q="Why is a pie chart considered a poor choice for more than a few categories?", a="People are measurably less accurate at comparing angles and areas than they are at comparing position or length (per the Cleveland-McGill research), so a pie chart with many slices makes it hard to judge relative sizes precisely, especially for similarly-sized slices."),
            dict(q="Suggest a better chart than a pie chart for this survey response breakdown.", a="A sorted horizontal bar chart almost always communicates the same categorical breakdown more clearly, letting viewers compare bar lengths precisely instead of estimating wedge angles."),
        ],
        quiz=[
            dict(
                question="According to the Cleveland-McGill research, which visual encoding is generally perceived MOST accurately?",
                options=["Angle", "Area", "Position along a common scale", "Color hue"],
                correct=2,
                explanation="Position along a common, aligned scale (like bars starting from the same baseline) is the most accurately perceived encoding, which is why bar and dot charts tend to outperform pie charts for precise comparisons.",
            ),
        ],
        prompts=[
            "What chart type fits comparing five products' monthly sales trends?",
            "Why is a pie chart considered a poor choice for more than a few categories?",
            "Suggest a better chart than a pie chart for this survey response breakdown.",
            "When should I use small multiples instead of one combined chart?",
        ],
    ),
    dict(
        id="matplotlib-seaborn-basics",
        title="Matplotlib & Seaborn Fundamentals",
        hook="Matplotlib is the low-level engine nearly every Python plotting library sits on top of — Seaborn is the same engine with statistically-aware defaults baked in.",
        explanation=(
            "Matplotlib gives full control over every element of a figure — axes, ticks, legends, colors — "
            "through an object-oriented API (`fig, ax = plt.subplots()`) that's more verbose but far more "
            "customizable than higher-level libraries. Seaborn builds on top of Matplotlib, adding functions that "
            "understand pandas DataFrames directly and default to statistically sensible visualizations, like "
            "automatically adding confidence intervals to a line plot or computing a proper regression line.\n\n"
            "In practice, most workflows use both: Seaborn for the fast, statistically-informed first draft, and "
            "Matplotlib's lower-level API to fine-tune labels, annotations, and layout for a polished, "
            "presentation-ready version of the same chart.\n\n"
            "Matplotlib's figure/axes hierarchy — a `Figure` is the overall canvas, which can contain one or "
            "more `Axes` (individual plot areas) — is the key mental model for anything beyond a single simple "
            "chart; multi-panel figures, shared axes, and complex layouts are all built by explicitly managing "
            "this hierarchy rather than relying on the simpler, older pyplot-style interface."
        ),
        deep_dive=(
            "Seaborn's statistical estimation happens automatically in many of its plotting functions — "
            "`sns.lineplot` with multiple observations per x-value automatically computes and displays a "
            "confidence interval band by default, and `sns.regplot`/`sns.lmplot` fit and display a regression "
            "line with its own confidence interval — this statistical layer is genuinely computed, not just "
            "cosmetic, and is a meaningful part of Seaborn's value beyond simply being 'prettier Matplotlib "
            "defaults.'\n\n"
            "Matplotlib's `constrained_layout=True` (or the newer, generally superior `layout='constrained'` "
            "parameter to `plt.subplots()`) automatically adjusts spacing between subplots and their labels to "
            "avoid overlap, addressing a very common frustration (cut-off axis labels, overlapping titles) "
            "with a single parameter rather than manual trial-and-error spacing adjustments.\n\n"
            "Saving figures for different destinations calls for different settings: a screen-only "
            "presentation might use a lower DPI (dots per inch) for a smaller file size, while a print "
            "publication typically requires 300 DPI or higher, and choosing a vector format (like SVG or PDF) "
            "rather than a raster format (PNG, JPEG) for print preserves crisp quality at any final print size."
        ),
        code=dict(
            lang="python",
            label="Seaborn for speed, Matplotlib for control",
            src=(
                "import seaborn as sns\n"
                "import matplotlib.pyplot as plt\n\n"
                "fig, ax = plt.subplots(figsize=(8, 5))\n"
                "sns.boxplot(data=df, x=\"category\", y=\"price\", ax=ax)\n"
                "ax.set_title(\"Price Distribution by Category\", fontsize=14, fontweight=\"bold\")\n"
                "ax.set_ylabel(\"Price (USD)\")\n"
                "ax.spines[[\"top\", \"right\"]].set_visible(False)\n"
                "plt.tight_layout()"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Multi-panel figure with constrained layout",
            src=(
                "fig, axes = plt.subplots(1, 2, figsize=(12, 5), layout=\"constrained\")\n\n"
                "sns.histplot(data=df, x=\"price\", ax=axes[0])\n"
                "axes[0].set_title(\"Price Distribution\")\n\n"
                "sns.scatterplot(data=df, x=\"price\", y=\"rating\", ax=axes[1])\n"
                "axes[1].set_title(\"Price vs. Rating\")\n\n"
                "fig.savefig(\"report_figure.svg\")   # vector format, crisp at any print size"
            ),
        ),
        example=(
            "A single line, `sns.regplot(data=df, x=\"ad_spend\", y=\"revenue\")`, produces a scatter plot with a "
            "fitted regression line and shaded confidence interval — replicating that in raw Matplotlib takes "
            "several additional lines of statistical and plotting code."
        ),
        best_practices=[
            "Use the object-oriented Matplotlib API (`fig, ax = plt.subplots()`) rather than the older `plt.plot()` pyplot-style calls, especially for multi-panel figures.",
            "Reach for Seaborn first when the data is in a tidy pandas DataFrame — its defaults handle grouping, coloring by category, and statistical annotations with far less code.",
            "Use `layout=\"constrained\"` to avoid manually fixing overlapping labels and titles in multi-panel figures.",
            "Save in a vector format (SVG/PDF) for anything destined for print, and choose an appropriate DPI for the actual final use case.",
        ],
        pitfalls=[
            "Mixing pyplot-style (`plt.plot`) and object-oriented (`ax.plot`) calls inconsistently within the same script, causing confusing bugs with multi-panel figures.",
            "Forgetting `plt.tight_layout()` (or `constrained_layout`), resulting in cut-off axis labels in saved figures.",
            "Saving a raster (PNG) image for a print publication, resulting in blurry or pixelated output at the final print size.",
        ],
        glossary=[
            dict(term="Figure vs. Axes", definition="In Matplotlib, a Figure is the overall canvas; Axes are individual plot areas within it — the core hierarchy for building any multi-panel chart."),
            dict(term="Confidence interval (in a plot)", definition="A shaded band around a line or estimate showing statistical uncertainty, computed automatically by many Seaborn plotting functions."),
            dict(term="Vector format", definition="An image format (like SVG or PDF) that scales without pixelation, generally preferred for print over raster formats like PNG."),
        ],
        faq=[
            dict(q="Convert this pyplot-style plotting code to the object-oriented API.", a="Replace top-level plt.plot()/plt.title() calls with fig, ax = plt.subplots() followed by ax.plot()/ax.set_title(), which gives explicit, unambiguous control over which axes each command applies to — essential once you have more than one subplot."),
            dict(q="How do I create a 2x2 grid of subplots showing different breakdowns of the same data?", a="fig, axes = plt.subplots(2, 2, figsize=(10, 8)) creates a 2x2 array of Axes objects; index into axes[0,0], axes[0,1], etc. (or flatten with axes.flat) to plot each individual breakdown onto its own subplot."),
            dict(q="What does sns.regplot add on top of a plain scatter plot?", a="It automatically fits and overlays a regression line with a shaded confidence interval band, computing the actual statistical fit rather than just adding a decorative line — a genuinely computed statistical layer, not just a stylistic addition."),
        ],
        quiz=[
            dict(
                question="What's the main advantage of the object-oriented Matplotlib API (fig, ax) over the older pyplot-style calls?",
                options=["It's the only way to make a plot at all", "It gives explicit, unambiguous control, especially important for multi-panel figures", "It automatically makes charts prettier", "It's required for Seaborn to work"],
                correct=1,
                explanation="The object-oriented API lets you explicitly reference which specific Axes a command applies to, avoiding ambiguity that becomes a real problem once a figure has more than one subplot.",
            ),
        ],
        prompts=[
            "Convert this pyplot-style plotting code to the object-oriented API.",
            "How do I create a 2x2 grid of subplots showing different breakdowns of the same data?",
            "What does sns.regplot add on top of a plain scatter plot?",
            "What DPI and file format should I use for a chart going into a printed report?",
        ],
    ),
    dict(
        id="interactive-plotly",
        title="Interactive Visualization with Plotly",
        hook="A static chart shows one view of the data; an interactive one lets the viewer ask their own follow-up questions without going back to you for a new chart.",
        explanation=(
            "Plotly builds charts as interactive HTML/JavaScript objects rather than static images, giving "
            "viewers zoom, pan, hover tooltips, and toggleable legend items for free. `plotly.express` is a "
            "high-level interface (similar in spirit to Seaborn) that produces a fully interactive chart from a "
            "DataFrame in a single function call, while the lower-level `plotly.graph_objects` gives full control "
            "for building custom, multi-trace figures or dashboards.\n\n"
            "Interactivity matters most when the audience needs to explore rather than just receive one "
            "conclusion — a static chart is right for a report making one specific point, while an interactive "
            "one is right for a dashboard someone will use repeatedly to answer different questions over time.\n\n"
            "Dash (a separate framework built on top of Plotly) lets you turn interactive charts into full, "
            "shareable web applications with callbacks — dropdowns, sliders, and buttons that trigger real "
            "Python code to update the displayed charts — going meaningfully beyond what a single static or "
            "even interactive Plotly figure alone can offer."
        ),
        deep_dive=(
            "Plotly figures are, under the hood, a JSON specification describing every trace, layout element, "
            "and style choice — this is why a Plotly figure can be serialized, saved, and reloaded exactly as "
            "it was, and why the same underlying figure object works identically whether rendered in a Jupyter "
            "notebook, a standalone HTML file, or embedded inside a Dash application.\n\n"
            "Faceting (via `facet_col`/`facet_row` in Plotly Express) is Plotly's built-in support for the "
            "small multiples pattern discussed in the chart-choosing lesson — automatically generating a grid "
            "of consistently-scaled subplots split by a categorical column, without manually managing subplot "
            "creation the way raw Matplotlib would require.\n\n"
            "For genuinely large datasets (many hundreds of thousands of points), rendering every single point "
            "interactively in a browser can become slow — techniques like aggregating data before plotting "
            "(binning into a 2D histogram/heatmap), using WebGL-accelerated trace types (`scattergl` instead "
            "of `scatter`), or sampling a representative subset of points are all practical mitigations for "
            "keeping an interactive chart responsive at scale."
        ),
        code=dict(
            lang="python",
            label="An interactive chart with hover detail",
            src=(
                "import plotly.express as px\n\n"
                "fig = px.scatter(\n"
                "    df, x=\"ad_spend\", y=\"revenue\", color=\"region\", size=\"orders\",\n"
                "    hover_data=[\"campaign_name\", \"date\"],\n"
                "    title=\"Ad Spend vs. Revenue by Region\"\n"
                ")\n"
                "fig.update_layout(template=\"plotly_white\")\n"
                "fig.show()"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Faceted small multiples, and a large-dataset-friendly WebGL trace",
            src=(
                "# Small multiples via faceting, built in\n"
                "fig = px.line(df, x=\"month\", y=\"revenue\", facet_col=\"region\", facet_col_wrap=3)\n\n"
                "# For very large point counts, use scattergl instead of scatter\n"
                "import plotly.graph_objects as go\n"
                "fig2 = go.Figure(go.Scattergl(x=df[\"x\"], y=df[\"y\"], mode=\"markers\"))"
            ),
        ),
        example=(
            "A marketing dashboard using Plotly lets a stakeholder hover over any point to see the exact "
            "campaign name and date, then toggle individual regions on and off in the legend to isolate a "
            "specific market — all without a single follow-up request to the analyst who built it."
        ),
        best_practices=[
            "Use `hover_data` deliberately to surface the specific fields a viewer would actually want when they hover, not every column in the DataFrame.",
            "Prefer Plotly (or another interactive library) when the deliverable is a dashboard people will explore repeatedly, and static Matplotlib/Seaborn for a fixed report or publication figure.",
            "Set a clean template (`plotly_white` or a custom theme) once rather than leaving the default gridlines and background for a client-facing chart.",
            "Switch to `scattergl` or aggregate data first for interactive charts with very large point counts, to keep the browser responsive.",
        ],
        pitfalls=[
            "Embedding dozens of complex interactive Plotly figures on one page, creating a large, slow-loading HTML file.",
            "Adding interactivity to a chart meant for a static PDF report, where none of the hover or zoom features will ever be usable.",
            "Rendering hundreds of thousands of individual points with the standard (non-GL) scatter trace, causing a sluggish, unresponsive browser experience.",
        ],
        glossary=[
            dict(term="plotly.express", definition="Plotly's high-level, DataFrame-native interface for quickly producing interactive charts, analogous in spirit to Seaborn."),
            dict(term="Faceting", definition="Automatically generating a grid of small, consistently-scaled subplots split by a categorical column, Plotly's built-in support for the small multiples pattern."),
            dict(term="scattergl", definition="A WebGL-accelerated scatter trace type in Plotly, used for keeping large point-count charts responsive in the browser."),
        ],
        faq=[
            dict(q="Convert this static Matplotlib chart into an interactive Plotly version.", a="Identify the equivalent plotly.express function (px.line for a line plot, px.scatter for a scatter plot, px.bar for a bar chart) and pass the same DataFrame and column names — most common Matplotlib/Seaborn chart types have a direct, similarly-simple Plotly Express equivalent."),
            dict(q="How do I add a dropdown filter to a Plotly figure?", a="Use fig.update_layout with an updatemenus configuration defining dropdown options, each specifying which trace visibility or data to switch to when selected — this lets a single figure toggle between different views without needing a full Dash application for simple cases."),
            dict(q="When does a chart actually need to be interactive versus just static?", a="When the audience needs to explore the data themselves — drilling into specific points, filtering by category, or comparing different slices repeatedly over time. A chart making one specific, fixed point for a written report or presentation slide is usually better served by a clean static image."),
        ],
        quiz=[
            dict(
                question="When should you consider using scattergl instead of the standard scatter trace in Plotly?",
                options=["Always, for every chart", "When plotting a very large number of points, for better browser performance", "Only for 3D charts", "It's identical to scatter with no difference"],
                correct=1,
                explanation="scattergl uses WebGL acceleration, which handles rendering large point counts far more smoothly in the browser than the standard SVG-based scatter trace.",
            ),
        ],
        prompts=[
            "Convert this static Matplotlib chart into an interactive Plotly version.",
            "How do I add a dropdown filter to a Plotly figure?",
            "When does a chart actually need to be interactive versus just static?",
            "How do I keep an interactive scatter plot responsive with hundreds of thousands of points?",
        ],
    ),
    dict(
        id="color-and-design-choices",
        title="Color Theory & Design Choices in Dashboards",
        hook="Color in a chart isn't decoration — it's an encoding, and using it inconsistently is functionally the same as mislabeling an axis.",
        explanation=(
            "Color should carry meaning, and that meaning should be consistent across a dashboard: if 'North "
            "Region' is blue on one chart, it should be blue everywhere, not a different color depending on "
            "which visual it appears in. There are three main types of color scale, each suited to a different "
            "kind of data: sequential (light to dark, for ordered values like revenue), diverging (two colors "
            "meeting at a neutral midpoint, for values that go both above and below a meaningful baseline like "
            "zero or a target), and qualitative (distinct hues with no inherent order, for unordered categories).\n\n"
            "Roughly 8% of men have some form of color vision deficiency, most commonly red-green, which makes "
            "red/green as a 'bad/good' encoding a genuinely common accessibility failure, not a hypothetical "
            "edge case. Colorblind-safe palettes and redundant encoding (using shape or position in addition to "
            "color) protect against this.\n\n"
            "Visual hierarchy — using size, color intensity, and position to guide the eye to what matters most "
            "first — matters as much as color choice alone; a well-designed dashboard makes the single most "
            "important number or trend immediately obvious, with supporting detail available but visually "
            "secondary, rather than presenting every piece of information with equal visual weight."
        ),
        deep_dive=(
            "Preattentive attributes (color, size, position) are visual properties the brain processes "
            "essentially instantly, before conscious, deliberate attention kicks in — this is the perceptual "
            "basis for why highlighting one data point in a saturated color against a field of muted gray "
            "others is such an effective way to draw immediate attention to it, without the viewer needing to "
            "consciously search for what matters.\n\n"
            "Data-ink ratio, a concept popularized by Edward Tufte, describes the proportion of a chart's "
            "visual elements that actually convey information versus purely decorative chart-junk (unnecessary "
            "gridlines, heavy borders, 3D effects with no informational value) — maximizing this ratio "
            "generally produces cleaner, more effective charts, though the principle is a guideline for "
            "restraint rather than a rule demanding the absolute visual minimum in every case.\n\n"
            "Culturally, color associations aren't universal — red commonly means danger/loss in Western "
            "financial contexts but can carry very different (sometimes positive) connotations in other "
            "cultural contexts, which is worth considering explicitly for any dashboard or report intended for "
            "a genuinely international audience rather than assuming one region's color conventions translate "
            "everywhere."
        ),
        code=dict(
            lang="python",
            label="Using an appropriate, colorblind-safe scale",
            src=(
                "import plotly.express as px\n\n"
                "# Diverging: values meaningfully above/below zero\n"
                "fig1 = px.bar(df, x=\"month\", y=\"profit_vs_target\",\n"
                "              color=\"profit_vs_target\", color_continuous_scale=\"RdBu\")\n\n"
                "# Sequential: ordered values, one direction\n"
                "fig2 = px.choropleth(df, color=\"population\", color_continuous_scale=\"Viridis\")\n\n"
                "# Qualitative, colorblind-safe: unordered categories\n"
                "fig3 = px.bar(df, x=\"region\", y=\"sales\", color=\"region\",\n"
                "              color_discrete_sequence=px.colors.qualitative.Safe)"
            ),
        ),
        advanced_code=dict(
            lang="python",
            label="Using preattentive highlighting to draw the eye to what matters",
            src=(
                "import plotly.express as px\n\n"
                "df[\"highlight\"] = df[\"region\"].apply(lambda r: \"Target Region\" if r == \"East Africa\" else \"Other\")\n\n"
                "fig = px.bar(\n"
                "    df, x=\"region\", y=\"revenue\", color=\"highlight\",\n"
                "    color_discrete_map={\"Target Region\": \"#d62728\", \"Other\": \"#d3d3d3\"}\n"
                ")\n"
                "# One region pops in saturated red; everything else recedes into muted gray"
            ),
        ),
        example=(
            "A retail dashboard switched its 'over/under target' bar chart from red-versus-green to a "
            "blue-versus-orange diverging palette after a colorblind stakeholder couldn't reliably tell which "
            "stores were underperforming — the data didn't change, but the chart went from unusable to clear for that viewer."
        ),
        best_practices=[
            "Fix one color to one meaning across an entire dashboard, and keep that mapping unchanged from chart to chart.",
            "Use a colorblind-safe qualitative palette (like ColorBrewer's 'Set2' or Plotly's 'Safe') by default rather than an arbitrary rainbow of colors.",
            "Reserve saturated, high-contrast color for the one or two data points that matter most; let everything else recede into muted grays.",
            "Consider maximizing data-ink ratio as a guideline — remove chart elements that don't convey information, without stripping a chart down to the point of losing necessary context.",
        ],
        pitfalls=[
            "Using red and green as the only signal for 'bad' and 'good,' which is unreadable for a meaningful share of viewers.",
            "Letting the same category get a different color on different charts within the same report, forcing viewers to re-learn the legend each time.",
            "Assuming color conventions (like red for danger) translate universally across all cultural contexts for an international audience.",
        ],
        glossary=[
            dict(term="Sequential color scale", definition="A color gradient (typically light to dark) representing ordered numeric values, one direction of intensity."),
            dict(term="Diverging color scale", definition="A color gradient with two distinct hues meeting at a neutral midpoint, representing values that meaningfully go both above and below a baseline."),
            dict(term="Preattentive attributes", definition="Visual properties like color and size that the brain processes almost instantly, before conscious attention, useful for drawing immediate focus."),
            dict(term="Data-ink ratio", definition="The proportion of a chart's visual elements that convey actual information versus purely decorative chart-junk, a concept from Edward Tufte."),
        ],
        faq=[
            dict(q="Suggest a colorblind-safe palette for this multi-region sales chart.", a="Plotly's 'Safe' qualitative palette (px.colors.qualitative.Safe) or ColorBrewer's 'Set2'/'Dark2' palettes are widely used, tested colorblind-safe options for unordered categorical data like regions."),
            dict(q="What's the difference between a sequential and a diverging color scale, with examples of when to use each?", a="Sequential (like light-to-dark blue) suits ordered values with one natural direction, like population or revenue. Diverging (like blue-to-white-to-red) suits values with a meaningful zero or target midpoint, like profit vs. target or temperature anomaly from a baseline."),
            dict(q="How should I encode 'over target' vs 'under target' without relying only on red and green?", a="Use a diverging color scale with colorblind-distinguishable hues (like blue for under, orange for over) instead of red/green, and consider adding a redundant encoding like a directional arrow icon or explicit +/- labeling for additional clarity beyond color alone."),
        ],
        quiz=[
            dict(
                question="Why is red/green as the sole encoding for 'bad/good' considered a genuine accessibility problem?",
                options=["Red and green are visually identical to everyone", "A meaningful share of people (especially men) have red-green color vision deficiency", "It's only a stylistic preference, not an accessibility issue", "Charts never use red or green together"],
                correct=1,
                explanation="Red-green color vision deficiency affects roughly 8% of men, making red/green as the sole distinguishing signal genuinely unreadable for a meaningful portion of any audience.",
            ),
        ],
        prompts=[
            "Suggest a colorblind-safe palette for this multi-region sales chart.",
            "What's the difference between a sequential and a diverging color scale, with examples of when to use each?",
            "How should I encode 'over target' vs 'under target' without relying only on red and green?",
            "How can I use preattentive attributes to highlight the most important data point in this chart?",
        ],
    ),
]