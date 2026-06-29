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


@education_bp.route('/api/modules/<module_id>/quiz', methods=['GET'])
def get_quiz(module_id):
    """Generate a quiz for a specific module."""
    # First, try to get existing exercises for the module
    existing_exercises = EXERCISES.get(module_id, [])
    
    # If no existing exercises, generate new ones using LLM
    if not existing_exercises:
        from services.llm_service import LLMService
        try:
            # Get module information to generate relevant questions
            from config import LEARNING_PATHS
            module_title = None
            module_desc = None
            
            for path in LEARNING_PATHS:
                for module in path['modules']:
                    if module['id'] == module_id:
                        module_title = module['title']
                        module_desc = path['description']
                        break
                if module_title:
                    break
            
            if module_title:
                # Generate quiz questions using LLM
                system_prompt = f"""You are an expert educator creating quiz questions for a learning module.
                Module: {module_title}
                Description: {module_desc}
                
                Create 3-5 quiz questions appropriate for this module. Return the questions in JSON format:
                {{
                  "questions": [
                    {{
                      "id": "unique_id",
                      "type": "multiple_choice|true_false|short_answer",
                      "question": "The question text",
                      "options": ["option1", "option2", ...], // for multiple choice
                      "correct_answer": "the correct answer",
                      "explanation": "Explanation of the correct answer",
                      "difficulty": "beginner|intermediate|advanced"
                    }}
                  ]
                }}
                
                Make questions appropriate for the specified difficulty level and relevant to the module content."""
                
                user_prompt = f"Generate quiz questions for module '{module_title}' described as '{module_desc}'."
                
                provider = LLMService.get_provider('openai')
                response = provider.chat([
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt},
                ], temperature=0.3, max_tokens=1000)
                
                import re
                import ast
                # Extract JSON from response
                json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
                if json_match:
                    quiz_data = ast.literal_eval(json_match.group())
                    generated_questions = quiz_data.get('questions', [])
                    
                    # Format for response
                    quiz_questions = []
                    for i, q in enumerate(generated_questions):
                        quiz_questions.append({
                            'id': f"gen-{module_id}-{i+1}",
                            'title': q.get('question', ''),
                            'description': q.get('question', ''),
                            'difficulty': q.get('difficulty', 'beginner'),
                            'hint': q.get('explanation', ''),
                            'expected_answer': q.get('correct_answer', ''),
                            'explanation': q.get('explanation', ''),
                            'options': q.get('options', []),
                            'type': q.get('type', 'short_answer')
                        })
                    
                    return jsonify({'exercises': quiz_questions})
                else:
                    # Fallback to empty quiz
                    return jsonify({'exercises': []})
            else:
                return jsonify({'exercises': []})
        except Exception as e:
            logger.error(f"Error generating quiz: {e}")
            return jsonify({'exercises': []})
    else:
        # Return existing exercises as quiz
        return jsonify({'exercises': existing_exercises})


