from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Fix the database URI configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=True)
    list = db.relationship('List', back_populates='books')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'list_id': self.list_id
        }

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

# Create tables
with app.app_context():
    db.create_all()

# API Routes
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        description=data.get('description')
    )
    
    # If list_id is provided, add the book to that list
    if 'list_id' in data and data['list_id']:
        book_list = List.query.get_or_404(data['list_id'])
        new_book.list = book_list
    
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict())

@app.route('/books', methods=['GET'])
def get_books():
    # Get all books, including those in lists
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get_or_404(book_id)
    
    # Update book fields
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.description = data.get('description', book.description)
    
    db.session.commit()
    return jsonify(book.to_dict())

@app.route('/lists', methods=['POST'])
def create_list():
    data = request.get_json()
    new_list = List(name=data['name'])
    db.session.add(new_list)
    db.session.commit()
    return jsonify(new_list.to_dict())

@app.route('/lists', methods=['GET'])
def get_lists():
    lists = List.query.all()
    return jsonify([list.to_dict() for list in lists])

@app.route('/lists/<int:list_id>/books/<int:book_id>', methods=['POST'])
def add_book_to_list(list_id, book_id):
    book_list = List.query.get_or_404(list_id)
    book = Book.query.get_or_404(book_id)
    
    # Update the book's list
    book.list = book_list
    db.session.commit()
    
    return jsonify(book_list.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
