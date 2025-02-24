import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # Relative path to your DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
