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
        tag = cls(name=name)
        db.session.add(tag)
        db.session.commit()
        return tag

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, tag_id):
        return cls.query.get(tag_id)

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
