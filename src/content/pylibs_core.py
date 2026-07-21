"""Python Libraries — one-by-one survey (22+ libraries)."""

SUBTOPICS = [
    dict(
        id="numpy",
        title="NumPy",
        hook="The array library nearly every other data/ML library in Python is built on top of, directly or indirectly.",
        explanation=(
            "NumPy provides the `ndarray`, a fixed-type, contiguous-memory array that supports vectorized "
            "operations — applying a computation to every element at once via optimized C code, instead of a "
            "Python-level for-loop. This is why `arr * 2` on a NumPy array of a million numbers runs orders of "
            "magnitude faster than the equivalent Python list comprehension."
        ),
        code=dict(
            lang="python",
            label="Vectorized operations vs. plain Python",
            src=(
                "import numpy as np\n\n"
                "arr = np.array([1, 2, 3, 4, 5])\n"
                "print(arr * 2)             # [2 4 6 8 10] — no loop needed\n"
                "print(arr[arr > 2])        # boolean indexing: [3 4 5]\n\n"
                "matrix = np.array([[1, 2], [3, 4]])\n"
                "print(matrix.T)             # transpose\n"
                "print(matrix @ matrix)      # matrix multiplication"
            ),
        ),
        example=(
            "Pandas, scikit-learn, and TensorFlow all use NumPy arrays as their underlying data format — "
            "learning NumPy's indexing and broadcasting rules pays off across the entire Python data stack, not just NumPy itself."
        ),
        best_practices=[
            "Prefer vectorized operations and broadcasting over explicit Python loops over array elements.",
            "Use boolean indexing (`arr[arr > 0]`) instead of filtering with a list comprehension.",
        ],
        pitfalls=[
            "Looping over a NumPy array element-by-element in pure Python, throwing away the entire performance benefit.",
            "Mixing incompatible shapes and relying on broadcasting rules without understanding them, producing silently wrong results.",
        ],
        prompts=[
            "Explain NumPy broadcasting rules with a shape example.",
            "Vectorize this Python for-loop using NumPy.",
        ],
    ),
    dict(
        id="pandas",
        title="Pandas",
        hook="The default tool for loading, cleaning, and reshaping tabular data in Python — think 'Excel, but scriptable and reproducible.'",
        explanation=(
            "Pandas introduces the `DataFrame` (a labeled, 2D table) and `Series` (a labeled, 1D column), built "
            "on top of NumPy. It provides expressive tools for filtering, grouping, merging, and reshaping data "
            "that would take many lines of manual code with plain lists and dicts."
        ),
        code=dict(
            lang="python",
            label="Load, filter, group, aggregate",
            src=(
                "import pandas as pd\n\n"
                "df = pd.read_csv(\"sales.csv\")\n"
                "recent = df[df[\"date\"] >= \"2026-01-01\"]\n"
                "summary = recent.groupby(\"region\")[\"revenue\"].sum().sort_values(ascending=False)\n"
                "print(summary.head())"
            ),
        ),
        example=(
            "An analyst turning a raw 2-million-row CSV export into a clean regional revenue summary does it in "
            "four lines of Pandas instead of hand-writing a dictionary-based aggregation loop."
        ),
        best_practices=[
            "Use vectorized column operations (`df['total'] = df['price'] * df['qty']`) instead of `.iterrows()`.",
            "Chain `.loc[]` for label-based selection and avoid mixing it with positional indexing in the same expression.",
        ],
        pitfalls=[
            "Using `.iterrows()` for a transformation that could be vectorized, which is often 50-100x slower.",
            "Chained indexing (`df[df.a > 1]['b'] = 2`) that triggers a SettingWithCopyWarning and may silently not update the original DataFrame.",
        ],
        prompts=[
            "Why is .iterrows() slow, and how do I vectorize this loop?",
            "Write a Pandas groupby that computes multiple aggregations per group.",
        ],
    ),
    dict(
        id="matplotlib",
        title="Matplotlib",
        hook="The foundational plotting library nearly every other Python visualization tool sits on top of.",
        explanation=(
            "Matplotlib provides fine-grained control over every visual element of a chart through an "
            "object-oriented API (`Figure` and `Axes` objects). It's more verbose than higher-level libraries "
            "but is the right tool whenever you need pixel-level control over a static, publication-quality figure."
        ),
        code=dict(
            lang="python",
            label="A styled figure with the object-oriented API",
            src=(
                "import matplotlib.pyplot as plt\n\n"
                "fig, ax = plt.subplots(figsize=(7, 4))\n"
                "ax.plot(months, revenue, marker=\"o\", color=\"#2f6fed\")\n"
                "ax.set_title(\"Monthly Revenue\")\n"
                "ax.set_ylabel(\"USD\")\n"
                "fig.savefig(\"revenue.png\", dpi=150, bbox_inches=\"tight\")"
            ),
        ),
        example=(
            "A scientific paper's figures are almost always Matplotlib, because reviewers expect exact control "
            "over fonts, axis ticks, and export resolution that higher-level charting libraries don't expose."
        ),
        best_practices=[
            "Use `fig, ax = plt.subplots()` rather than the older stateful `plt.plot()` calls, especially for multi-panel figures.",
            "Save with `bbox_inches='tight'` to avoid cropped labels in exported images.",
        ],
        pitfalls=[
            "Forgetting `plt.tight_layout()`, resulting in overlapping or cut-off labels.",
            "Mixing pyplot-style and object-oriented calls inconsistently, causing confusing multi-figure bugs.",
        ],
        prompts=[
            "Convert this pyplot-style script to the object-oriented Matplotlib API.",
            "How do I create a figure with two subplots sharing an x-axis?",
        ],
    ),
    dict(
        id="seaborn",
        title="Seaborn",
        hook="Matplotlib with statistically-aware defaults and native pandas support — usually the fastest way to a good-looking first chart.",
        explanation=(
            "Seaborn wraps Matplotlib with functions that understand DataFrames directly and default to "
            "sensible statistical visualizations — confidence intervals on line plots, proper regression fits, "
            "and automatic color grouping by category — with far less code than the Matplotlib equivalent."
        ),
        code=dict(
            lang="python",
            label="A grouped comparison in one line",
            src=(
                "import seaborn as sns\n\n"
                "sns.set_theme(style=\"whitegrid\")\n"
                "sns.boxplot(data=df, x=\"category\", y=\"price\", hue=\"region\")"
            ),
        ),
        example=(
            "A single `sns.pairplot(df)` call generates a full grid of scatter plots and histograms for every "
            "numeric column pair in a DataFrame — a fast way to explore a new dataset before deciding what to build with Matplotlib."
        ),
        best_practices=[
            "Use Seaborn for the fast first draft, then switch to raw Matplotlib for final polish on titles, annotations, and layout.",
            "Set a consistent theme once (`sns.set_theme()`) rather than restyling each chart.",
        ],
        pitfalls=[
            "Trying to fully customize a complex figure in Seaborn instead of dropping down to Matplotlib once you hit its limits.",
        ],
        prompts=[
            "What does sns.regplot compute automatically that a plain scatter plot doesn't?",
            "Show me how to build a correlation heatmap with Seaborn.",
        ],
    ),
    dict(
        id="plotly",
        title="Plotly",
        hook="Interactive, zoomable, hoverable charts rendered as HTML/JS instead of static images.",
        explanation=(
            "Plotly builds charts as interactive objects with built-in zoom, pan, and hover tooltips. "
            "`plotly.express` offers a high-level, DataFrame-native API similar in spirit to Seaborn, while "
            "`plotly.graph_objects` gives lower-level control for custom, multi-trace dashboards."
        ),
        code=dict(
            lang="python",
            label="An interactive scatter with hover detail",
            src=(
                "import plotly.express as px\n\n"
                "fig = px.scatter(df, x=\"spend\", y=\"revenue\", color=\"region\",\n"
                "                  hover_data=[\"campaign\"], trendline=\"ols\")\n"
                "fig.show()"
            ),
        ),
        example=(
            "A dashboard letting stakeholders hover over any point for exact values, and toggle regions on/off "
            "in the legend, is built with a handful of Plotly Express calls instead of custom JavaScript."
        ),
        best_practices=[
            "Reach for Plotly specifically when the deliverable is an exploratory dashboard, not a fixed report figure.",
            "Curate `hover_data` deliberately instead of dumping every column into the tooltip.",
        ],
        pitfalls=[
            "Embedding dozens of complex Plotly figures on one page, producing a slow-loading HTML file.",
        ],
        prompts=[
            "Convert this Matplotlib chart into an interactive Plotly version.",
            "How do I add a dropdown filter to switch between metrics in a Plotly chart?",
        ],
    ),
    dict(
        id="requests",
        title="Requests",
        hook="The library that made calling an HTTP API in Python feel like a two-line operation instead of a networking chore.",
        explanation=(
            "Requests wraps Python's lower-level `urllib` into a simple, human-friendly API for making HTTP "
            "calls — GET, POST, headers, JSON bodies, authentication — with sensible defaults and clear error handling."
        ),
        code=dict(
            lang="python",
            label="A GET request with error handling",
            src=(
                "import requests\n\n"
                "resp = requests.get(\n"
                "    \"https://api.example.com/users\",\n"
                "    headers={\"Authorization\": f\"Bearer {token}\"},\n"
                "    timeout=10,\n"
                ")\n"
                "resp.raise_for_status()   # raises an exception on 4xx/5xx\n"
                "users = resp.json()"
            ),
        ),
        example=(
            "A script pulling exchange rates from a public API each morning uses `requests.get()` plus "
            "`raise_for_status()` to fail loudly and immediately if the API is down, rather than silently working with stale data."
        ),
        best_practices=[
            "Always set a `timeout` — a request with no timeout can hang your program indefinitely.",
            "Call `.raise_for_status()` (or check `resp.status_code`) instead of assuming every request succeeded.",
        ],
        pitfalls=[
            "Making a request with no timeout, which can hang the entire program on a network blip.",
            "Assuming `resp.json()` will succeed on a non-JSON error response.",
        ],
        prompts=[
            "How do I retry a failed request with exponential backoff using requests?",
            "What's the difference between requests and the built-in urllib?",
        ],
    ),
    dict(
        id="flask",
        title="Flask",
        hook="A minimal web framework that gives you routing and request handling, and deliberately leaves the rest up to you.",
        explanation=(
            "Flask is a 'micro' web framework — it provides the essentials (URL routing, request/response "
            "objects, templating via Jinja2) without prescribing a project structure or bundling an ORM, unlike "
            "Django. This makes it a common choice for APIs, small services, and prototypes where you want control "
            "over which pieces to add."
        ),
        code=dict(
            lang="python",
            label="A minimal Flask API",
            src=(
                "from flask import Flask, jsonify, request\n\n"
                "app = Flask(__name__)\n\n"
                "@app.route(\"/api/health\")\n"
                "def health():\n"
                "    return jsonify(status=\"ok\")\n\n"
                "@app.route(\"/api/echo\", methods=[\"POST\"])\n"
                "def echo():\n"
                "    return jsonify(request.get_json())\n\n"
                "if __name__ == \"__main__\":\n"
                "    app.run(debug=True)"
            ),
        ),
        example=(
            "This very platform is built on Flask — a small set of routes serving pre-written lesson content and "
            "a couple of API endpoints for the optional AI assistant, with no unnecessary framework overhead."
        ),
        best_practices=[
            "Never run with `debug=True` in production — it exposes a remote code execution risk via the interactive debugger.",
            "Keep secrets in environment variables, never hardcoded in the app, and load them with `python-dotenv` in development.",
        ],
        pitfalls=[
            "Leaving `debug=True` on in a deployed app, which is a serious security hole.",
            "Building a large app as a single `app.py` file instead of using Blueprints once routes start multiplying.",
        ],
        prompts=[
            "How do I structure a growing Flask app using Blueprints?",
            "What's the difference between Flask and FastAPI for building an API?",
        ],
    ),
    dict(
        id="django",
        title="Django",
        hook="A 'batteries-included' web framework that bundles an ORM, admin panel, and authentication out of the box — the opposite philosophy from Flask.",
        explanation=(
            "Django provides a full-featured framework: an ORM for database models, a built-in admin interface "
            "generated from those models, a templating engine, authentication, and a project structure with "
            "strong conventions. It trades some flexibility for speed on standard, database-backed web applications."
        ),
        code=dict(
            lang="python",
            label="A Django model and its auto-generated admin",
            src=(
                "# models.py\n"
                "from django.db import models\n\n"
                "class Article(models.Model):\n"
                "    title = models.CharField(max_length=200)\n"
                "    body = models.TextField()\n"
                "    published_at = models.DateTimeField(auto_now_add=True)\n\n"
                "# admin.py\n"
                "from django.contrib import admin\n"
                "from .models import Article\n"
                "admin.site.register(Article)   # instant CRUD UI, no extra code"
            ),
        ),
        example=(
            "A content-heavy site needing an admin panel for non-technical editors to manage articles gets that "
            "UI for free from Django's admin app, something that would need to be hand-built in Flask."
        ),
        best_practices=[
            "Use Django's ORM migrations (`makemigrations` / `migrate`) rather than modifying the database schema by hand.",
            "Reach for Django when the project needs a database-backed admin, auth, and CRUD quickly; reach for Flask/FastAPI when you want minimal, composable pieces.",
        ],
        pitfalls=[
            "Fighting Django's conventions (custom user models added too late, bypassing the ORM) instead of working with them from the start.",
        ],
        prompts=[
            "When would I choose Django over Flask for a new project?",
            "How do Django migrations work, and what happens if two developers create conflicting ones?",
        ],
    ),
    dict(
        id="fastapi",
        title="FastAPI",
        hook="A modern, async-first web framework that generates interactive API documentation automatically from your type hints.",
        explanation=(
            "FastAPI uses Python type hints and Pydantic models to validate request/response data and "
            "automatically generate an interactive OpenAPI (Swagger) documentation page — no separate schema "
            "file to maintain. Built on Starlette and async by default, it's a common choice for high-throughput APIs."
        ),
        code=dict(
            lang="python",
            label="A typed, self-documenting endpoint",
            src=(
                "from fastapi import FastAPI\n"
                "from pydantic import BaseModel\n\n"
                "app = FastAPI()\n\n"
                "class Item(BaseModel):\n"
                "    name: str\n"
                "    price: float\n\n"
                "@app.post(\"/items\")\n"
                "async def create_item(item: Item):\n"
                "    return {\"received\": item, \"tax\": item.price * 0.16}"
            ),
        ),
        example=(
            "A mobile app team building against a FastAPI backend gets a live, always-current API reference at "
            "`/docs` for free, generated directly from the endpoint's type hints — no separate documentation to fall out of sync."
        ),
        best_practices=[
            "Define request/response shapes as Pydantic models rather than raw dicts — you get validation and documentation for free.",
            "Use `async def` for I/O-bound endpoints (database calls, external APIs) to take advantage of FastAPI's async performance.",
        ],
        pitfalls=[
            "Mixing blocking, synchronous calls inside an `async def` endpoint, which can stall the entire event loop.",
        ],
        prompts=[
            "Convert this Flask endpoint to FastAPI with proper request validation.",
            "Explain the difference between def and async def endpoints in FastAPI.",
        ],
    ),
    dict(
        id="beautifulsoup",
        title="BeautifulSoup",
        hook="Turns messy, real-world HTML into a navigable Python object you can search by tag, class, or CSS selector.",
        explanation=(
            "BeautifulSoup parses HTML/XML into a tree structure and provides methods to search it — by tag "
            "name, attribute, CSS class, or CSS selector — even when the source HTML is malformed, which real "
            "web pages very often are."
        ),
        code=dict(
            lang="python",
            label="Extracting article titles from a page",
            src=(
                "from bs4 import BeautifulSoup\n"
                "import requests\n\n"
                "html = requests.get(\"https://example.com/blog\").text\n"
                "soup = BeautifulSoup(html, \"html.parser\")\n\n"
                "titles = [h.get_text(strip=True) for h in soup.select(\"h2.post-title\")]"
            ),
        ),
        example=(
            "A price-monitoring script parses a retailer's product page nightly with BeautifulSoup to extract "
            "the current price from a specific `<span class='price'>` tag, tracking changes over time."
        ),
        best_practices=[
            "Always check a site's `robots.txt` and terms of service before scraping it programmatically.",
            "Use CSS selectors (`.select()`) for anything beyond the simplest single-tag lookup — they're more precise and readable than chained `.find()` calls.",
        ],
        pitfalls=[
            "Assuming a page's HTML structure will never change — scrapers built this way break silently the moment a site redesigns.",
            "Scraping aggressively without rate limiting, which can get an IP address blocked or violate a site's terms.",
        ],
        prompts=[
            "Write a BeautifulSoup selector to extract all links inside a specific div.",
            "How do I make my scraper resilient to small HTML structure changes?",
        ],
    ),
    dict(
        id="scikit-learn",
        title="Scikit-learn",
        hook="The standard library for classical machine learning in Python — a consistent fit/predict interface across dozens of algorithms.",
        explanation=(
            "Scikit-learn provides a unified API (`.fit()`, `.predict()`, `.transform()`) across regression, "
            "classification, clustering, and preprocessing tools, which means swapping one algorithm for another "
            "is often a one-line change. Its `Pipeline` class chains preprocessing and modeling steps into a "
            "single object that behaves correctly under cross-validation."
        ),
        code=dict(
            lang="python",
            label="A complete, leak-safe training pipeline",
            src=(
                "from sklearn.pipeline import Pipeline\n"
                "from sklearn.preprocessing import StandardScaler\n"
                "from sklearn.ensemble import RandomForestClassifier\n"
                "from sklearn.model_selection import cross_val_score\n\n"
                "pipe = Pipeline([\n"
                "    (\"scale\", StandardScaler()),\n"
                "    (\"clf\", RandomForestClassifier(random_state=42)),\n"
                "])\n"
                "scores = cross_val_score(pipe, X, y, cv=5)"
            ),
        ),
        example=(
            "A churn-prediction model for a subscription business is prototyped in an afternoon using "
            "scikit-learn's consistent API — swapping `LogisticRegression` for `RandomForestClassifier` to compare them is a one-line change."
        ),
        best_practices=[
            "Wrap preprocessing and the model together in a `Pipeline` to prevent data leakage during cross-validation.",
            "Use `GridSearchCV` or `RandomizedSearchCV` for hyperparameter tuning instead of manual trial and error.",
        ],
        pitfalls=[
            "Fitting a scaler on the full dataset before splitting, leaking test information into training.",
        ],
        prompts=[
            "Should I use GridSearchCV or RandomizedSearchCV for this hyperparameter search?",
            "Explain what Pipeline actually prevents during cross-validation.",
        ],
    ),
    dict(
        id="tensorflow",
        title="TensorFlow / Keras",
        hook="Google's deep learning framework, most commonly used today through its high-level Keras API.",
        explanation=(
            "TensorFlow is a full deep learning framework; Keras, now built directly into it as `tf.keras`, "
            "provides a high-level, readable API for defining and training neural networks without hand-writing "
            "gradient computations. It's a common choice for production deployment given tools like TensorFlow Serving and TensorFlow Lite."
        ),
        code=dict(
            lang="python",
            label="Defining and training a small model",
            src=(
                "import tensorflow as tf\n\n"
                "model = tf.keras.Sequential([\n"
                "    tf.keras.layers.Dense(64, activation=\"relu\", input_shape=(20,)),\n"
                "    tf.keras.layers.Dense(1, activation=\"sigmoid\"),\n"
                "])\n"
                "model.compile(optimizer=\"adam\", loss=\"binary_crossentropy\", metrics=[\"accuracy\"])\n"
                "model.fit(X_train, y_train, epochs=10, validation_split=0.2)"
            ),
        ),
        example=(
            "A mobile app running on-device image classification converts a trained `tf.keras` model to "
            "TensorFlow Lite, shrinking it to run efficiently on a phone's limited compute — a deployment path TensorFlow supports natively."
        ),
        best_practices=[
            "Always call `model.summary()` after defining an architecture to catch shape mismatches before training.",
            "Use callbacks like `EarlyStopping` and `ModelCheckpoint` rather than manually watching training curves.",
        ],
        pitfalls=[
            "Feeding un-normalized inputs into a network expecting a 0-1 or standardized range, slowing or destabilizing training.",
        ],
        prompts=[
            "Why did my model.summary() show a shape mismatch, and how do I fix it?",
            "What's the difference between TensorFlow and Keras today?",
        ],
    ),
    dict(
        id="pytorch",
        title="PyTorch",
        hook="The deep learning framework most research papers and cutting-edge model releases ship code in, prized for its flexible, 'just Python' feel.",
        explanation=(
            "PyTorch builds computation graphs dynamically as code executes (define-by-run), which makes "
            "debugging feel like debugging ordinary Python rather than a separate compiled graph. Its autograd "
            "system automatically computes gradients for backpropagation from operations on `Tensor` objects."
        ),
        code=dict(
            lang="python",
            label="A basic training loop",
            src=(
                "import torch, torch.nn as nn\n\n"
                "model = nn.Sequential(nn.Linear(20, 64), nn.ReLU(), nn.Linear(64, 1), nn.Sigmoid())\n"
                "optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)\n"
                "loss_fn = nn.BCELoss()\n\n"
                "for epoch in range(10):\n"
                "    optimizer.zero_grad()\n"
                "    preds = model(X_train)\n"
                "    loss = loss_fn(preds, y_train)\n"
                "    loss.backward()\n"
                "    optimizer.step()"
            ),
        ),
        example=(
            "Most newly published research models on Hugging Face ship PyTorch weights first, since the "
            "flexibility of define-by-run graphs makes it the preferred framework for experimenting with novel architectures."
        ),
        best_practices=[
            "Call `optimizer.zero_grad()` at the start of every training step — gradients accumulate by default otherwise.",
            "Move both the model and data to the same device (`.to('cuda')` or `.to('mps')`) before training, or you'll hit a device mismatch error.",
        ],
        pitfalls=[
            "Forgetting `zero_grad()`, which silently accumulates gradients across steps and destabilizes training.",
            "Leaving the model in training mode (`model.train()`) during evaluation, which affects layers like Dropout and BatchNorm.",
        ],
        prompts=[
            "Why do I need to call zero_grad() every training step?",
            "What's the practical difference between model.train() and model.eval()?",
        ],
    ),
    dict(
        id="sqlalchemy",
        title="SQLAlchemy",
        hook="Python's most widely used ORM and SQL toolkit — write Python classes, get real, portable SQL underneath.",
        explanation=(
            "SQLAlchemy lets you define database tables as Python classes (the ORM layer) and query them with "
            "Python expressions instead of raw SQL strings, while still generating real, optimized SQL under the "
            "hood. It also offers a lower-level Core API for when you want more direct SQL control without giving up the toolkit."
        ),
        code=dict(
            lang="python",
            label="Defining a model and querying it",
            src=(
                "from sqlalchemy import create_engine, select\n"
                "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session\n\n"
                "class Base(DeclarativeBase): pass\n\n"
                "class User(Base):\n"
                "    __tablename__ = \"users\"\n"
                "    id: Mapped[int] = mapped_column(primary_key=True)\n"
                "    email: Mapped[str]\n\n"
                "engine = create_engine(\"sqlite:///app.db\")\n"
                "with Session(engine) as session:\n"
                "    users = session.scalars(select(User).where(User.email.like(\"%@company.com\"))).all()"
            ),
        ),
        example=(
            "A Flask app switching its backing database from SQLite in development to PostgreSQL in production "
            "changes only the connection string — the same SQLAlchemy models and queries work against both, because SQLAlchemy abstracts the SQL dialect differences."
        ),
        best_practices=[
            "Use the ORM for typical application CRUD, and drop to SQLAlchemy Core or raw SQL for complex reporting queries where the ORM adds overhead without benefit.",
            "Always use sessions as context managers (`with Session(engine) as session:`) to ensure connections are properly closed.",
        ],
        pitfalls=[
            "Triggering the 'N+1 query problem' by accessing a related object inside a loop without eager loading it first.",
        ],
        prompts=[
            "What's the N+1 query problem in SQLAlchemy, and how do I fix it with eager loading?",
            "Show me the difference between SQLAlchemy's ORM and Core APIs for the same query.",
        ],
    ),
    dict(
        id="pytest",
        title="Pytest",
        hook="The de facto standard testing framework in Python, prized for letting you write `assert some_value == expected` instead of verbose assertion methods.",
        explanation=(
            "Pytest discovers and runs test functions automatically (any function prefixed `test_`), uses plain "
            "`assert` statements with rich failure output, and provides fixtures — reusable setup/teardown "
            "functions injected into tests by name — for managing test dependencies cleanly."
        ),
        code=dict(
            lang="python",
            label="A test with a fixture",
            src=(
                "import pytest\n\n"
                "@pytest.fixture\n"
                "def sample_cart():\n"
                "    return {\"items\": [], \"total\": 0}\n\n"
                "def test_add_item_updates_total(sample_cart):\n"
                "    sample_cart[\"items\"].append({\"price\": 10})\n"
                "    sample_cart[\"total\"] += 10\n"
                "    assert sample_cart[\"total\"] == 10\n"
                "    assert len(sample_cart[\"items\"]) == 1"
            ),
        ),
        example=(
            "A CI pipeline runs `pytest` on every pull request; a failing test blocks the merge automatically, "
            "catching a regression before it ever reaches production instead of after a customer reports it."
        ),
        best_practices=[
            "Use fixtures for shared setup instead of copy-pasting the same setup code into every test function.",
            "Use `pytest.mark.parametrize` to run the same test logic against multiple input/output pairs without duplicating the test body.",
        ],
        pitfalls=[
            "Writing tests that depend on execution order or shared mutable state, which pass individually but fail when run together.",
        ],
        prompts=[
            "Show me how to parametrize this test to cover five different inputs.",
            "How do pytest fixtures with different scopes (function, module, session) behave differently?",
        ],
    ),
    dict(
        id="nltk",
        title="NLTK",
        hook="One of the original Python natural language processing toolkits — still widely used for teaching NLP fundamentals and quick text-processing tasks.",
        explanation=(
            "NLTK (Natural Language Toolkit) provides tools for tokenization, stemming, part-of-speech tagging, "
            "and access to linguistic corpora. It's slower and less production-oriented than newer libraries like "
            "spaCy or transformer-based approaches, but its clear, educational API makes it a common starting point for learning core NLP concepts."
        ),
        code=dict(
            lang="python",
            label="Tokenizing and tagging a sentence",
            src=(
                "import nltk\n"
                "nltk.download(\"punkt\"); nltk.download(\"averaged_perceptron_tagger\")\n\n"
                "text = \"NLTK makes basic text processing approachable.\"\n"
                "tokens = nltk.word_tokenize(text)\n"
                "tags = nltk.pos_tag(tokens)\n"
                "print(tags)   # [('NLTK', 'NNP'), ('makes', 'VBZ'), ...]"
            ),
        ),
        example=(
            "A student building a first sentiment-analysis project uses NLTK's built-in movie review corpus and "
            "a simple bag-of-words classifier to learn the fundamentals before moving on to modern transformer-based sentiment models."
        ),
        best_practices=[
            "Use NLTK for learning and quick prototyping; move to spaCy or a transformer-based library for anything performance-sensitive or production-bound.",
        ],
        pitfalls=[
            "Forgetting to download the specific NLTK data package (`punkt`, `stopwords`, etc.) a function depends on, causing a `LookupError`.",
        ],
        prompts=[
            "What's the difference between NLTK and spaCy, and when should I use each?",
            "Show me how to remove stopwords from this text using NLTK.",
        ],
    ),
    dict(
        id="opencv",
        title="OpenCV",
        hook="The standard library for classical computer vision — image filtering, edge detection, and video processing — separate from deep-learning-based vision.",
        explanation=(
            "OpenCV (`cv2` in Python) provides highly optimized functions for reading, transforming, and "
            "analyzing images and video: resizing, color space conversion, edge detection, contour finding, and "
            "face detection with classical (non-deep-learning) algorithms like Haar cascades."
        ),
        code=dict(
            lang="python",
            label="Basic image processing pipeline",
            src=(
                "import cv2\n\n"
                "img = cv2.imread(\"photo.jpg\")\n"
                "gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)\n"
                "edges = cv2.Canny(gray, threshold1=100, threshold2=200)\n"
                "cv2.imwrite(\"edges.jpg\", edges)"
            ),
        ),
        example=(
            "A document-scanning app uses OpenCV's edge detection and contour finding to locate a paper's "
            "corners in a photo, then applies a perspective transform to flatten it — all classical computer vision, no neural network required."
        ),
        best_practices=[
            "Remember OpenCV reads images in BGR order by default, not RGB — a common source of 'my colors look wrong' bugs.",
            "Use classical OpenCV techniques for well-defined, controllable conditions; reach for a deep-learning model when the task involves messy, real-world variability.",
        ],
        pitfalls=[
            "Forgetting the BGR-vs-RGB color order when displaying an OpenCV image with a library (like Matplotlib) that expects RGB.",
        ],
        prompts=[
            "Why do my image colors look wrong after loading with OpenCV and displaying with Matplotlib?",
            "Show me how to detect and draw contours around objects in an image.",
        ],
    ),
    dict(
        id="pillow",
        title="Pillow (PIL)",
        hook="The go-to library for straightforward image manipulation in Python — opening, resizing, cropping, and format conversion.",
        explanation=(
            "Pillow (a maintained fork of the original PIL) handles everyday image tasks: opening and saving "
            "across formats (JPEG, PNG, WebP), resizing, cropping, rotating, and basic filters — simpler and "
            "more Pythonic than OpenCV for tasks that don't need computer-vision algorithms."
        ),
        code=dict(
            lang="python",
            label="Resize, watermark, and save",
            src=(
                "from PIL import Image, ImageDraw\n\n"
                "img = Image.open(\"photo.jpg\").convert(\"RGB\")\n"
                "img.thumbnail((800, 800))                 # resize, preserving aspect ratio\n\n"
                "draw = ImageDraw.Draw(img)\n"
                "draw.text((10, 10), \"(c) FINESE SCHOOL\", fill=\"white\")\n"
                "img.save(\"photo_resized.jpg\", quality=85)"
            ),
        ),
        example=(
            "A web app generating thumbnail versions of every user-uploaded image uses Pillow's `.thumbnail()` "
            "to resize on upload, keeping page load times fast without shipping full-resolution images to every visitor."
        ),
        best_practices=[
            "Use `.thumbnail()` (which preserves aspect ratio) rather than `.resize()` with hardcoded dimensions when you just need a smaller version.",
            "Convert images to `RGB` explicitly before saving as JPEG — some source formats (like PNG with transparency) will error otherwise.",
        ],
        pitfalls=[
            "Saving a PNG with an alpha channel directly as JPEG without converting to RGB first, causing an error.",
        ],
        prompts=[
            "How do I batch-resize a folder of images with Pillow?",
            "What's the difference between Pillow's resize() and thumbnail() methods?",
        ],
    ),
    dict(
        id="selenium",
        title="Selenium",
        hook="Automates a real browser — clicking, typing, scrolling — for testing web apps or scraping sites that require JavaScript to render.",
        explanation=(
            "Selenium controls an actual browser (Chrome, Firefox) programmatically, which lets it interact with "
            "pages the way a real user would: clicking buttons, filling forms, waiting for JavaScript-rendered "
            "content to appear. This makes it essential for testing dynamic web apps and scraping sites that "
            "BeautifulSoup alone can't handle, since BeautifulSoup only sees the initial HTML, not what JavaScript later renders."
        ),
        code=dict(
            lang="python",
            label="Automating a login and reading the result",
            src=(
                "from selenium import webdriver\n"
                "from selenium.webdriver.common.by import By\n\n"
                "driver = webdriver.Chrome()\n"
                "driver.get(\"https://example.com/login\")\n"
                "driver.find_element(By.NAME, \"email\").send_keys(\"user@example.com\")\n"
                "driver.find_element(By.NAME, \"password\").send_keys(\"secret\")\n"
                "driver.find_element(By.CSS_SELECTOR, \"button[type=submit]\").click()\n\n"
                "driver.quit()"
            ),
        ),
        example=(
            "A QA team automates their app's checkout flow end-to-end with Selenium, running the same click-by-click "
            "sequence a real customer would on every deploy, catching UI regressions that unit tests can't."
        ),
        best_practices=[
            "Use explicit waits (`WebDriverWait`) for elements to appear instead of `time.sleep()`, which is both slower and less reliable.",
            "Run tests in headless mode in CI to avoid needing an actual visible browser window on the build server.",
        ],
        pitfalls=[
            "Using fixed `time.sleep()` calls to 'wait for the page,' which is flaky under variable network conditions.",
            "Writing brittle selectors tied to auto-generated class names that change on every deploy.",
        ],
        prompts=[
            "Why should I use WebDriverWait instead of time.sleep() in Selenium?",
            "Show me how to run a Selenium test in headless mode.",
        ],
    ),
    dict(
        id="scrapy",
        title="Scrapy",
        hook="A full web-scraping framework, not just a parsing library — built for crawling many pages at scale with retries, concurrency, and pipelines already handled.",
        explanation=(
            "Scrapy is a complete framework for building 'spiders' that crawl websites, follow links, and "
            "extract structured data, with built-in support for concurrency, request throttling, retries, and "
            "exporting results (JSON, CSV) — handling the operational complexity that a simple `requests` + "
            "`BeautifulSoup` script leaves entirely up to you."
        ),
        code=dict(
            lang="python",
            label="A minimal Scrapy spider",
            src=(
                "import scrapy\n\n"
                "class BlogSpider(scrapy.Spider):\n"
                "    name = \"blog\"\n"
                "    start_urls = [\"https://example.com/blog\"]\n\n"
                "    def parse(self, response):\n"
                "        for post in response.css(\"article.post\"):\n"
                "            yield {\n"
                "                \"title\": post.css(\"h2::text\").get(),\n"
                "                \"link\": post.css(\"a::attr(href)\").get(),\n"
                "            }\n"
                "        next_page = response.css(\"a.next::attr(href)\").get()\n"
                "        if next_page:\n"
                "            yield response.follow(next_page, self.parse)"
            ),
        ),
        example=(
            "A price comparison site crawls tens of thousands of product pages nightly with Scrapy, relying on "
            "its built-in concurrency and automatic retry-on-failure instead of hand-building that infrastructure."
        ),
        best_practices=[
            "Respect `robots.txt` and set a reasonable `DOWNLOAD_DELAY` to avoid overwhelming the target site.",
            "Use Scrapy's Item Pipelines to clean and validate scraped data in one central place rather than scattering logic across spiders.",
        ],
        pitfalls=[
            "Ignoring a site's crawl rate limits, risking an IP ban or violating terms of service.",
        ],
        prompts=[
            "How do I add a delay between requests in Scrapy to avoid overloading a site?",
            "What's the difference between using Scrapy versus requests + BeautifulSoup for a scraping project?",
        ],
    ),
    dict(
        id="streamlit",
        title="Streamlit",
        hook="Turns a plain Python script into an interactive web app in minutes, with no HTML, CSS, or JavaScript required.",
        explanation=(
            "Streamlit re-runs your entire script top to bottom every time a widget changes, and uses that "
            "simple mental model to let you build interactive data apps with plain Python function calls — "
            "`st.slider()`, `st.dataframe()`, `st.button()` — instead of a traditional frontend/backend split."
        ),
        code=dict(
            lang="python",
            label="A small interactive data app",
            src=(
                "import streamlit as st\n"
                "import pandas as pd\n\n"
                "st.title(\"Sales Explorer\")\n"
                "df = pd.read_csv(\"sales.csv\")\n\n"
                "region = st.selectbox(\"Region\", df[\"region\"].unique())\n"
                "filtered = df[df[\"region\"] == region]\n"
                "st.dataframe(filtered)\n"
                "st.bar_chart(filtered.groupby(\"month\")[\"revenue\"].sum())"
            ),
        ),
        example=(
            "A data scientist turns a Jupyter notebook analysis into a shareable internal tool for their team in "
            "under an hour with Streamlit, letting non-technical colleagues explore the data themselves instead of requesting a new chart each time."
        ),
        best_practices=[
            "Use `st.cache_data` to avoid re-running expensive data loading or computation on every widget interaction.",
            "Keep heavy computation out of the main script body when possible — Streamlit's rerun-on-interaction model means everything not cached re-executes constantly.",
        ],
        pitfalls=[
            "Loading a large dataset from disk on every interaction without caching, making the app feel sluggish.",
        ],
        prompts=[
            "How does st.cache_data work, and when should I use it?",
            "Turn this data analysis script into an interactive Streamlit app.",
        ],
    ),
    dict(
        id="pydantic",
        title="Pydantic",
        hook="Turns Python type hints into runtime data validation — catch a malformed input the moment it enters your system, with a clear error instead of a mysterious crash later.",
        explanation=(
            "Pydantic models are Python classes with type-annotated fields; instantiating one with invalid data "
            "(a string where an int was expected, a missing required field) raises a clear validation error "
            "immediately, rather than letting bad data silently propagate deeper into the system. It's the "
            "validation layer underneath FastAPI's automatic request parsing."
        ),
        code=dict(
            lang="python",
            label="Validating incoming data with a model",
            src=(
                "from pydantic import BaseModel, EmailStr, field_validator\n\n"
                "class SignupRequest(BaseModel):\n"
                "    email: EmailStr\n"
                "    age: int\n\n"
                "    @field_validator(\"age\")\n"
                "    @classmethod\n"
                "    def must_be_adult(cls, v):\n"
                "        if v < 18:\n"
                "            raise ValueError(\"Must be 18 or older\")\n"
                "        return v\n\n"
                "SignupRequest(email=\"not-an-email\", age=15)   # raises ValidationError immediately"
            ),
        ),
        example=(
            "An API endpoint accepting user signups uses a Pydantic model to reject a malformed email or "
            "underage signup with a precise, structured error response before any of that data ever touches the database."
        ),
        best_practices=[
            "Define API request/response shapes as Pydantic models instead of raw dicts to get validation and self-documentation together.",
            "Use custom validators (`field_validator`) for business-rule checks (like age limits) rather than validating manually after parsing.",
        ],
        pitfalls=[
            "Bypassing the model and working with raw, unvalidated dicts 'just this once,' reintroducing the exact class of bug Pydantic exists to prevent.",
        ],
        prompts=[
            "Add a custom validator to this Pydantic model that checks a date range.",
            "What's the difference between Pydantic v1 and v2 in how validation is defined?",
        ],
    ),
]
