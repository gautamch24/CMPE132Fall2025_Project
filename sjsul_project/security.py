from passlib.hash import bcrypt
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from sqlalchemy.orm import Session
from models import AuditLog
from datetime import datetime


def hash_password(password):
    """Hash a password using bcrypt with automatic salt generation"""
    return bcrypt.hash(password)


def verify_password(password, password_hash):
    """Verify a password against its hash"""
    return bcrypt.verify(password, password_hash)


def log_audit(session: Session, user_id, action, resource, result):
    """Log an audit event to the database"""
    audit_entry = AuditLog(
        user_id=user_id,
        action=action,
        resource=resource,
        result=result,
        timestamp=datetime.utcnow()
    )
    session.add(audit_entry)
    session.commit()


def requires(resource, action):
    """Decorator to check if user has required permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            if not current_user.has_permission(resource, action):
                flash(f'Access denied: You do not have permission to {action} {resource}.', 'danger')
                return redirect(url_for('forbidden'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator