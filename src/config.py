import os
from typing import Dict, List, Literal
from pydantic import BaseModel

class TopicSpec(BaseModel):
    name: str
    description: str
    domain: Literal["programming", "analysis", "visualization", "bi", "ml", "dl"]
    allowed_libraries: List[str]
    banned_topics: List[str]  # e.g., web dev, mobile
    style_guide: str 


TOPIC_REGISTRY = {
    "Python": TopicSpec(
        name="Python",
        description="Core Python: data structures, functions, decorators, context managers, type hints, performance.",
        domain="programming",
        allowed_libraries=["builtins", "collections", "itertools", "functools", "pathlib", "json"],
        banned_topics=["Django", "Flask", "GUI", "web scraping", "APIs"],
        style_guide="Be concise. Prefer standard library. Use type hints. Show 1-2 line examples unless complex."
    ),
    "Data Analysis with Pandas & NumPy": TopicSpec(
        name="Data Analysis with Pandas & NumPy",
        description="Data wrangling, vectorization, time series, memory optimization.",
        domain="analysis",
        allowed_libraries=["pandas", "numpy", "polars"],
        banned_topics=["web", "streaming", "big data frameworks"],
        style_guide="Always show DataFrame/Series input and output. Use .head() in examples. Avoid chained indexing."
    ),
    "SQL": TopicSpec(
        name="SQL",
        description="ANSI SQL with focus on PostgreSQL/SQLite. Window functions, CTEs, optimization.",
        domain="analysis",
        allowed_libraries=[],
        banned_topics=["ORM", "NoSQL", "MongoDB"],
        style_guide="Use explicit JOINs. Prefer CTEs over subqueries. Comment on performance implications."
    ),
    "Power BI": TopicSpec(
        name="Power BI",
        description="DAX formulas, data modeling, relationships, performance tuning.",
        domain="bi",
        allowed_libraries=[],
        banned_topics=["Tableau", "Looker", "Python scripts in PBI"],
        style_guide="Explain DAX logic step-by-step. Use VAR for readability. Warn about context transition gotchas."
    ),
    "Machine Learning": TopicSpec(
        name="Machine Learning",
        description="Scikit-learn, model evaluation, feature engineering, interpretability.",
        domain="ml",
        allowed_libraries=["sklearn", "xgboost", "lightgbm", "shap", "eli5"],
        banned_topics=["LLMs", "neural nets", "PyTorch/TensorFlow"],
        style_guide="Use pipelines. Show cross-validation. Emphasize data leakage prevention."
    ),
    "Deep Learning": TopicSpec(
        name="Deep Learning",
        description="Neural networks with TensorFlow/PyTorch: CNNs, RNNs, transformers basics.",
        domain="dl",
        allowed_libraries=["torch", "tensorflow", "keras", "transformers"],
        banned_topics=["web deployment", "mobile"],
        style_guide="Use high-level APIs (e.g., tf.keras). Show model.summary(). Include input shape."
    ),
    "Data Visualization": TopicSpec(
        name="Data Visualization",
        description="Effective static & interactive plots for insight communication.",
        domain="visualization",
        allowed_libraries=["matplotlib", "seaborn", "plotly", "altair"],
        banned_topics=["D3.js", "web dashboards beyond Plotly"],
        style_guide="Explain design choices (color, scale). Prefer Plotly for interactivity. Avoid pie charts."
    ),
}

# Add validation for model configuration
# Default to a more current and widely available model based on API type
API_TYPE = os.getenv("API_TYPE", "huggingface").lower()

if API_TYPE == "google":
    DEFAULT_MODEL = "gemini-1.5-flash"
elif API_TYPE == "openai":
    DEFAULT_MODEL = "gpt-3.5-turbo"
else:  # huggingface
    DEFAULT_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

MODEL_NAME = os.getenv("MODEL_NAME", DEFAULT_MODEL)

# Ensure that the model name is valid
if not MODEL_NAME:
    MODEL_NAME = DEFAULT_MODEL

try:
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
except ValueError:
    TEMPERATURE = 0.3

try:
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
except ValueError:
    MAX_TOKENS = 2048

# Validate temperature range
if TEMPERATURE < 0 or TEMPERATURE > 1:
    TEMPERATURE = 0.3

# Validate max tokens range
if MAX_TOKENS < 1 or MAX_TOKENS > 8192:
    MAX_TOKENS = 2048