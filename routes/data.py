"""
Data Routes - SQL execution, code execution, data analysis, visualization.
Blueprint prefix: /data
"""
import json
import logging
from flask import Blueprint, request, jsonify, session
import uuid

logger = logging.getLogger(__name__)
data_bp = Blueprint('data', __name__)

# ── Singleton services ─────────────────────────────────────────────
_db_service = None
_code_executor = None
_data_analyzer = None


def _get_db_service():
    global _db_service
    if _db_service is None:
        from core.database_service import DatabaseService
        _db_service = DatabaseService()
    return _db_service


def _get_code_executor():
    global _code_executor
    if _code_executor is None:
        from core.code_executor import CodeExecutor
        _code_executor = CodeExecutor()
    return _code_executor


def _get_data_analyzer():
    global _data_analyzer
    if _data_analyzer is None:
        from core.data_analyzer import DataAnalyzer
        _data_analyzer = DataAnalyzer()
    return _data_analyzer


# ═══════════════════════════════════════════════════════════════════
# DATABASE CONNECTIONS
# ═══════════════════════════════════════════════════════════════════

@data_bp.route('/connections', methods=['GET'])
def list_connections():
    """List available database connections."""
    from models import db
    from models.database_connection import DatabaseConnection
    sid = session.get('session_id', 'anon')
    conns = DatabaseConnection.query.filter_by(session_id=sid).all()
    return jsonify({'connections': [c.to_dict() for c in conns]})


@data_bp.route('/connections', methods=['POST'])
def create_connection():
    """Create a new database connection."""
    from models import db
    from models.database_connection import DatabaseConnection
    data = request.get_json() or {}
    sid = session.get('session_id', 'anon')

    name = data.get('name', '').strip()
    db_type = data.get('db_type', 'sqlite')
    conn_str = data.get('connection_string', '')

    if not name:
        return jsonify({'error': 'Connection name is required'}), 400

    # For SQLite, build connection string from path
    if db_type == 'sqlite' and not conn_str:
        path = data.get('path', 'finese_data.db')
        conn_str = f'sqlite:///{path}'

    db_svc = _get_db_service()
    test_result = db_svc.connect(name, conn_str)

    if not test_result['success']:
        return jsonify(test_result), 400

    # Save to database
    conn = DatabaseConnection(
        session_id=sid,
        name=name,
        db_type=db_type,
        connection_string=conn_str,
        is_default=data.get('is_default', False),
    )
    db.session.add(conn)
    db.session.commit()

    return jsonify({'success': True, 'connection': conn.to_dict()})


@data_bp.route('/connections/<conn_id>', methods=['DELETE'])
def delete_connection(conn_id):
    """Delete a database connection."""
    from models import db
    from models.database_connection import DatabaseConnection
    conn = DatabaseConnection.query.get(conn_id)
    if not conn:
        return jsonify({'error': 'Connection not found'}), 404

    db_svc = _get_db_service()
    db_svc.disconnect(conn.name)
    db.session.delete(conn)
    db.session.commit()
    return jsonify({'success': True})


# ═══════════════════════════════════════════════════════════════════
# SQL EXECUTION
# ═══════════════════════════════════════════════════════════════════

@data_bp.route('/sql/execute', methods=['POST'])
def execute_sql():
    """Execute a SQL query against a connected database."""
    data = request.get_json() or {}
    connection_name = data.get('connection', '')
    sql = data.get('sql', '').strip()

    if not connection_name or not sql:
        return jsonify({'error': 'connection and sql are required'}), 400

    db_svc = _get_db_service()
    result = db_svc.execute_sql(connection_name, sql)
    return jsonify(result)


@data_bp.route('/sql/schema', methods=['GET'])
def get_schema():
    """Get database schema for a connection."""
    connection_name = request.args.get('connection', '')
    if not connection_name:
        return jsonify({'error': 'connection parameter required'}), 400

    db_svc = _get_db_service()
    schema = db_svc.get_schema(connection_name)
    return jsonify(schema)


@data_bp.route('/sql/schema-summary', methods=['GET'])
def get_schema_summary():
    """Get text summary of schema for LLM context."""
    connection_name = request.args.get('connection', '')
    if not connection_name:
        return jsonify({'error': 'connection parameter required'}), 400

    db_svc = _get_db_service()
    summary = db_svc.get_schema_summary(connection_name)
    return jsonify({'summary': summary})


