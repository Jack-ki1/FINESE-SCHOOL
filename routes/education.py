"""
Education Routes - Learning paths, exercises, progress tracking.
Blueprint prefix: /learn
"""
import json
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify, session, render_template

logger = logging.getLogger(__name__)
education_bp = Blueprint('education', __name__)

# ── Exercise Bank ──────────────────────────────────────────────────
EXERCISES = {
    'sql-1': [
        {
            'id': 'sql-1-1',
            'title': 'Select All Customers',
            'description': 'Write a SQL query to select all customers from the customers table.',
            'difficulty': 'beginner',
            'hint': 'Use SELECT * FROM table_name',
            'expected_answer': 'SELECT * FROM customers',
            'explanation': 'SELECT * selects all columns, FROM customers specifies the table.',
        },
        {
            'id': 'sql-1-2',
            'title': 'Filter by City',
            'description': 'Write a SQL query to select all customers from New York.',
            'difficulty': 'beginner',
            'hint': 'Use WHERE clause with city column',
            'expected_answer': "SELECT * FROM customers WHERE city = 'New York'",
            'explanation': 'WHERE filters rows based on a condition. String values need quotes.',
        },
        {
            'id': 'sql-1-3',
            'title': 'Select Specific Columns',
            'description': 'Write a query to get only the name and email of all customers.',
            'difficulty': 'beginner',
            'hint': 'List column names after SELECT',
            'expected_answer': 'SELECT name, email FROM customers',
            'explanation': 'Instead of *, list specific column names to select only those columns.',
        },
    ],
    'sql-2': [
        {
            'id': 'sql-2-1',
            'title': 'Join Orders with Customers',
            'description': 'Write a query to show order IDs with customer names.',
            'difficulty': 'beginner',
            'hint': 'Use INNER JOIN with ON clause',
            'expected_answer': 'SELECT o.id, c.name FROM orders o JOIN customers c ON o.customer_id = c.id',
            'explanation': 'JOIN combines rows from two tables based on a related column.',
        },
        {
            'id': 'sql-2-2',
            'title': 'Count Orders per Customer',
            'description': 'Show each customer name and their total number of orders.',
            'difficulty': 'intermediate',
            'hint': 'Use COUNT() with GROUP BY',
            'expected_answer': 'SELECT c.name, COUNT(o.id) as order_count FROM customers c LEFT JOIN orders o ON c.id = o.customer_id GROUP BY c.name',
            'explanation': 'GROUP BY groups rows, COUNT() counts them. LEFT JOIN includes customers with 0 orders.',
        },
    ],
    'sql-3': [
        {
            'id': 'sql-3-1',
            'title': 'Average Order Total',
            'description': 'Calculate the average total of all orders.',
            'difficulty': 'intermediate',
            'hint': 'Use AVG() aggregate function',
            'expected_answer': 'SELECT AVG(total) as avg_total FROM orders',
            'explanation': 'AVG() calculates the mean of a numeric column.',
        },
        {
            'id': 'sql-3-2',
            'title': 'Revenue by Category',
            'description': 'Calculate total revenue for each product category.',
            'difficulty': 'intermediate',
            'hint': 'Join order_items with products, GROUP BY category',
            'expected_answer': "SELECT p.category, SUM(oi.quantity * oi.unit_price) as revenue FROM order_items oi JOIN products p ON oi.product_id = p.id GROUP BY p.category ORDER BY revenue DESC",
            'explanation': 'Join tables, calculate revenue per item, group by category, and sort.',
        },
    ],
    'py-1': [
        {
            'id': 'py-1-1',
            'title': 'Create a DataFrame',
            'description': 'Create a pandas DataFrame with columns: name, age, city. Include 3 rows of data.',
            'difficulty': 'beginner',
            'hint': 'Use pd.DataFrame({...}) or pd.DataFrame([list of dicts])',
            'expected_answer': "import pandas as pd\ndf = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie'], 'age': [25, 30, 35], 'city': ['NYC', 'LA', 'Chicago']})",
            'explanation': 'pd.DataFrame() creates a table-like structure from dictionaries or lists.',
        },
        {
            'id': 'py-1-2',
            'title': 'Filter Rows',
            'description': 'Given a DataFrame df, filter rows where age > 25.',
            'difficulty': 'beginner',
            'hint': 'Use boolean indexing: df[df["column"] > value]',
            'expected_answer': 'result = df[df["age"] > 25]',
            'explanation': 'Boolean indexing creates a mask and filters rows that match the condition.',
        },
    ],
    'py-2': [
        {
            'id': 'py-2-1',
            'title': 'GroupBy Aggregation',
            'description': 'Group a DataFrame by city and calculate the mean age for each city.',
            'difficulty': 'intermediate',
            'hint': 'Use df.groupby("column")["column"].mean()',
            'expected_answer': 'result = df.groupby("city")["age"].mean()',
            'explanation': 'groupby() splits data by a column, then you apply aggregation functions.',
        },
    ],
    'viz-1': [
        {
            'id': 'viz-1-1',
            'title': 'Choose the Right Chart',
            'description': 'You want to show the distribution of ages in a dataset. Which chart type is best?',
            'difficulty': 'beginner',
            'hint': 'Think about showing frequency of values in ranges',
            'expected_answer': 'histogram',
            'explanation': 'Histograms show the distribution of a single numeric variable by binning values into ranges.',
        },
    ],
    'ml-1': [
        {
            'id': 'ml-1-1',
            'title': 'Supervised vs Unsupervised',
            'description': 'Is predicting house prices based on features like size and location supervised or unsupervised learning?',
            'difficulty': 'beginner',
            'hint': 'Do we have labeled training data?',
            'expected_answer': 'supervised',
            'explanation': 'Predicting a target variable (price) from features is supervised learning - we train on labeled examples.',
        },
    ],
}


