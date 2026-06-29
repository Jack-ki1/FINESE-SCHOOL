"""
FINESE SCHOOL - Global Configuration
"""
import os
from datetime import timedelta

# ── Flask ──────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me-in-production')
SESSION_TYPE = 'filesystem'
SESSION_PERMANENT = True
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

# ── LLM Provider API Keys ─────────────────────────────────────────
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')
HF_TOKEN = os.environ.get('HF_TOKEN', '')

# ── Default Model Settings ────────────────────────────────────────
DEFAULT_MODEL_PROVIDER = 'openai'
DEFAULT_OPENAI_MODEL = 'gpt-4o-mini'
DEFAULT_ANTHROPIC_MODEL = 'claude-3-haiku-20240307'
DEFAULT_GOOGLE_MODEL = 'gemini-1.5-flash'
DEFAULT_HF_MODEL = 'mistralai/Mistral-7B-Instruct-v0.3'
DEFAULT_OLLAMA_MODEL = 'llama3.2'

# ── Generation Parameters ─────────────────────────────────────────
DEFAULT_MAX_TOKENS = 1024
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 1.0

# ── Chat Settings ─────────────────────────────────────────────────
MAX_CONVERSATIONS = 50
MAX_MESSAGES_PER_CONVERSATION = 200
SYSTEM_MESSAGE_MAX_LENGTH = 2000

# ── File Upload ───────────────────────────────────────────────────
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'docx', 'csv', 'json', 'py', 'md',
    'xlsx', 'xls', 'sql', 'r', 'ipynb', 'yaml', 'yml', 'xml', 'html'
}
UPLOAD_FOLDER = 'static/uploads'

# ── Database ──────────────────────────────────────────────────────
BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(BASEDIR, 'finese_school.db')}")

# ── Code Execution ────────────────────────────────────────────────
CODE_EXEC_TIMEOUT = int(os.environ.get('CODE_EXEC_TIMEOUT', '30'))
CODE_EXEC_MAX_OUTPUT = 50000  # max chars from code execution

# ── Vector DB / RAG ──────────────────────────────────────────────
VECTORDB_PATH = os.path.join(BASEDIR, 'data', 'vectordb')
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')

# ── Education ─────────────────────────────────────────────────────
LEARNING_PATHS = [
    {
        'id': 'sql-fundamentals',
        'title': 'SQL Fundamentals',
        'description': 'Master SQL from basic queries to advanced analytics',
        'icon': 'bi-database',
        'modules': [
            {'id': 'sql-1', 'title': 'SELECT & Filtering', 'difficulty': 'beginner'},
            {'id': 'sql-2', 'title': 'JOINs & Relationships', 'difficulty': 'beginner'},
            {'id': 'sql-3', 'title': 'Aggregation & Grouping', 'difficulty': 'intermediate'},
            {'id': 'sql-4', 'title': 'Subqueries & Window Functions', 'difficulty': 'intermediate'},
            {'id': 'sql-5', 'title': 'Query Optimization', 'difficulty': 'advanced'},
        ]
    },
    {
        'id': 'python-data',
        'title': 'Python for Data',
        'description': 'Data analysis with pandas, numpy, and matplotlib',
        'icon': 'bi-filetype-py',
        'modules': [
            {'id': 'py-1', 'title': 'Python Basics for Data', 'difficulty': 'beginner'},
            {'id': 'py-2', 'title': 'Pandas DataFrames', 'difficulty': 'beginner'},
            {'id': 'py-3', 'title': 'Data Cleaning', 'difficulty': 'intermediate'},
            {'id': 'py-4', 'title': 'Visualization with Matplotlib', 'difficulty': 'intermediate'},
            {'id': 'py-5', 'title': 'Statistical Analysis', 'difficulty': 'advanced'},
        ]
    },
    {
        'id': 'data-viz',
        'title': 'Data Visualization',
        'description': 'Create compelling visualizations and dashboards',
        'icon': 'bi-bar-chart',
        'modules': [
            {'id': 'viz-1', 'title': 'Chart Selection Guide', 'difficulty': 'beginner'},
            {'id': 'viz-2', 'title': 'Plotly Interactive Charts', 'difficulty': 'intermediate'},
            {'id': 'viz-3', 'title': 'Dashboard Design', 'difficulty': 'advanced'},
        ]
    },
    {
        'id': 'ml-basics',
        'title': 'Machine Learning Basics',
        'description': 'Introduction to ML concepts and scikit-learn',
        'icon': 'bi-cpu',
        'modules': [
            {'id': 'ml-1', 'title': 'What is ML?', 'difficulty': 'beginner'},
            {'id': 'ml-2', 'title': 'Regression', 'difficulty': 'intermediate'},
            {'id': 'ml-3', 'title': 'Classification', 'difficulty': 'intermediate'},
            {'id': 'ml-4', 'title': 'Model Evaluation', 'difficulty': 'advanced'},
        ]
    },
]
