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

    @classmethod
    def create(cls, username, email, password_hash, role='user'):
        """新增一筆使用者資料"""
        try:
            user = cls(username=username, email=email, password_hash=password_hash, role=role)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return None

    @classmethod
    def get_by_id(cls, user_id):
        """根據 ID 取得單筆使用者資料"""
        try:
            return cls.query.get(user_id)
        except Exception as e:
            print(f"Error finding user {user_id}: {e}")
            return None

    @classmethod
    def get_by_username(cls, username):
        """根據 Username 取得單筆使用者資料"""
        try:
            return cls.query.filter_by(username=username).first()
        except Exception as e:
            print(f"Error finding username {username}: {e}")
            return None

    def update(self, **kwargs):
        """更新目前的記錄資料"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating user {self.id}: {e}")
            return False

    def delete(self):
        """刪除目前的記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting user {self.id}: {e}")
            return False
