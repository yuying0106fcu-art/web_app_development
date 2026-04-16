from datetime import datetime
from . import db
from .tag import recipe_tags

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text, nullable=False)
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 關聯
    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=True, cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary=recipe_tags, backref=db.backref('recipes', lazy='dynamic'))

    @classmethod
    def create(cls, user_id, title, instructions, description=None, is_public=False):
        """新增一筆食譜"""
        try:
            recipe = cls(user_id=user_id, title=title, instructions=instructions, description=description, is_public=is_public)
            db.session.add(recipe)
            db.session.commit()
            return recipe
        except Exception as e:
            db.session.rollback()
            print(f"Error creating recipe: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有食譜"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting recipes: {e}")
            return []

    @classmethod
    def get_by_id(cls, recipe_id):
        """取得單筆食譜"""
        try:
            return cls.query.get(recipe_id)
        except Exception as e:
            print(f"Error getting recipe {recipe_id}: {e}")
            return None

    def update(self, **kwargs):
        """更新食譜資料"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating recipe {self.id}: {e}")
            return False

    def delete(self):
        """刪除食譜"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting recipe {self.id}: {e}")
            return False

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)

    @classmethod
    def create(cls, recipe_id, name, quantity):
        """新增一個食譜食材"""
        try:
            ingredient = cls(recipe_id=recipe_id, name=name, quantity=quantity)
            db.session.add(ingredient)
            db.session.commit()
            return ingredient
        except Exception as e:
            db.session.rollback()
            print(f"Error creating ingredient: {e}")
            return None

    def delete(self):
        """刪除該食材"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting ingredient {self.id}: {e}")
            return False
