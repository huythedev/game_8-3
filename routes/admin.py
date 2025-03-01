from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, User, AdminLog, StringEntry, StringPair
from utils import login_required, admin_required
from middleware import get_real_ip

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
logger = None

def set_logger(app_logger):
    global logger
    logger = app_logger

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip_address = get_real_ip(request)
        
        logger.info(f"Login attempt for user: {username} from IP: {ip_address}")
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session.clear()
            session.permanent = True
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            # Log admin access
            log_entry = AdminLog(
                username=username,
                ip_address=ip_address
            )
            db.session.add(log_entry)
            db.session.commit()
            
            logger.info(f"Successful login for user: {username}")
            return redirect(url_for('admin.dashboard'))
        else:
            logger.warning(f"Failed login attempt for user: {username}")
            flash("Invalid credentials", "error")
    
    return render_template('admin_login.html')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    try:
        string_entries = StringEntry.query.order_by(StringEntry.created_at.desc()).all()
        admin_logs = AdminLog.query.order_by(AdminLog.logged_in_at.desc()).all()
        string_pairs = StringPair.query.order_by(StringPair.created_at.desc()).all()
        users = User.query.all()
        
        logger.info(f"Admin dashboard accessed by user: {session.get('username')}")
        
        return render_template('admin_dashboard.html', 
                            string_entries=string_entries, 
                            admin_logs=admin_logs,
                            string_pairs=string_pairs,
                            users=users)
    except Exception as e:
        logger.error(f"Error in admin_dashboard route: {e}", exc_info=True)
        flash("An error occurred while loading the dashboard.", "error")
        return redirect(url_for('main.index'))

@admin_bp.route('/string_pair', methods=['POST'])
@login_required
def add_string_pair():
    if not session.get('user_id'):
        return redirect(url_for('admin.login'))
    
    input_pattern = request.form.get('input_pattern')
    output_pattern = request.form.get('output_pattern')
    
    # Check if input pattern already exists
    existing = StringPair.query.filter_by(input_pattern=input_pattern).first()
    if existing:
        existing.output_pattern = output_pattern
        db.session.commit()
        flash("String pair updated successfully", "success")
    else:
        new_pair = StringPair(
            input_pattern=input_pattern,
            output_pattern=output_pattern,
            created_by=session.get('user_id')
        )
        db.session.add(new_pair)
        db.session.commit()
        flash("String pair added successfully", "success")
    
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/string_pair/<int:pair_id>/delete', methods=['POST'])
@login_required
def delete_string_pair(pair_id):
    if not session.get('user_id'):
        return redirect(url_for('admin.login'))
    
    pair = StringPair.query.get_or_404(pair_id)
    db.session.delete(pair)
    db.session.commit()
    flash("String pair deleted successfully", "success")
    
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/users/add', methods=['POST'])
@login_required
@admin_required
def add_user():
    if not session.get('is_admin'):
        flash("Only admins can add users", "error")
        return redirect(url_for('admin.dashboard'))
    
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = 'is_admin' in request.form
    
    # Check if username already exists
    if User.query.filter_by(username=username).first():
        flash("Username already exists", "error")
        return redirect(url_for('admin.dashboard'))
    
    new_user = User(username=username, is_admin=is_admin)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    flash("User added successfully", "success")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if not session.get('is_admin'):
        flash("Only admins can delete users", "error")
        return redirect(url_for('admin.dashboard'))
    
    # Prevent deleting yourself
    if user_id == session.get('user_id'):
        flash("You cannot delete your own account", "error")
        return redirect(url_for('admin.dashboard'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    flash("User deleted successfully", "success")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/entry/<int:entry_id>/toggle_reaccess', methods=['POST'])
@login_required
def toggle_reaccess(entry_id):
    if not session.get('user_id'):
        return redirect(url_for('admin.login'))
    
    entry = StringEntry.query.get_or_404(entry_id)
    
    # Toggle reaccess state
    entry.reaccesible = not entry.reaccesible
    
    # If enabling reaccess, also reset the accessed flag
    if entry.reaccesible:
        entry.accessed = False
        flash(f"Reaccess enabled for entry #{entry.id}. The string can be viewed again.", "success")
    else:
        flash(f"Reaccess disabled for entry #{entry.id}.", "success")
    
    # Commit changes to database
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating entry: {str(e)}", "error")
    
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/entry/<int:entry_id>/delete', methods=['POST'])
@login_required
def delete_entry(entry_id):
    if not session.get('user_id'):
        return redirect(url_for('admin.login'))
    
    entry = StringEntry.query.get_or_404(entry_id)
    
    try:
        db.session.delete(entry)
        db.session.commit()
        flash(f"String entry #{entry_id} has been deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting entry: {str(e)}", "error")
    
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    try:
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate input
        if not (current_password and new_password and confirm_password):
            flash("All password fields are required.", "error")
            return redirect(url_for('admin.dashboard'))
        
        if new_password != confirm_password:
            flash("New passwords don't match.", "error")
            return redirect(url_for('admin.dashboard'))
        
        # Get user
        user = User.query.get(session.get('user_id'))
        
        # Verify current password
        if not user.check_password(current_password):
            logger.warning(f"Failed password change attempt for {user.username} (incorrect current password)")
            flash("Current password is incorrect.", "error")
            return redirect(url_for('admin.dashboard'))
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        logger.info(f"Password changed successfully for user: {user.username}")
        flash("Your password has been updated successfully.", "success")
        return redirect(url_for('admin.dashboard'))
    except Exception as e:
        logger.error(f"Error in change_password route: {e}", exc_info=True)
        flash("An error occurred while changing your password.", "error")
        return redirect(url_for('admin.dashboard'))

@admin_bp.route('/logout')
def logout():
    username = session.get('username')
    session.clear()
    logger.info(f"User logged out: {username}")
    return redirect(url_for('main.index'))

@admin_bp.route('/entries/clear_all', methods=['POST'])
@login_required
@admin_required
def clear_all_entries():
    if not session.get('is_admin'):
        flash("Only administrators can clear all entries", "error")
        return redirect(url_for('admin.dashboard'))
    
    try:
        # Count entries before deletion for logging and feedback
        entries_count = StringEntry.query.count()
        
        # Delete all entries
        StringEntry.query.delete()
        db.session.commit()
        
        logger.warning(f"All string entries ({entries_count}) cleared by admin: {session.get('username')}")
        flash(f"Successfully cleared {entries_count} string entries", "success")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error clearing entries: {str(e)}", exc_info=True)
        flash(f"Error clearing entries: {str(e)}", "error")
        
    return redirect(url_for('admin.dashboard'))
