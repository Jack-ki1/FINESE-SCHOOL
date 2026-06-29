"""Learning progress and exercise models for FINESE SCHOOL."""
from datetime import datetime
from models import db
import uuid


class LearningProgress(db.Model):
    """Track user progress through learning modules."""
    __tablename__ = 'learning_progress'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = db.Column(db.String(36), nullable=False, index=True)
    path_id = db.Column(db.String(50), nullable=False)
    module_id = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, completed
    score = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'path_id': self.path_id,
            'module_id': self.module_id,
            'status': self.status,
            'score': self.score,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }


class ExerciseAttempt(db.Model):
    """Track exercise attempts."""
    __tablename__ = 'exercise_attempts'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = db.Column(db.String(36), nullable=False, index=True)
    module_id = db.Column(db.String(50), nullable=False)
    exercise_id = db.Column(db.String(50), nullable=False)
    user_answer = db.Column(db.Text)
    correct = db.Column(db.Boolean, default=False)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'exercise_id': self.exercise_id,
            'user_answer': self.user_answer,
            'correct': self.correct,
            'feedback': self.feedback,
            'created_at': self.created_at.isoformat(),
        }
