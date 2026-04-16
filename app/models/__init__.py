from flask_sqlalchemy import SQLAlchemy

# 初始化 SQLAlchemy 實例，避免 circular imports
db = SQLAlchemy()
