import os
import secrets
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Configure logging
def setup_logger():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'logs.txt')

    # Create a logger
    logger = logging.getLogger('string_transformer')
    logger.setLevel(logging.INFO)

    # Create a file handler that logs even debug messages
    file_handler = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5)
    file_handler.setLevel(logging.INFO)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)
    return logger

# Application configuration
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///strings.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = os.environ.get('SECURE_COOKIES', 'True').lower() == 'true'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour session lifetime
    DEBUG = False
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Add proxy configuration
    BEHIND_PROXY = os.environ.get('BEHIND_PROXY', 'False').lower() == 'true'
    PROXY_HEADERS = ['X-Forwarded-For', 'X-Real-IP']
