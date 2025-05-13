"""
Database configuration and setup
"""
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy extension
db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the application context
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        db.create_all()
