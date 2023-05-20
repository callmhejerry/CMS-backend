from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Factory function to create and return
    flask application instance
    """
    app = Flask(__name__)
    db.init_app(app)
    
    return app
