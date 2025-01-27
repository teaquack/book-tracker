from app.extensions import db
from app.models.tag import book_tags

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=True)
    list = db.relationship('List', back_populates='books')
    
    # Relationship with tags
    tags = db.relationship('Tag', secondary=book_tags, back_populates='books')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'list_id': self.list_id,
            'tags': [tag.to_dict() for tag in self.tags]
        }
