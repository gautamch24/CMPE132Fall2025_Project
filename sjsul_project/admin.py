from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import User, Role, AuditLog
from security import requires, log_audit

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def get_db():
    """Get database session from app context"""
    from flask import current_app
    return current_app.config['DB_SESSION']


@admin_bp.route('/users')
@login_required
@requires('users', 'manage')
def users():
    """Display all users for management"""
    session = get_db()
    all_users = session.query(User).all()
    return render_template('users.html', users=all_users)


@admin_bp.route('/users/<int:user_id>/toggle', methods=['POST'])
@login_required
@requires('users', 'manage')
def toggle_user(user_id):
    """Enable or disable a user account (de-provisioning)"""
    session = get_db()
    user = session.query(User).filter_by(id=user_id).first()
    
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('admin.users'))
    
    if user.id == current_user.id:
        flash('You cannot disable your own account.', 'warning')
        return redirect(url_for('admin.users'))
    
    user.active = not user.active
    session.commit()
    
    action = 'enabled' if user.active else 'disabled'
    log_audit(session, current_user.id, 'deprovision', f'user:{user.username}', action)
    flash(f'User {user.username} has been {action}.', 'success')
    
    return redirect(url_for('admin.users'))


@admin_bp.route('/audit-logs')
@login_required
@requires('audit', 'read')
def audit_logs():
    """View audit logs"""
    session = get_db()
    logs = session.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
    return render_template('approvals.html', logs=logs)