@education_bp.route('/')
def learning_hub():
    """Main learning hub page."""
    from config import LEARNING_PATHS
    sid = session.get('session_id', 'anon')

    # Get progress
    from models.learning import LearningProgress
    progress_records = LearningProgress.query.filter_by(session_id=sid).all()
    progress_map = {f"{p.path_id}:{p.module_id}": p.status for p in progress_records}

    return render_template('learning.html', paths=LEARNING_PATHS, progress=progress_map)


@education_bp.route('/api/paths', methods=['GET'])
def get_paths():
    """Get all learning paths with progress."""
    from config import LEARNING_PATHS
    sid = session.get('session_id', 'anon')

    from models.learning import LearningProgress
    progress_records = LearningProgress.query.filter_by(session_id=sid).all()
    progress_map = {}
    for p in progress_records:
        key = f"{p.path_id}:{p.module_id}"
        progress_map[key] = {'status': p.status, 'score': p.score}

    result = []
    for path in LEARNING_PATHS:
        path_data = {**path, 'modules': []}
        completed = 0
        for module in path['modules']:
            key = f"{path['id']}:{module['id']}"
            status = progress_map.get(key, {}).get('status', 'not_started')
            if status == 'completed':
                completed += 1
            path_data['modules'].append({**module, 'status': status})
        path_data['progress_pct'] = round(completed / len(path['modules']) * 100) if path['modules'] else 0
        result.append(path_data)

    return jsonify({'paths': result})


@education_bp.route('/api/modules/<module_id>/exercises', methods=['GET'])
def get_exercises(module_id):
    """Get exercises for a module."""
    exercises = EXERCISES.get(module_id, [])
    return jsonify({'exercises': exercises})