@education_bp.route('/api/exercises/<exercise_id>/check', methods=['POST'])
def check_exercise(exercise_id):
    """Check an exercise answer and track accuracy metrics."""
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

    # Special handling for different question types
    if exercise.get('type') == 'multiple_choice':
        correct = actual == exercise['expected_answer'].lower()
    elif exercise.get('type') == 'true_false':
        correct = (actual.startswith('true') or actual.startswith('yes')) == exercise['expected_answer'].lower().startswith('true')
    elif exercise.get('type') == 'short_answer':
        # For short answers, we could use LLM evaluation
        correct = evaluate_free_text_answer(exercise['expected_answer'], user_answer)

    # Record attempt with accuracy metrics
    from models import db
    from models.learning import ExerciseAttempt
    sid = session.get('session_id', 'anon')
    module_id = exercise_id.rsplit('-', 1)[0]
    path_id = '-'.join(module_id.split('-')[:-1])
    
    # Get previous attempts for accuracy calculation
    previous_attempts = ExerciseAttempt.query.filter_by(
        session_id=sid, exercise_id=exercise_id
    ).count()
    
    attempt = ExerciseAttempt(
        session_id=sid,
        module_id=module_id,
        exercise_id=exercise_id,
        user_answer=user_answer,
        correct=correct,
        feedback=exercise['explanation'] if not correct else 'Correct!',
        attempt_number=previous_attempts + 1
    )
    db.session.add(attempt)

    # Update progress with accuracy tracking
    progress = LearningProgress.query.filter_by(
        session_id=sid, path_id=path_id, module_id=module_id
    ).first()

    if not progress:
        progress = LearningProgress(session_id=sid, path_id=path_id, module_id=module_id)
        db.session.add(progress)

    # Update completion status based on correctness
    if correct:
        progress.status = 'completed'
        progress.score = 100
        progress.completed_at = datetime.utcnow()
    elif progress.status != 'completed':
        progress.status = 'in_progress'

    # Update overall statistics
    progress.total_attempts = (progress.total_attempts or 0) + 1
    if correct:
        progress.correct_attempts = (progress.correct_attempts or 0) + 1
    
    # Calculate current accuracy percentage
    if progress.total_attempts > 0:
        progress.accuracy_pct = (progress.correct_attempts or 0) / progress.total_attempts * 100

    db.session.commit()

    # Track prediction accuracy using the Accuracy Tracker service
    try:
        from services.accuracy_tracker import get_accuracy_tracker
        
        # Get student ID from session or use anonymous
        student_id = session.get('user_id', 0)
        if not student_id:
            # Use hash of session_id as temporary student identifier
            import hashlib
            student_id = int(hashlib.md5(sid.encode()).hexdigest()[:8], 16)
        
        tracker = get_accuracy_tracker()
        
        # Estimate predicted mastery based on user's progress and difficulty level
        base_prediction = 0.5
        if progress:
            if progress.accuracy_pct is not None:
                # Use historical accuracy as base prediction
                base_prediction = progress.accuracy_pct / 100.0
            elif progress.score is not None:
                # Use progress score if available
                base_prediction = progress.score / 100.0
        
        # Adjust prediction based on exercise difficulty
        difficulty = exercise.get('difficulty', 'beginner')
        difficulty_multiplier = {
            'beginner': 1.0,
            'intermediate': 0.8,
            'advanced': 0.6
        }
        predicted_mastery = base_prediction * difficulty_multiplier.get(difficulty, 0.8)
        
        # Cap predictions between reasonable bounds
        predicted_mastery = max(0.2, min(0.95, predicted_mastery))
        
        # Actual mastery is 1.0 for correct, 0.0 for incorrect
        actual_mastery = 1.0 if correct else 0.0
        
        # Calculate confidence based on amount of historical data
        confidence_score = 0.3
        if progress.total_attempts and progress.total_attempts > 5:
            confidence_score = 0.7
        elif progress.total_attempts and progress.total_attempts > 1:
            confidence_score = 0.5
            
        tracker.record_prediction(
            student_id=student_id,
            prediction_type='mastery',
            predicted_value=predicted_mastery,
            actual_value=actual_mastery,
            confidence_score=confidence_score,
            context={
                'exercise_id': exercise_id,
                'module_id': module_id,
                'path_id': path_id,
                'difficulty': difficulty,
                'attempt_number': previous_attempts + 1,
                'streak_length': calculate_streak_info(sid)['current_streak']
            }
        )
        
        logger.info(f"Recorded accuracy tracking for student {student_id}, exercise {exercise_id}")
    except Exception as e:
        logger.error(f"Error recording accuracy tracking: {e}")

    return jsonify({
        'correct': correct,
        'feedback': exercise['explanation'],
        'hint': exercise['hint'] if not correct else None,
        'expected': exercise['expected_answer'] if not correct else None,
        'attempt_number': previous_attempts + 1,
        'current_accuracy': progress.accuracy_pct if hasattr(progress, 'accuracy_pct') else None
    })


def evaluate_free_text_answer(expected: str, actual: str) -> bool:
    """Use LLM to evaluate free-text answers for more nuanced assessment."""
    from services.llm_service import LLMService
    
    system_prompt = """You are a strict but fair grader. 
    Evaluate whether the student's answer is correct compared to the expected answer.
    Respond with JSON only: {"correct": true/false, "feedback": "...", "score": 0.0-1.0}"""
    
    user_prompt = f"""Expected answer: {expected}
    Student's answer: {actual}
    Is the student's answer correct?"""
    
    try:
        provider = LLMService.get_provider('openai')
        response = provider.chat([
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ], temperature=0.1, max_tokens=300)
        
        import json
        import re
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return result.get('correct', False)
    except:
        # Fallback to simple string comparison
        pass
    
    # Fallback comparison
    return expected.lower().strip() == actual.lower().strip()


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
    """Get overall learning progress with accuracy metrics."""
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
                'total_attempts': rec.total_attempts if rec else 0,
                'correct_attempts': rec.correct_attempts if rec else 0,
                'accuracy_pct': rec.accuracy_pct if rec else 0,
                'attempts': len([a for a in ExerciseAttempt.query.filter_by(
                    session_id=sid, module_id=module['id']).all()])
            }
        completed = sum(1 for m in path_progress['modules'].values() if m['status'] == 'completed')
        path_progress['progress_pct'] = round(completed / len(path['modules']) * 100) if path['modules'] else 0
        result[path['id']] = path_progress

    return jsonify({'progress': result})


