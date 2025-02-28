import os
os.environ['SECRET_KEY'] = 'your_secret_key_here'
os.environ['DATABASE_URI'] = 'sqlite:///strings.db'
os.environ['SECURE_COOKIES'] = 'True'

from app import create_app

# This file is used by WSGI servers like Gunicorn
application = create_app()

if __name__ == "__main__":
    application.run()
