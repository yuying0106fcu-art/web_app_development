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
        s_list = cls(user_id=user_id, name=name)
        db.session.add(s_list)
        db.session.commit()
        return s_list

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
        item = cls(list_id=list_id, name=name, quantity=quantity, estimated_cost=estimated_cost)
        db.session.add(item)
        db.session.commit()
        return item