@data_bp.route('/sql/generate', methods=['POST'])
def generate_sql():
    """Generate SQL from natural language using LLM."""
    data = request.get_json() or {}
    question = data.get('question', '').strip()
    connection_name = data.get('connection', '')

    if not question or not connection_name:
        return jsonify({'error': 'question and connection are required'}), 400

    db_svc = _get_db_service()
    schema_summary = db_svc.get_schema_summary(connection_name)
    prompt = db_svc.generate_natural_language_sql_prompt(question, schema_summary)

    # Use LLM to generate SQL
    from services.llm_service import LLMService
    try:
        provider = LLMService.get_provider(
            data.get('provider', 'openai'),
            model=data.get('model')
        )
        response = provider.chat([
            {'role': 'system', 'content': 'You are an expert SQL developer. Write only the SQL query, no explanations.'},
            {'role': 'user', 'content': prompt},
        ], temperature=0.1, max_tokens=500)

        return jsonify({
            'success': True,
            'sql': response.content.strip(),
            'question': question,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════════
# PYTHON CODE EXECUTION
# ═══════════════════════════════════════════════════════════════════

@data_bp.route('/code/execute', methods=['POST'])
def execute_code():
    """Execute Python code in sandboxed environment."""
    data = request.get_json() or {}
    code = data.get('code', '').strip()

    if not code:
        return jsonify({'error': 'code is required'}), 400

    executor = _get_code_executor()

    # Build context from uploaded datasets
    context = {}
    analyzer = _get_data_analyzer()
    datasets = analyzer.list_datasets()
    if datasets:
        context['dataframes'] = {}
        for ds in datasets:
            csv_content = analyzer.get_csv_content(ds['name'])
            if csv_content:
                context['dataframes'][ds['name'].replace(' ', '_')] = csv_content

    result = executor.execute_python(code, context)
    return jsonify(result)


@data_bp.route('/code/generate', methods=['POST'])
def generate_code():
    """Generate Python analysis code using LLM."""
    data = request.get_json() or {}
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'error': 'question is required'}), 400

    # Build data context
    analyzer = _get_data_analyzer()
    data_desc = '\n\n'.join(
        analyzer.get_description(ds['name']) for ds in analyzer.list_datasets()
    ) or 'No data loaded. User wants to write general Python code.'

    prompt = executor_prompt = f"""You are a data analysis expert. Write Python code using pandas to answer this question.

Available Data:
{data_desc}

Question: {question}

Rules:
1. Use pandas DataFrames that are already loaded (variable names match dataset names with spaces replaced by underscores)
2. Print results clearly
3. Handle errors gracefully

Python code:"""

    from services.llm_service import LLMService
    try:
        provider = LLMService.get_provider(
            data.get('provider', 'openai'),
            model=data.get('model')
        )
        response = provider.chat([
            {'role': 'system', 'content': 'You are an expert Python data analyst. Write only Python code, no explanations.'},
            {'role': 'user', 'content': prompt},
        ], temperature=0.1, max_tokens=1000)

        return jsonify({
            'success': True,
            'code': response.content.strip(),
            'question': question,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════════
# DATA ANALYSIS & VISUALIZATION
# ═══════════════════════════════════════════════════════════════════

@data_bp.route('/datasets', methods=['GET'])
def list_datasets():
    """List all loaded datasets."""
    analyzer = _get_data_analyzer()
    return jsonify({'datasets': analyzer.list_datasets()})


@data_bp.route('/datasets/<name>/profile', methods=['GET'])
def profile_dataset(name):
    """Get data profile for a dataset."""
    analyzer = _get_data_analyzer()
    ds = analyzer.get_dataset(name)
    if not ds:
        return jsonify({'error': f'Dataset {name} not found'}), 404
    return jsonify({'profile': ds['profile']})


@data_bp.route('/datasets/<name>/visualize', methods=['GET'])
def auto_visualize(name):
    """Auto-generate visualization for a dataset."""
    analyzer = _get_data_analyzer()
    chart = analyzer.auto_visualize(name)
    if not chart:
        return jsonify({'error': 'Could not generate visualization'}), 400
    return jsonify(chart)


@data_bp.route('/chart', methods=['POST'])
def generate_chart():
    """Generate a specific chart type."""
    data = request.get_json() or {}
    chart_type = data.get('type', 'bar')
    chart_data = data.get('data', {})
    title = data.get('title', '')

    analyzer = _get_data_analyzer()
    spec = analyzer.generate_chart_spec(chart_type, chart_data, title)
    return jsonify(spec)


@data_bp.route('/analyze', methods=['POST'])
def analyze_data():
    """AI-powered data analysis - ask questions about uploaded data."""
    data = request.get_json() or {}
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'error': 'question is required'}), 400

    analyzer = _get_data_analyzer()
    data_desc = '\n\n'.join(
        analyzer.get_description(ds['name']) for ds in analyzer.list_datasets()
    )

    if not data_desc:
        return jsonify({'error': 'No datasets loaded. Upload a CSV first.'}), 400

    from services.llm_service import LLMService
    try:
        provider = LLMService.get_provider(
            data.get('provider', 'openai'),
            model=data.get('model')
        )
        response = provider.chat([
            {'role': 'system', 'content': 'You are a data analysis expert. Analyze the data and provide clear insights.'},
            {'role': 'user', 'content': f'Data:\n{data_desc}\n\nQuestion: {question}'},
        ], temperature=0.3, max_tokens=1500)

        return jsonify({
            'success': True,
            'analysis': response.content,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════════
# SAMPLE DATABASE
# ═══════════════════════════════════════════════════════════════════

@data_bp.route('/sample-db', methods=['POST'])
def create_sample_db():
    """Create a sample SQLite database for demos and exercises."""
    db_svc = _get_db_service()
    path = db_svc.create_sample_sqlite()
    return jsonify({
        'success': True,
        'path': path,
        'message': 'Sample database created with customers, products, orders, order_items tables',
        'connection': 'sample_db',
    })
