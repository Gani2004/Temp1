from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------
# User Model
# -------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    posts = db.relationship('BlogPost', back_populates='author', lazy=True)
    comments = db.relationship('Comment', back_populates='author', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'

# -------------------------
# Blog Post Model
# -------------------------
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Use back_populates for explicit relationships
    author = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', lazy=True)

    def __repr__(self):
        return f"<BlogPost {self.title}>"

# -------------------------
# Comment Model
# -------------------------
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'), nullable=False)

    # Consistent use of back_populates
    author = db.relationship('User', back_populates='comments')
    post = db.relationship('BlogPost', back_populates='comments')

    def __repr__(self):
        return f"<Comment {self.content[:20]}>"
