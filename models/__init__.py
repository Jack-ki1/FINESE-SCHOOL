"""Database models package for FINESE SCHOOL."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .conversation import Conversation, Message
from .database_connection import DatabaseConnection
from .learning import LearningProgress, ExerciseAttempt

__all__ = [
    'db', 'Conversation', 'Message', 'DatabaseConnection',
    'LearningProgress', 'ExerciseAttempt',
]
