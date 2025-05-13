"""
Database migrations initialization module
"""
from flask_migrate import Migrate
from internal.db.database import db

migrate = Migrate()

def init_migrations(app):
    """Initialize migrations with the app"""
    migrate.init_app(app, db)