@education_bp.route('/api/exercises/<exercise_id>/check', methods=['POST'])
def check_exercise(exercise_id):
    """Check an exercise answer."""
    data = request.get_json() or {}
    user_answer = data.get('answer', '').strip()

    # Find the exercise
    exercise = None
    for module_exercises in EXERCISES.values():
        for ex in module_exercises:
            if ex['id'] == exercise_id:
                exercise = ex
                break
        if exercise:
            break

    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404

    # Simple comparison (normalize whitespace and case for SQL)
    expected = exercise['expected_answer'].strip().lower().replace('  ', ' ')
    actual = user_answer.strip().lower().replace('  ', ' ')
    correct = expected == actual

    # Record attempt
    from models import db
    from models.learning import ExerciseAttempt
    sid = session.get('session_id', 'anon')
    attempt = ExerciseAttempt(
        session_id=sid,
        module_id=exercise_id.rsplit('-', 1)[0],
        exercise_id=exercise_id,
        user_answer=user_answer,
        correct=correct,
        feedback=exercise['explanation'] if not correct else 'Correct!',
    )
    db.session.add(attempt)

    # Update progress
    module_id = exercise_id.rsplit('-', 1)[0]
    path_id = '-'.join(module_id.split('-')[:-1])
    progress = LearningProgress.query.filter_by(
        session_id=sid, path_id=path_id, module_id=module_id
    ).first()

    if not progress:
        progress = LearningProgress(session_id=sid, path_id=path_id, module_id=module_id)
        db.session.add(progress)

    progress.status = 'completed' if correct else 'in_progress'
    if correct:
        progress.score = 100
        progress.completed_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        'correct': correct,
        'feedback': exercise['explanation'],
        'hint': exercise['hint'] if not correct else None,
        'expected': exercise['expected_answer'] if not correct else None,
    })


@education_bp.route('/api/exercises/<exercise_id>/hint', methods=['GET'])
def get_hint(exercise_id):
    """Get a hint for an exercise."""
    for module_exercises in EXERCISES.values():
        for ex in module_exercises:
            if ex['id'] == exercise_id:
                return jsonify({'hint': ex['hint']})
    return jsonify({'error': 'Exercise not found'}), 404


@education_bp.route('/api/progress', methods=['GET'])
def get_progress():
    """Get overall learning progress."""
    sid = session.get('session_id', 'anon')
    from models.learning import LearningProgress
    records = LearningProgress.query.filter_by(session_id=sid).all()

    from config import LEARNING_PATHS
    result = {}
    for path in LEARNING_PATHS:
        path_progress = {'path_id': path['id'], 'modules': {}}
        for module in path['modules']:
            rec = next((r for r in records if r.path_id == path['id'] and r.module_id == module['id']), None)
            path_progress['modules'][module['id']] = {
                'status': rec.status if rec else 'not_started',
                'score': rec.score if rec else 0,
            }
        completed = sum(1 for m in path_progress['modules'].values() if m['status'] == 'completed')
        path_progress['progress_pct'] = round(completed / len(path['modules']) * 100) if path['modules'] else 0
        result[path['id']] = path_progress

    return jsonify({'progress': result})


@education_bp.route('/api/ai-tutor', methods=['POST'])
def ai_tutor():
    """Get AI tutoring help for a topic."""
    data = request.get_json() or {}
    question = data.get('question', '').strip()
    module_id = data.get('module_id', '')
    context = data.get('context', '')

    if not question:
        return jsonify({'error': 'question is required'}), 400

    system_prompt = """You are a patient and knowledgeable data science tutor at FINESE SCHOOL.
Help students understand SQL, Python, data visualization, and machine learning concepts.
- Explain concepts clearly with examples
- Use simple analogies when possible
- Provide code examples when relevant
- Encourage the student to think critically
- Keep responses concise but thorough"""

    user_msg = question
    if module_id:
        user_msg = f"[Topic: {module_id}]\n\n{question}"
    if context:
        user_msg = f"[Student's work so far:\n{context}]\n\n{question}"

    from services.llm_service import LLMService
    try:
        provider = LLMService.get_provider(
            data.get('provider', 'openai'),
            model=data.get('model')
        )
        response = provider.chat([
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_msg},
        ], temperature=0.5, max_tokens=1000)

        return jsonify({'success': True, 'response': response.content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
