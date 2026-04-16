from datetime import datetime
from . import db

class ShoppingList(db.Model):
    __tablename__ = 'shopping_lists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('ShoppingItem', backref='shopping_list', lazy=True, cascade='all, delete-orphan')

    @classmethod
    def create(cls, user_id, name):
        """建立一本新的購物清單"""
        try:
            s_list = cls(user_id=user_id, name=name)
            db.session.add(s_list)
            db.session.commit()
            return s_list
        except Exception as e:
            db.session.rollback()
            print(f"Error creating shopping list: {e}")
            return None

    @classmethod
    def get_by_id(cls, list_id):
        """利用 ID 取得購物清單"""
        try:
            return cls.query.get(list_id)
        except Exception as e:
            print(f"Error getting shopping list {list_id}: {e}")
            return None

    @classmethod
    def get_by_user_id(cls, user_id):
        """取得某名使用者的所有購物清單"""
        try:
            return cls.query.filter_by(user_id=user_id).all()
        except Exception as e:
            print(f"Error getting shopping lists for user {user_id}: {e}")
            return []

    def update(self, **kwargs):
        """更新清單屬性 (例如：清單名稱、是否結束)"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating shopping list {self.id}: {e}")
            return False

    def delete(self):
        """刪除該本購物清單與其關聯物品"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting shopping list {self.id}: {e}")
            return False

class ShoppingItem(db.Model):
    __tablename__ = 'shopping_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_id = db.Column(db.Integer, db.ForeignKey('shopping_lists.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    estimated_cost = db.Column(db.Float, default=0.0)
    is_bought = db.Column(db.Boolean, default=False)

    @classmethod
    def create(cls, list_id, name, quantity, estimated_cost=0.0):
        """新增清單內商品"""
        try:
            item = cls(list_id=list_id, name=name, quantity=quantity, estimated_cost=estimated_cost)
            db.session.add(item)
            db.session.commit()
            return item
        except Exception as e:
            db.session.rollback()
            print(f"Error creating shopping list item: {e}")
            return None

    def update(self, **kwargs):
        """更新商品資料 (例如：勾選購買與否)"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating shopping list item {self.id}: {e}")
            return False

    def delete(self):
        """由清單中移除此商品"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting item {self.id}: {e}")
            return False