@education_bp.route('/api/accuracy-stats', methods=['GET'])
def get_accuracy_stats():
    """Get detailed accuracy statistics for the user."""
    sid = session.get('session_id', 'anon')
    from models.learning import LearningProgress, ExerciseAttempt
    
    # Get all progress records for this user
    progress_records = LearningProgress.query.filter_by(session_id=sid).all()
    
    # Calculate overall accuracy
    total_attempts = sum(p.total_attempts or 0 for p in progress_records)
    total_correct = sum(p.correct_attempts or 0 for p in progress_records)
    overall_accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
    
    # Calculate accuracy by path
    from config import LEARNING_PATHS
    path_accuracies = {}
    for path in LEARNING_PATHS:
        path_progress = [p for p in progress_records if p.path_id == path['id']]
        path_attempts = sum(p.total_attempts or 0 for p in path_progress)
        path_correct = sum(p.correct_attempts or 0 for p in path_progress)
        path_accuracy = (path_correct / path_attempts * 100) if path_attempts > 0 else 0
        
        path_accuracies[path['id']] = {
            'title': path['title'],
            'accuracy_pct': round(path_accuracy, 2),
            'total_attempts': path_attempts,
            'correct_attempts': path_correct
        }
    
    # Calculate accuracy by difficulty level
    difficulty_stats = {'beginner': {'attempts': 0, 'correct': 0}, 
                       'intermediate': {'attempts': 0, 'correct': 0},
                       'advanced': {'attempts': 0, 'correct': 0}}
    
    all_attempts = ExerciseAttempt.query.filter_by(session_id=sid).all()
    for attempt in all_attempts:
        # Find the exercise to get its difficulty
        exercise = None
        for module_exercises in EXERCISES.values():
            for ex in module_exercises:
                if ex['id'] == attempt.exercise_id:
                    exercise = ex
                    break
            if exercise:
                break
                
        if exercise:
            difficulty = exercise.get('difficulty', 'beginner')
            if difficulty in difficulty_stats:
                difficulty_stats[difficulty]['attempts'] += 1
                if attempt.correct:
                    difficulty_stats[difficulty]['correct'] += 1
    
    # Calculate percentages for difficulty stats
    for diff_level in difficulty_stats:
        attempts = difficulty_stats[diff_level]['attempts']
        correct = difficulty_stats[diff_level]['correct']
        difficulty_stats[diff_level]['accuracy_pct'] = (correct / attempts * 100) if attempts > 0 else 0
    
    return jsonify({
        'overall_accuracy': round(overall_accuracy, 2),
        'total_attempts': total_attempts,
        'total_correct': total_correct,
        'by_path': path_accuracies,
        'by_difficulty': difficulty_stats,
        'streak_info': calculate_streak_info(sid)  # Include streak information
    })


def calculate_streak_info(session_id: str) -> dict:
    """Calculate current and best streaks for a user."""
    from models.learning import ExerciseAttempt
    import datetime
    
    attempts = ExerciseAttempt.query.filter_by(session_id=session_id)\
                   .order_by(ExerciseAttempt.created_at.desc()).all()
    
    if not attempts:
        return {'current_streak': 0, 'best_streak': 0, 'last_attempt_date': None}
    
    # Calculate streaks
    current_streak = 0
    best_streak = 0
    today = datetime.date.today()
    
    for attempt in attempts:
        if attempt.correct:
            current_streak += 1
            best_streak = max(best_streak, current_streak)
        else:
            # Reset streak on incorrect answer
            current_streak = 0
    
    return {
        'current_streak': current_streak,
        'best_streak': best_streak,
        'last_attempt_date': attempts[0].created_at.date().isoformat()
    }


