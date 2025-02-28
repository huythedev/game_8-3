from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, StringEntry
from utils import transform_string
from middleware import get_real_ip

main_bp = Blueprint('main', __name__)
logger = None

def set_logger(app_logger):
    global logger
    logger = app_logger

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_string = request.form.get('input_string')
        ip_address = get_real_ip(request)
        
        logger.info(f"Transformation request from IP: {ip_address} for string: {input_string}")
        
        try:
            # Check if there's a matching pattern
            transformed = transform_string(input_string)
            
            # If no pattern found
            if transformed is None:
                logger.info(f"No matching pattern found for: {input_string}")
                return render_template('no_match.html')
            
            # Check if this IP has already viewed this pattern
            existing = StringEntry.query.filter_by(
                ip_address=ip_address, 
                input_string=input_string.lower(),
                accessed=True
            ).first()
            
            if existing and not existing.reaccesible:
                logger.info(f"IP {ip_address} already accessed pattern '{input_string}'")
                return render_template('no_match.html', message="This pattern has already been accessed from your IP address.")
            
            # Create new entry or update existing
            if existing and existing.reaccesible:
                # Reset the existing entry
                existing.accessed = False
                existing.reaccesible = False
                db.session.commit()
                entry_id = existing.id
                logger.info(f"Reset existing entry #{entry_id} for reaccess")
            else:
                # Create new entry
                new_entry = StringEntry(
                    input_string=input_string.lower(),
                    transformed_string=transformed,
                    ip_address=ip_address,
                    accessed=False,
                    reaccesible=False
                )
                db.session.add(new_entry)
                db.session.commit()
                entry_id = new_entry.id
                logger.info(f"Created new string entry #{entry_id}")
            
            # Redirect to view page
            return redirect(url_for('main.view_result', entry_id=entry_id))
                
        except Exception as e:
            logger.error(f"Error in index route: {e}", exc_info=True)
            db.session.rollback()
            flash("An error occurred. Please try again later.", "error")
            return redirect(url_for('main.index'))
    
    return render_template('index.html')

@main_bp.route('/view/<int:entry_id>')
def view_result(entry_id):
    # Get the entry
    try:
        entry = StringEntry.query.get_or_404(entry_id)
        
        # Enhanced access control
        logger.info(f"View request for entry #{entry_id} - accessed: {entry.accessed}, reaccesible: {entry.reaccesible}")
        
        # Check if the entry has been accessed already and reaccess is disabled
        if entry.accessed and not entry.reaccesible:
            logger.info(f"Access denied to entry #{entry_id} - already viewed and reaccess not enabled")
            return render_template('no_match.html')
        
        # Before showing the result, mark it as accessed and disable reaccess
        entry.accessed = True
        entry.reaccesible = False
        
        # Save changes
        try:
            db.session.commit()
            logger.info(f"Entry #{entry_id} marked as accessed and reaccess disabled")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating entry status: {e}", exc_info=True)
            flash("An error occurred while processing your request.", "error")
            return redirect(url_for('main.index'))
        
        # Show result
        return render_template('result.html', 
                            input_string=entry.input_string, 
                            result=entry.transformed_string, 
                            one_time=True,
                            entry_id=entry_id)
    except Exception as e:
        logger.error(f"Error in view_result route: {e}", exc_info=True)
        return render_template('error.html', error="An error occurred while processing your request")
