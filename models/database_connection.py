"""Database connection model for FINESE SCHOOL."""
from datetime import datetime
from models import db
import uuid


class DatabaseConnection(db.Model):
    """Saved database connections for SQL execution."""
    __tablename__ = 'database_connections'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = db.Column(db.String(36), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    db_type = db.Column(db.String(20), nullable=False)  # sqlite, mysql, postgresql
    connection_string = db.Column(db.Text, nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'db_type': self.db_type,
            'connection_string': self.connection_string,
            'is_default': self.is_default,
            'created_at': self.created_at.isoformat(),
        }
