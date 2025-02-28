import os
import sys

# Check if the database file exists
DB_FILE = 'instance/strings.db'

if os.path.exists(DB_FILE):
    print(f"Found database at {DB_FILE}")
    confirm = input("This will delete the existing database and create a new one. Continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        sys.exit(0)
    
    try:
        os.remove(DB_FILE)
        print(f"Deleted {DB_FILE}")
    except Exception as e:
        print(f"Error deleting database: {e}")
        sys.exit(1)
else:
    print(f"No database found at {DB_FILE}")
    print("Will create a new database when the application runs.")

print("\nDatabase setup complete. Run 'python app.py' to start the application.")
