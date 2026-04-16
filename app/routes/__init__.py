from flask import Blueprint

# 建立 Blueprint，避免 circular imports，由 app.py 註冊
from .auth import bp as auth_bp
from .main import bp as main_bp
from .recipe import bp as recipe_bp
from .shopping import bp as shopping_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(shopping_bp)
