import sqlite3
import sqlalchemy
from functools import wraps
from flask import redirect, url_for, session, flash
from models import db, User, StringPair, StringEntry

# Logger will be imported from the main app
logger = None

def set_logger(app_logger):
    global logger
    logger = app_logger

def handle_database_migration():
    """Handle database migration by dropping and recreating all tables."""
    try:
        # Try to drop all tables first
        db.drop_all()
        logger.info("Dropped all tables during migration")
    except Exception as e:
        logger.error(f"Error dropping tables: {e}")
    
    # Create all tables
    db.create_all()
    logger.info("Created all tables during migration")
    
    # Create default admin user
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", is_admin=True)
        admin.set_password("123")
        db.session.add(admin)
        
        # Add some default string patterns
        default_pair = StringPair(
            input_pattern="hello",
            output_pattern="OLLEH",
            created_by=1
        )
        db.session.add(default_pair)
        try:
            db.session.commit()
            logger.info("Created default admin and string pattern")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating defaults: {e}")

def initialize_database(app):
    with app.app_context():
        try:
            # First try to check if we need migration by testing if the reaccesible column exists
            try:
                StringEntry.query.filter_by(reaccesible=True).first()
                logger.info("Database schema is up to date")
            except (sqlite3.OperationalError, sqlalchemy.exc.OperationalError):
                logger.warning("Need to migrate the database schema")
                handle_database_migration()
        except Exception as e:
            logger.error(f"Error during database initialization: {e}")
            # If anything goes wrong, just recreate everything
            handle_database_migration()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash("You must be an admin to access this page", "error")
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# String transformation function
def transform_string(input_string):
    """
    Transform string based on predefined patterns
    Returns None if no pattern matches
    """
    # Check if there's a predefined pattern
    pattern = StringPair.query.filter_by(input_pattern=input_string.lower()).first()
    if pattern:
        return pattern.output_pattern
    
    # No match found
    return None
