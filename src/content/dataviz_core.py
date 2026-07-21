"""Data Visualization subtopics."""

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
            "Picking the chart first and forcing the data to fit it is backward — the question should choose the chart."
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
        example=(
            "A dashboard replacing a seven-slice pie chart of 'traffic source' with a sorted horizontal bar chart "
            "made the exact same underlying data readable at a glance instead of requiring the viewer to compare "
            "wedge angles — a purely structural fix, with zero new data or styling."
        ),
        best_practices=[
            "Start from the question ('compare categories', 'show a trend', 'show a relationship') and let it determine the chart type.",
            "Sort categorical bar charts by value rather than alphabetically, unless the category order itself carries meaning (like days of the week).",
            "Reserve pie charts for two or three slices at most, if you use them at all — a bar chart almost always communicates the same comparison more clearly.",
        ],
        pitfalls=[
            "Defaulting to a pie chart out of habit for any categorical breakdown, regardless of how many categories there are.",
            "Using a line chart to connect points that aren't actually sequential or continuous, implying a trend that doesn't exist.",
        ],
        prompts=[
            "What chart type fits comparing five products' monthly sales trends?",
            "Why is a pie chart considered a poor choice for more than a few categories?",
            "Suggest a better chart than a pie chart for this survey response breakdown.",
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
            "presentation-ready version of the same chart."
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
        example=(
            "A single line, `sns.regplot(data=df, x=\"ad_spend\", y=\"revenue\")`, produces a scatter plot with a "
            "fitted regression line and shaded confidence interval — replicating that in raw Matplotlib takes "
            "several additional lines of statistical and plotting code."
        ),
        best_practices=[
            "Use the object-oriented Matplotlib API (`fig, ax = plt.subplots()`) rather than the older `plt.plot()` pyplot-style calls, especially for multi-panel figures.",
            "Reach for Seaborn first when the data is in a tidy pandas DataFrame — its defaults handle grouping, coloring by category, and statistical annotations with far less code.",
            "Set a consistent style and color palette once (`sns.set_theme()`) at the top of a notebook instead of restyling every chart individually.",
        ],
        pitfalls=[
            "Mixing pyplot-style (`plt.plot`) and object-oriented (`ax.plot`) calls inconsistently within the same script, causing confusing bugs with multi-panel figures.",
            "Forgetting `plt.tight_layout()` (or `constrained_layout`), resulting in cut-off axis labels in saved figures.",
        ],
        prompts=[
            "Convert this pyplot-style plotting code to the object-oriented API.",
            "How do I create a 2x2 grid of subplots showing different breakdowns of the same data?",
            "What does sns.regplot add on top of a plain scatter plot?",
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
            "one is right for a dashboard someone will use repeatedly to answer different questions over time."
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
        example=(
            "A marketing dashboard using Plotly lets a stakeholder hover over any point to see the exact "
            "campaign name and date, then toggle individual regions on and off in the legend to isolate a "
            "specific market — all without a single follow-up request to the analyst who built it."
        ),
        best_practices=[
            "Use `hover_data` deliberately to surface the specific fields a viewer would actually want when they hover, not every column in the DataFrame.",
            "Prefer Plotly (or another interactive library) when the deliverable is a dashboard people will explore repeatedly, and static Matplotlib/Seaborn for a fixed report or publication figure.",
            "Set a clean template (`plotly_white` or a custom theme) once rather than leaving the default gridlines and background for a client-facing chart.",
        ],
        pitfalls=[
            "Embedding dozens of complex interactive Plotly figures on one page, creating a large, slow-loading HTML file.",
            "Adding interactivity to a chart meant for a static PDF report, where none of the hover or zoom features will ever be usable.",
        ],
        prompts=[
            "Convert this static Matplotlib chart into an interactive Plotly version.",
            "How do I add a dropdown filter to a Plotly figure?",
            "When does a chart actually need to be interactive versus just static?",
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
            "color) protect against this."
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
        example=(
            "A retail dashboard switched its 'over/under target' bar chart from red-versus-green to a "
            "blue-versus-orange diverging palette after a colorblind stakeholder couldn't reliably tell which "
            "stores were underperforming — the data didn't change, but the chart went from unusable to clear for that viewer."
        ),
        best_practices=[
            "Fix one color to one meaning across an entire dashboard, and keep that mapping unchanged from chart to chart.",
            "Use a colorblind-safe qualitative palette (like ColorBrewer's 'Set2' or Plotly's 'Safe') by default rather than an arbitrary rainbow of colors.",
            "Reserve saturated, high-contrast color for the one or two data points that matter most; let everything else recede into muted grays.",
        ],
        pitfalls=[
            "Using red and green as the only signal for 'bad' and 'good,' which is unreadable for a meaningful share of viewers.",
            "Letting the same category get a different color on different charts within the same report, forcing viewers to re-learn the legend each time.",
        ],
        prompts=[
            "Suggest a colorblind-safe palette for this multi-region sales chart.",
            "What's the difference between a sequential and a diverging color scale, with examples of when to use each?",
            "How should I encode 'over target' vs 'under target' without relying only on red and green?",
        ],
    ),
]
