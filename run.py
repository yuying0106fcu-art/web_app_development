import os
from flask import Flask
from dotenv import load_dotenv

# 引用我們已經定義好的 models 與 routes 註冊器
from app.models import db
from app.routes import register_blueprints

def create_app():
    # 載入環境變數設定
    load_dotenv()
    
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 基礎設定
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-dev-key')
    
    # 資料庫設定 (SQLite 路徑)
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_path = os.path.join(basedir, 'instance')
    db_path = os.path.join(instance_path, 'database.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 確保 instance 資料夾存在
    os.makedirs(instance_path, exist_ok=True)
    
    # 綁定 SQLAlchemy
    db.init_app(app)
    
    # 註冊 Blueprints
    register_blueprints(app)
    
    return app

app = create_app()

def init_db():
    """初始化資料庫工具函式"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully.")

if __name__ == '__main__':
    app.run(debug=True)
