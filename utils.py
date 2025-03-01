import sqlite3
import sqlalchemy
import os
import sys
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

# ------ Fix and Reset Functions ------

def reset_database(app):
    """Reset the database to its initial state"""
    print("Resetting database...")
    with app.app_context():
        try:
            # Drop all tables
            db.drop_all()
            print("All tables dropped successfully")
            
            # Recreate all tables
            db.create_all()
            print("All tables recreated successfully")
            
            # Create default admin user
            admin = User(username="admin", is_admin=True)
            admin.set_password("123")
            db.session.add(admin)
            
            # Add default string pattern
            default_pair = StringPair(
                input_pattern="hello",
                output_pattern="OLLEH",
                created_by=1
            )
            db.session.add(default_pair)
            
            db.session.commit()
            print("Default admin user and string pattern created successfully")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error resetting database: {e}")
            return False

def fix_database(app):
    """Fix common database issues"""
    print("Fixing database issues...")
    with app.app_context():
        try:
            # Check for missing tables
            missing_tables = False
            try:
                User.query.first()
                StringPair.query.first()
                StringEntry.query.first()
            except Exception:
                missing_tables = True
            
            if missing_tables:
                print("Missing tables detected, recreating schema...")
                db.create_all()
                print("Schema recreated successfully")
            
            # Check for admin user
            admin = User.query.filter_by(is_admin=True).first()
            if not admin:
                print("No admin user found, creating default admin...")
                admin = User(username="admin", is_admin=True)
                admin.set_password("123")
                db.session.add(admin)
                db.session.commit()
                print("Default admin created successfully")
            
            # Fix orphaned entries (entries without a valid user)
            orphaned_pairs = StringPair.query.filter(
                ~StringPair.created_by.in_(db.session.query(User.id))
            ).all()
            
            if orphaned_pairs:
                print(f"Found {len(orphaned_pairs)} orphaned string pairs, fixing...")
                for pair in orphaned_pairs:
                    if admin:
                        pair.created_by = admin.id
                db.session.commit()
                print("Orphaned pairs fixed")
            
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error fixing database: {e}")
            return False

def fix_routes(app):
    """Fix route issues"""
    print("Checking and fixing route issues...")
    try:
        from routes import admin, main, errors
        
        # Verify routes are registered correctly
        with app.app_context():
            # Check if routes are accessible
            print("Testing route registration...")
            for rule in app.url_map.iter_rules():
                print(f"Route: {rule.endpoint} -> {rule}")
            
            print("Routes check complete")
        return True
    except Exception as e:
        print(f"Error fixing routes: {e}")
        return False

def fix_critical_templates(app):
    """Fix critical templates"""
    print("Checking for critical template issues...")
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
    
    critical_templates = [
        'index.html',
        'result.html',
        'admin_login.html',
        'admin_dashboard.html'
    ]
    
    missing_templates = []
    for template in critical_templates:
        if not os.path.exists(os.path.join(templates_dir, template)):
            missing_templates.append(template)
    
    if missing_templates:
        print(f"Missing critical templates: {', '.join(missing_templates)}")
        print("Please restore these templates from backup or repository")
        return False
    else:
        print("All critical templates are present")
        return True

def quick_fix(app):
    """Perform a quick fix of all common issues"""
    print("Performing quick fix of all systems...")
    
    # Fix database
    db_result = fix_database(app)
    
    # Fix routes
    routes_result = fix_routes(app)
    
    # Fix templates
    templates_result = fix_critical_templates(app)
    
    if db_result and routes_result and templates_result:
        print("Quick fix completed successfully")
        return True
    else:
        print("Quick fix completed with some errors")
        return False

# ------ Maintenance Menu ------

def show_maintenance_menu(app):
    """Display maintenance menu and handle user choice"""
    while True:
        print("\n===== Maintenance Menu =====")
        print("1. Reset Database (WARNING: Deletes all data)")
        print("2. Fix Database Issues")
        print("3. Fix Route Issues")
        print("4. Fix Critical Templates")
        print("5. Quick Fix (All Systems)")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-5): ")
        
        if choice == '0':
            print("Exiting maintenance menu...")
            break
        elif choice == '1':
            confirm = input("WARNING: This will DELETE ALL DATA. Type 'CONFIRM' to proceed: ")
            if confirm == 'CONFIRM':
                reset_database(app)
            else:
                print("Database reset cancelled")
        elif choice == '2':
            fix_database(app)
        elif choice == '3':
            fix_routes(app)
        elif choice == '4':
            fix_critical_templates(app)
        elif choice == '5':
            quick_fix(app)
        else:
            print("Invalid choice, please try again")
        
        input("\nPress Enter to continue...")

# Function to run maintenance menu from command line
def run_maintenance_menu():
    """Run the maintenance menu from command line"""
    # Import app here to avoid circular imports
    from app import create_app
    app = create_app()
    show_maintenance_menu(app)

# Allow running maintenance menu directly
if __name__ == "__main__":
    # Check if being run directly
    if os.path.basename(sys.argv[0]) == "utils.py":
        run_maintenance_menu()
