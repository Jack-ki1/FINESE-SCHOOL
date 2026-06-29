"""Main routes - Dashboard, pages."""
from flask import Blueprint, render_template, redirect, url_for
from config import LEARNING_PATHS

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Dashboard - main landing page."""
    return render_template('dashboard.html', paths=LEARNING_PATHS)


@main_bp.route('/settings')
def settings():
    return render_template('settings.html')


@main_bp.route('/workspace')
def workspace():
    """Data workspace - SQL editor, code execution, data analysis."""
    return render_template('workspace.html')
