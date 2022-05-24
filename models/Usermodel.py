from models.database import db 
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, data, date, user_id):
        self.data = data
        self.date = date
        self.userd_id = user_id
        
    
    def __repr__(self):
        return vars(Note)

class User(db.Model, UserMixin):
    """user class model"""

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(64), nullable=False)
    notes = db.relationship('Note')

    def __init__(self, email, password, firstname):
        self.email = email
        self.password = password
        self.firstname = firstname
    
    def __repr__(self):
        """string representaion of instance"""
        return vars(User)
