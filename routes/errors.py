from flask import Blueprint, request, render_template

errors_bp = Blueprint('errors', __name__)
logger = None

def set_logger(app_logger):
    global logger
    logger = app_logger

@errors_bp.app_errorhandler(404)
def page_not_found(e):
    if request.path.startswith('/view/'):
        # If it's a view route with invalid ID, show no match page
        logger.info(f"Invalid view ID requested: {request.path}")
        return render_template('no_match.html'), 404
    # Regular 404 for other routes
    logger.info(f"404 not found: {request.path}")
    return render_template('error.html', error="Page not found"), 404

@errors_bp.app_errorhandler(500)
def internal_server_error(e):
    logger.error(f"500 server error: {str(e)}")
    return render_template('error.html', error="Internal Server Error"), 500
