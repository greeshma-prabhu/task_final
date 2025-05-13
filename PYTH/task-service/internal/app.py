"""
Application factory module for Task Management Service
"""
import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from internal.config import config
from internal.db.database import db
from internal.api.routes import register_routes

def create_app(config_name=None):
    """
    Application factory function
    
    Args:
        config_name: Configuration name to use (development, testing, production)
        
    Returns:
        Flask application instance
    """
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")
        
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    # Register API routes
    register_routes(app)
    
    return app
