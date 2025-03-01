from flask import Flask, request
from models import db
from routes.main import main_bp
from routes.admin import admin_bp
from routes.errors import errors_bp
from utils import initialize_database, set_logger
from config import setup_logger, Config
from middleware import ProxyFix, get_real_ip

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    
    # Load configuration
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.update(test_config)
    
    # Setup logging
    logger = setup_logger()
    set_logger(logger)
    
    # Add ProxyFix middleware if app is behind a proxy
    if app.config.get('BEHIND_PROXY', False):
        app.wsgi_app = ProxyFix(app.wsgi_app, app.config.get('PROXY_HEADERS'))
        logger.info("ProxyFix middleware enabled")
    
    # Add global function to get real IP
    app.jinja_env.globals.update(get_real_ip=get_real_ip)
    
    # Add request logging for IP addresses
    @app.before_request
    def log_request_info():
        original_ip = request.remote_addr
        real_ip = get_real_ip(request)
        
        # Only log if different (indicating proxy is working)
        if original_ip != real_ip:
            logger.info(f"Request from IP: {real_ip} (via proxy: {original_ip})")
        
        # Store the real IP in request for other functions to use
        request.real_ip = real_ip
    
    # Set loggers in route modules
    from routes.main import set_logger as set_main_logger
    from routes.admin import set_logger as set_admin_logger
    from routes.errors import set_logger as set_errors_logger
    
    set_main_logger(logger)
    set_admin_logger(logger)
    set_errors_logger(logger)
    
    # Initialize database
    db.init_app(app)
    initialize_database(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(errors_bp)
    
    # Startup notification
    @app.before_first_request
    def before_first_request():
        logger.info("First request received. Application is now running.")
    
    return app

# Application entry point
if __name__ == '__main__':
    app = create_app()
    logger = setup_logger()
    logger.info(f"Starting application on {Config.HOST}:{Config.PORT}")
    # Make sure we're using the HOST and PORT from config
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
