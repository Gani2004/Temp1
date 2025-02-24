from datetime import datetime
from Blog_Project.app import db
from datetime import datetime
from Blog_Project.app import db

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)  # New field for timestamp
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Author ID

    user = db.relationship('User', backref='posts')  # Establish relationship

    def __repr__(self):
        return f"<BlogPost {self.title}>"

from Blog_Project.app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'

