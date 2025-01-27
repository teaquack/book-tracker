from app.extensions import db

# Association table for many-to-many relationship between books and tags
book_tags = db.Table('book_tags',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # Relationship with books
    books = db.relationship('Book', secondary=book_tags, back_populates='tags')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
