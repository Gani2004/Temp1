from flask import Flask,render_template,session,abort,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import requests

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ='4f9d3a6a9e5b1c2b3d7a8f6c4d9e5a1b'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)
    from app import models  # Import models before creating tables
    with app.app_context():
        db.create_all()  # Create tables
    login_manager.init_app(app)

    from app.models import User  # Now safe after db initialization

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from app.routes.auth_routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.blog_routes import bp as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')

    @app.route('/')
    def welcome():
        return render_template('welcome.html')
    acc_key='030902'

    @app.route('/users', methods=['GET', 'POST'])
    def list_users():
        # Check if user is already authenticated
        if session.get('authenticated'):
            users = User.query.all()
            return render_template('users.html', users=users)

        if request.method == 'POST':
            entered_key = request.form.get('access_key')
            if entered_key == acc_key:
                session['authenticated'] = True  # Set session as authenticated
                return redirect(url_for('list_users'))
            else:
                return render_template('key_prompt.html', error="Invalid Key")

        return render_template('key_prompt.html')

    @app.route('/logout')
    def logout():
        session.pop('authenticated', None)
        return redirect(url_for('list_users'))
    return app

