from datetime import datetime
from moviecollector import db, login_manager
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(30), nullable=False,
                           default="default_img.jpg")
    # posts = db.relationship('Post', backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.image_file}')"

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    plot = db.Column(db.Text, nullable=False)
    cast = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.title}', '{self.author}', '{self.cast}', '{self.plot}')"
    
Base = declarative_base()
class Films(Base):
    __tablename__ = 'Films'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    director = Column(String)
    year = Column(Integer)
    description = Column(String)
    poster = Column(String)


