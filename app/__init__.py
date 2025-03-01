from flask import Flask
import os
from dotenv import load_dotenv

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Load environment variables
    load_dotenv()
    
    # App configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///strings.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Register blueprints
    from app.main_routes import main_bp
    app.register_blueprint(main_bp)
    
    # Register mobile routes
    from app.mobile_routes import mobile_bp
    app.register_blueprint(mobile_bp)
    
    # Initialize extensions
    from app.extensions import db
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
