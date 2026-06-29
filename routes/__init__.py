"""Routes package for FINESE SCHOOL."""
from .main import main_bp
from .chatbot import chatbot_bp
from .api import api_bp
from .data import data_bp
from .education import education_bp

__all__ = ['main_bp', 'chatbot_bp', 'api_bp', 'data_bp', 'education_bp']
