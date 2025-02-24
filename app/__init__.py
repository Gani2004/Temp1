from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ='4f9d3a6a9e5b1c2b3d7a8f6c4d9e5a1b'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    db.init_app(app)
    login_manager.init_app(app)

    from Blog_Project.app.models import User  # Now safe after db initialization

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from Blog_Project.app.routes.auth_routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from Blog_Project.app.routes.blog_routes import bp as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')

    @app.route('/')
    def welcome():
        return render_template('welcome.html')

    return app

