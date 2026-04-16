from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯
    recipes = db.relationship('Recipe', backref='author', lazy=True, cascade='all, delete-orphan')
    shopping_lists = db.relationship('ShoppingList', backref='owner', lazy=True, cascade='all, delete-orphan')

    # CRUD helper methods
    @classmethod
    def create(cls, username, email, password_hash, role='user'):
        user = cls(username=username, email=email, password_hash=password_hash, role=role)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
