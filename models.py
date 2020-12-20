"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

def connect_db(app):
    db.app = app    
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        """Show info about user"""
        u = self    
        return f"<User first_name = {u.first_name} last_name = {u.last_name}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    img_url = db.Column(db.String(300), nullable = False, default = DEFAULT_IMAGE_URL)

    post = db.relationship('Post', backref = 'user', cascade = 'all, delete-orphan')

    @property
    def full_name(self):
        """Return a full name"""
        return f"{self.last_name}, {self.first_name}"

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key= True, autoincrement = True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.String(50), nullable = False)
    create_at = db.Column(db.DateTime, nullable = False, default = datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    @property
    def friendly_time(self):
        """Get time"""
        return self.create_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    