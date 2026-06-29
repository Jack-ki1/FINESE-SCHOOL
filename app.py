"""
FINESE SCHOOL - AI Assistant for Data Professionals
Flask Application Entry Point
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import timedelta
from flask import Flask
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models import db
from routes import main_bp, chatbot_bp, api_bp, data_bp, education_bp


def create_app():
    app = Flask(__name__)

    # ── Configuration ──────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me-in-production')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB uploads

    # Database
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'finese_school.db')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Code execution
    app.config['CODE_EXEC_TIMEOUT'] = int(os.environ.get('CODE_EXEC_TIMEOUT', '30'))
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')

    # Ensure directories exist
    os.makedirs('flask_session', exist_ok=True)
    os.makedirs('flask_session/chats', exist_ok=True)
    os.makedirs('flask_session/docs', exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(basedir, 'logs'), exist_ok=True)
    os.makedirs(os.path.join(basedir, 'data', 'vectordb'), exist_ok=True)

    # ── Initialize Extensions ──────────────────────────────────────
    db.init_app(app)
    Session(app)

    # Rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )
    app.limiter = limiter

    # ── Register Blueprints ────────────────────────────────────────
    app.register_blueprint(main_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(data_bp, url_prefix='/data')
    app.register_blueprint(education_bp, url_prefix='/learn')

    # ── Create DB tables ───────────────────────────────────────────
    with app.app_context():
        db.create_all()

    # ── Logging ────────────────────────────────────────────────────
    log_handler = RotatingFileHandler(
        os.path.join(basedir, 'logs', 'finese_school.log'),
        maxBytes=10 * 1024 * 1024, backupCount=5
    )
    log_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s] %(message)s'
    ))
    log_handler.setLevel(logging.INFO)
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("FINESE SCHOOL startup")

    # ── Context Globals ────────────────────────────────────────────
    @app.context_processor
    def inject_globals():
        return {
            'app_name': 'FINESE SCHOOL',
            'app_version': '1.0.0',
            'app_tagline': 'AI Assistant for Data Professionals',
        }

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
