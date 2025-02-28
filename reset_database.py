import os
import sys
import sqlite3
from werkzeug.security import generate_password_hash
import json
from datetime import datetime
import time

# Path to database file
DB_FILE = 'instance/strings.db'

def reset_database_keeping_admins():
    """Reset the database but keep admin accounts"""
    
    if not os.path.exists(DB_FILE):
        print(f"No database found at {DB_FILE}")
        print("Run the application first to create a database")
        return False
    
    # Confirm before proceeding
    confirm = input("This will delete all string entries, pairs, logs, and non-admin users. Continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return False
    
    print("\n1. Checking if the Flask application is running...")
    try:
        # Try to connect to the database - if the app is running, this might fail
        conn = sqlite3.connect(DB_FILE, timeout=1)
        conn.close()
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            print("\n⚠️ ERROR: The database is locked. Please stop the Flask application before proceeding.")
            print("   Close the Flask application (Ctrl+C in the terminal) and try again.")
            return False
    
    print("2. Backing up admin accounts...")
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get admin accounts
        cursor.execute("SELECT id, username, password_hash, is_admin, created_at FROM user WHERE is_admin = 1")
        admin_users = [dict(row) for row in cursor.fetchall()]
        
        if not admin_users:
            print("No admin accounts found. Will create default admin.")
            admin_users = [{
                'username': 'admin', 
                'password_hash': generate_password_hash('123'),
                'is_admin': 1,
                'created_at': datetime.utcnow().isoformat()
            }]
        
        print(f"Found {len(admin_users)} admin account(s)")
        
        # Create a backup of tables about to be deleted
        print("3. Creating backup of string patterns before deletion...")
        cursor.execute("SELECT * FROM string_pair")
        string_pairs = [dict(row) for row in cursor.fetchall()]
        
        # Close the connection to allow schema changes
        conn.close()
        
        # Create a backup file with the string pairs
        backup_file = 'string_pairs_backup.json'
        with open(backup_file, 'w') as f:
            json.dump(string_pairs, f, indent=2, default=str)
        print(f"Backed up {len(string_pairs)} string pairs to {backup_file}")
        
        # Wait a moment to ensure connections are closed
        time.sleep(1)
        
        # Optional: Create a backup of the old database
        import shutil
        db_backup = 'database_backup.db'
        shutil.copy2(DB_FILE, db_backup)
        print(f"Created full database backup at {db_backup}")
        
        # Delete the database file instead of dropping tables
        print("4. Removing old database file...")
        os.remove(DB_FILE)
        
        # Connect to database again - this creates a new file
        print("5. Creating new database...")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Create tables again
        print("6. Recreating database schema...")
        cursor.executescript('''
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(200) NOT NULL,
                is_admin BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE string_pair (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_pattern VARCHAR(500) NOT NULL UNIQUE,
                output_pattern VARCHAR(500) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_by INTEGER REFERENCES user(id)
            );
            
            CREATE TABLE string_entry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_string VARCHAR(500) NOT NULL,
                transformed_string VARCHAR(500) NOT NULL,
                ip_address VARCHAR(50) NOT NULL,
                accessed BOOLEAN DEFAULT 0,
                reaccesible BOOLEAN DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE admin_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) NOT NULL,
                ip_address VARCHAR(50) NOT NULL,
                logged_in_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        # Restore admin users
        print("7. Restoring admin accounts...")
        for user in admin_users:
            cursor.execute('''
                INSERT INTO user (username, password_hash, is_admin, created_at)
                VALUES (?, ?, ?, ?)
            ''', (
                user.get('username'), 
                user.get('password_hash'), 
                user.get('is_admin', 1),
                user.get('created_at', datetime.utcnow().isoformat())
            ))
        
        # Commit changes and close
        conn.commit()
        conn.close()
        
        print("\n✓ Database reset complete! Admin accounts preserved.")
        print("\nIMPORTANT NEXT STEPS:")
        print("1. Make sure your Flask application is COMPLETELY stopped")
        print("2. Start your Flask application with: python app.py")
        print("3. Clear your browser cache or use a private/incognito window")
        print("\nTo restore backed up string pairs, use the admin interface.")
        return True
        
    except Exception as e:
        print(f"⚠️ Error resetting database: {e}")
        return False

if __name__ == "__main__":
    reset_database_keeping_admins()
