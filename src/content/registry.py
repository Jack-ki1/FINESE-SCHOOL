"""
Central registry of every core topic on the platform.

Each entry defines the topic's identity (id, name, icon, accent color),
a short description, and a pointer to its SUBTOPICS list living in the
matching *_core.py module. This is the single source of truth the Flask
app reads to build navigation, theming, and page content — add a new
topic by writing a content module and adding one entry here.
"""

from src.content import (
    python_core,
    ai_core,
    sql_core,
    nosql_core,
    mcp_core,
    powerbi_core,
    ml_core,
    dl_core,
    dataviz_core,
    pylibs_core,
    git_core,
    dsa_core,
)

TOPICS = [
    dict(
        id="python",
        name="Python",
        icon="🐍",
        color="#2f6fed",
        tagline="Core language fundamentals",
        description="Variables, control flow, functions, OOP, comprehensions, decorators, error handling, and file I/O.",
        module=python_core,
    ),
    dict(
        id="ai",
        name="Artificial Intelligence",
        icon="🤖",
        color="#7c5cff",
        tagline="The big picture before the math",
        description="What AI actually is, how ML/DL relate to it, neural networks 101, prompting, generative AI, and ethics.",
        module=ai_core,
    ),
    dict(
        id="sql",
        name="SQL",
        icon="🗄️",
        color="#12a594",
        tagline="Relational databases & queries",
        description="SELECT/WHERE, joins, aggregations, subqueries & CTEs, window functions, and indexing.",
        module=sql_core,
    ),
    dict(
        id="nosql",
        name="NoSQL",
        icon="🍃",
        color="#3aa655",
        tagline="Beyond the relational table",
        description="Document, key-value, wide-column, and graph databases, plus CAP theorem and consistency models.",
        module=nosql_core,
    ),
    dict(
        id="mcp",
        name="MCP",
        icon="🔌",
        color="#ff8a3d",
        tagline="Model Context Protocol",
        description="What MCP is, its architecture, primitives (tools/resources/prompts), transports, and building a server.",
        module=mcp_core,
    ),
    dict(
        id="powerbi",
        name="Power BI",
        icon="📊",
        color="#f2b705",
        tagline="Business intelligence & DAX",
        description="The Power BI workflow, data modeling, DAX fundamentals, context transition, and time intelligence.",
        module=powerbi_core,
    ),
    dict(
        id="ml",
        name="Machine Learning",
        icon="🧠",
        color="#ef5da8",
        tagline="Classical ML with scikit-learn",
        description="Supervised vs. unsupervised learning, evaluation, leakage, feature engineering, and metrics.",
        module=ml_core,
    ),
    dict(
        id="dl",
        name="Deep Learning",
        icon="🕸️",
        color="#5b4de0",
        tagline="Neural networks in depth",
        description="Neurons & activations, backprop, CNNs, RNNs/LSTMs, and the transformer architecture.",
        module=dl_core,
    ),
    dict(
        id="dataviz",
        name="Data Visualization",
        icon="📈",
        color="#ff6b57",
        tagline="Communicating data clearly",
        description="Choosing chart types, Matplotlib/Seaborn, interactive Plotly, and color & accessibility.",
        module=dataviz_core,
    ),
    dict(
        id="pylibs",
        name="Python Libraries",
        icon="📦",
        color="#17b8c4",
        tagline="22+ libraries, one by one",
        description="A hands-on tour of the Python libraries you'll actually reach for, from NumPy to Pydantic.",
        module=pylibs_core,
    ),
    dict(
        id="git",
        name="Git & GitHub",
        icon="🌿",
        color="#f14e32",
        tagline="Version control that doesn't bite",
        description="Git's mental model, branching & merging, merge vs. rebase, remotes, and keeping a repo clean.",
        module=git_core,
    ),
    dict(
        id="dsa",
        name="Data Structures & Algorithms",
        icon="🧩",
        color="#64748b",
        tagline="Bonus: the foundations underneath it all",
        description="Big-O notation, arrays vs. linked lists, hash tables, and stacks & queues.",
        module=dsa_core,
    ),
]

TOPICS_BY_ID = {t["id"]: t for t in TOPICS}


def get_topic(topic_id: str):
    """Return a topic's registry entry, or None if it doesn't exist."""
    return TOPICS_BY_ID.get(topic_id)


def get_subtopics(topic_id: str):
    """Return the list of subtopic dicts for a topic, or [] if unknown."""
    topic = get_topic(topic_id)
    return topic["module"].SUBTOPICS if topic else []


def get_subtopic(topic_id: str, subtopic_id: str):
    """Return one subtopic dict, or None if the topic/subtopic doesn't exist."""
    for s in get_subtopics(topic_id):
        if s["id"] == subtopic_id:
            return s
    return None


def total_subtopic_count() -> int:
    return sum(len(t["module"].SUBTOPICS) for t in TOPICS)