@education_bp.route('/api/ai-tutor', methods=['POST'])
def ai_tutor():
    """Get AI tutoring help for a topic."""
    data = request.get_json() or {}
    question = data.get('question', '').strip()
    module_id = data.get('module_id', '')
    context = data.get('context', '')

    if not question:
        return jsonify({'error': 'question is required'}), 400

    # Implement Socratic mode: encourage thinking rather than giving direct answers
    socratic_system_prompt = """You are a patient and knowledgeable data science tutor at FINESE SCHOOL.
    Your goal is to guide students to discover answers themselves using the Socratic method.
    - Ask probing questions that lead to the answer
    - Give hints rather than solutions
    - Encourage critical thinking
    - Help students understand concepts deeply
    - Only provide direct answers if the student is completely stuck after multiple attempts
    - Explain concepts clearly with examples when necessary
    - Use simple analogies when possible
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
            {'role': 'system', 'content': socratic_system_prompt},
            {'role': 'user', 'content': user_msg},
        ], temperature=0.5, max_tokens=1000)

        return jsonify({'success': True, 'response': response.content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@education_bp.route('/api/adapt-difficulty', methods=['POST'])
def adapt_difficulty():
    """Adjust module difficulty based on performance."""
    data = request.get_json() or {}
    module_id = data.get('module_id', '')
    performance_score = data.get('performance_score', 0)

    if not module_id:
        return jsonify({'error': 'module_id is required'}), 400

    # Determine if difficulty should be adjusted based on performance
    if performance_score < 0.6:  # Less than 60% correct
        suggestion = {
            'message': 'It seems you\'re finding this challenging. Consider reviewing foundational concepts first.',
            'recommendation': 'review',
            'next_module': 'prerequisite_material'  # Placeholder
        }
    elif performance_score > 0.8:  # More than 80% correct
        suggestion = {
            'message': 'Great job! You seem ready for more advanced material.',
            'recommendation': 'advance',
            'next_module': 'advanced_topic'  # Placeholder
        }
    else:
        suggestion = {
            'message': 'Good progress! Continue with the current pace.',
            'recommendation': 'continue',
            'next_module': 'current_path'
        }

    return jsonify(suggestion)


@education_bp.route('/api/teacher-dashboard', methods=['GET'])
def teacher_dashboard():
    """Get aggregated statistics for teacher dashboard."""
    from models.learning import LearningProgress, ExerciseAttempt
    from config import LEARNING_PATHS
    
    # Get all progress records
    all_progress = LearningProgress.query.all()
    
    # Calculate overall statistics
    total_students = len(set([p.session_id for p in all_progress]))
    
    # Calculate completion rates by path
    path_completions = {}
    for path in LEARNING_PATHS:
        path_progress = [p for p in all_progress if p.path_id == path['id']]
        completed_modules = sum(1 for p in path_progress if p.status == 'completed')
        total_modules = len(path['modules'])
        completion_rate = completed_modules / total_modules if total_modules > 0 else 0
        
        path_completions[path['id']] = {
            'title': path['title'],
            'completion_rate': completion_rate,
            'students_enrolled': len(set([p.session_id for p in path_progress])),
            'average_score': sum(p.score for p in path_progress) / len(path_progress) if path_progress else 0
        }
    
    # Get recent activity
    recent_attempts = ExerciseAttempt.query.order_by(ExerciseAttempt.created_at.desc()).limit(10).all()
    recent_activity = [{
        'session_id': att.session_id[:8] + '...',  # Anonymized
        'module_id': att.module_id,
        'exercise_id': att.exercise_id,
        'correct': att.correct,
        'timestamp': att.created_at.isoformat()
    } for att in recent_attempts]
    
    return jsonify({
        'total_students': total_students,
        'path_completions': path_completions,
        'recent_activity': recent_activity,
        'active_sessions': len(set([p.session_id for p in all_progress if (datetime.utcnow() - p.updated_at).days <= 1]))
    })


@education_bp.route('/api/accuracy/metrics', methods=['GET'])
def get_accuracy_metrics():
    """Get accuracy tracking metrics for teacher dashboard."""
    try:
        from services.accuracy_tracker import get_accuracy_tracker
        
        days = int(request.args.get('days', 7))
        student_id = request.args.get('student_id', None)
        
        if student_id:
            student_id = int(student_id)
        
        tracker = get_accuracy_tracker()
        metrics = tracker.calculate_metrics(days=days, student_id=student_id)
        trend = tracker.get_trend_analysis(days=days)
        
        # Check for alerts
        alerts = tracker.check_accuracy_thresholds(threshold=70.0)
        
        return jsonify({
            'metrics': metrics.to_dict(),
            'trend': trend,
            'alerts': alerts,
            'success': True
        })
    except Exception as e:
        logger.error(f"Error getting accuracy metrics: {e}")
        return jsonify({'error': str(e), 'success': False}), 500


@education_bp.route('/api/accuracy/report', methods=['GET'])
def generate_accuracy_report():
    """Generate and download accuracy report."""
    try:
        from services.accuracy_tracker import get_accuracy_tracker
        from services.report_generator import get_report_generator
        
        student_id = request.args.get('student_id', None)
        if student_id:
            student_id = int(student_id)
        
        tracker = get_accuracy_tracker()
        reporter = get_report_generator()
        
        # Get data
        metrics = tracker.calculate_metrics(days=30, student_id=student_id)
        predictions = tracker.get_recent_predictions(student_id=student_id, limit=100)
        
        # Prepare student data (placeholder - would fetch from DB in real implementation)
        student_data = {
            'name': f'Student {student_id}' if student_id else 'All Students',
            'overall_score': metrics.accuracy_rate,
            'improvement_rate': metrics.mean_absolute_error * 100,
            'knowledge_retention': 0.7,
            'engagement_score': 0.8,
            'practice_frequency': 0.6,
            'concept_mastery': 0.75,
            'time_on_task': 0.65,
            'error_pattern_score': 0.3,
            'improvement_velocity': 0.5,
            'learning_style_match': 0.8,
            'score_history': [50 + i*2 for i in range(10)]
        }
        
        # Generate report
        html_report = reporter.generate_student_progress_report(
            student_data=student_data,
            accuracy_data=metrics.to_dict(),
            predictions=[p.to_dict() for p in predictions]
        )
        
        from flask import Response
        return Response(
            html_report,
            mimetype='text/html',
            headers={
                'Content-Disposition': f'attachment; filename=accuracy_report_{datetime.now().strftime("%Y%m%d")}.html'
            }
        )
    except Exception as e:
        logger.error(f"Error generating accuracy report: {e}")
        return jsonify({'error': str(e)}), 500


@education_bp.route('/api/accuracy/calibrate', methods=['POST'])
def calibrate_model():
    """Trigger model calibration based on historical accuracy."""
    try:
        from services.accuracy_tracker import get_accuracy_tracker
        
        prediction_type = request.json.get('prediction_type', 'mastery')
        
        tracker = get_accuracy_tracker()
        calibration = tracker.calibrate_model(prediction_type)
        
        return jsonify({
            'calibration': calibration,
            'success': True
        })
    except Exception as e:
        logger.error(f"Error calibrating model: {e}")
        return jsonify({'error': str(e), 'success': False}), 500


@education_bp.route('/api/student-model/predict', methods=['POST'])
def predict_student_outcome():
    """Use probabilistic student model to predict outcomes."""
    try:
        from services.student_model import get_student_model, StudentProfile
        
        data = request.json or {}
        student_id = data.get('student_id', 0)
        difficulty = data.get('difficulty', 0.5)
        
        # Create student profile (in real implementation, fetch from DB)
        profile = StudentProfile(
            student_id=student_id,
            knowledge_retention=data.get('knowledge_retention', 0.5),
            engagement_score=data.get('engagement_score', 0.5),
            practice_frequency=data.get('practice_frequency', 0.5),
            concept_mastery=data.get('concept_mastery', 0.5),
            time_on_task=data.get('time_on_task', 0.5),
            error_pattern_score=data.get('error_pattern_score', 0.5),
            improvement_velocity=data.get('improvement_velocity', 0.5),
            learning_style_match=data.get('learning_style_match', 0.5)
        )
        
        model = get_student_model()
        prediction = model.predict_success_probability(profile, difficulty)
        
        return jsonify({
            'prediction': prediction.to_dict(),
            'success': True
        })
    except Exception as e:
        logger.error(f"Error predicting student outcome: {e}")
        return jsonify({'error': str(e), 'success': False}), 500


@education_bp.route('/api/student-model/recommend-difficulty', methods=['POST'])
def recommend_difficulty():
    """Recommend optimal difficulty level for a student."""
    try:
        from services.student_model import get_student_model, StudentProfile
        
        data = request.json or {}
        student_id = data.get('student_id', 0)
        target_success_rate = data.get('target_success_rate', 0.75)
        
        # Create student profile
        profile = StudentProfile(
            student_id=student_id,
            knowledge_retention=data.get('knowledge_retention', 0.5),
            engagement_score=data.get('engagement_score', 0.5),
            practice_frequency=data.get('practice_frequency', 0.5),
            concept_mastery=data.get('concept_mastery', 0.5),
            time_on_task=data.get('time_on_task', 0.5),
            error_pattern_score=data.get('error_pattern_score', 0.5),
            improvement_velocity=data.get('improvement_velocity', 0.5),
            learning_style_match=data.get('learning_style_match', 0.5)
        )
        
        model = get_student_model()
        recommended_difficulty = model.recommend_difficulty(profile, target_success_rate)
        
        return jsonify({
            'recommended_difficulty': recommended_difficulty,
            'target_success_rate': target_success_rate,
            'success': True
        })
    except Exception as e:
        logger.error(f"Error recommending difficulty: {e}")
        return jsonify({'error': str(e), 'success': False}), 500
