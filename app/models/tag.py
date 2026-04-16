from . import db

# 多對多關聯表：Recipe <-> Tag
recipe_tags = db.Table('recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    @classmethod
    def create(cls, name):
        """新增標籤"""
        try:
            tag = cls(name=name)
            db.session.add(tag)
            db.session.commit()
            return tag
        except Exception as e:
            db.session.rollback()
            print(f"Error creating tag: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有標籤"""
        try:
            return cls.query.all()
        except Exception as e:
            print(f"Error getting tags: {e}")
            return []

    @classmethod
    def get_by_id(cls, tag_id):
        """利用 ID 取得標籤"""
        try:
            return cls.query.get(tag_id)
        except Exception as e:
            print(f"Error getting tag {tag_id}: {e}")
            return None

    @classmethod
    def get_by_name(cls, name):
        """利用名稱取得標籤"""
        try:
            return cls.query.filter_by(name=name).first()
        except Exception as e:
            print(f"Error finding tag {name}: {e}")
            return None

    def update(self, name):
        """更新標籤名稱"""
        try:
            self.name = name
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating tag {self.id}: {e}")
            return False

    def delete(self):
        """刪除標籤"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting tag {self.id}: {e}")
            return False
