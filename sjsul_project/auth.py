from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import Session
from models import User, Role
from security import hash_password, verify_password, log_audit

auth_bp = Blueprint('auth', __name__)


def get_db():
    """Get database session from app context"""
    from flask import current_app
    return current_app.config['DB_SESSION']


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role_name = request.form.get('role', 'Student')
        
        session = get_db()
        
        existing_user = session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            flash('Username or email already exists.', 'danger')
            log_audit(session, None, 'register', username, 'failure')
            return redirect(url_for('auth.register'))
        
        password_hash = hash_password(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            active=True
        )
        
        role = session.query(Role).filter_by(name=role_name).first()
        if role:
            new_user.roles.append(role)
        
        session.add(new_user)
        session.commit()
        
        log_audit(session, new_user.id, 'register', 'user_account', 'success')
        flash(f'Account created successfully for {username}!', 'success')
        return redirect(url_for('auth.login'))
    
    session = get_db()
    roles = session.query(Role).all()
    return render_template('register.html', roles=roles)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        session = get_db()
        user = session.query(User).filter_by(username=username).first()
        
        if not user:
            flash('Invalid username or password.', 'danger')
            log_audit(session, None, 'login', username, 'failure')
            return redirect(url_for('auth.login'))
        
        if not user.active:
            flash('Your account has been disabled. Please contact an administrator.', 'danger')
            log_audit(session, user.id, 'login', username, 'failure_disabled')
            return redirect(url_for('auth.login'))
        
        if not verify_password(password, user.password_hash):
            flash('Invalid username or password.', 'danger')
            log_audit(session, user.id, 'login', username, 'failure')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        log_audit(session, user.id, 'login', username, 'success')
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout route"""
    session = get_db()
    log_audit(session, current_user.id, 'logout', current_user.username, 'success')
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))