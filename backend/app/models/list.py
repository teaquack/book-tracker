from app.extensions import db

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    books = db.relationship('Book', back_populates='list')

    def to_dict(self, include_books=True):
        data = {
            'id': self.id,
            'name': self.name,
        }
        if include_books:
            data['books'] = [book.to_dict() for book in self.books]
        return data
