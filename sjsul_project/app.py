from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, User
from auth import auth_bp
from admin import admin_bp
from security import requires, log_audit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sjsu-library-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sjsul.db'

# Database setup
engine = create_engine('sqlite:///sjsul.db', echo=False)
db_session = scoped_session(sessionmaker(bind=engine))
app.config['DB_SESSION'] = db_session

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return db_session.query(User).get(int(user_id))


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)


@app.route('/')
def index():
    """Home page - redirect to login or dashboard"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing roles and permissions"""
    return render_template('dashboard.html', user=current_user)


@app.route('/books')
@login_required
@requires('books', 'read')
def books():
    """Books page - demonstrates authorization success"""
    session = db_session
    log_audit(session, current_user.id, 'access', 'books', 'success')
    return render_template('dashboard.html', 
                         user=current_user, 
                         message='Access Granted: You can view the library books catalog.',
                         page_title='Books Catalog')


@app.route('/reports')
@login_required
@requires('reports', 'read')
def reports():
    """Reports page - demonstrates authorization (admin only)"""
    session = db_session
    log_audit(session, current_user.id, 'access', 'reports', 'success')
    return render_template('dashboard.html', 
                         user=current_user, 
                         message='✅ Access Granted: You can view administrative reports.',
                         page_title='Administrative Reports')


@app.route('/forbidden')
@login_required
def forbidden():
    """Access denied page"""
    session = db_session
    log_audit(session, current_user.id, 'access_denied', 'restricted_resource', 'failure')
    return render_template('forbidden.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Clean up database session"""
    Session = app.config.get('DB_SESSION')
    if Session:
        Session.remove()


if __name__ == '__main__':
    app.run(debug=True, port=5000)