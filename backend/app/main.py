from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Set up the database path in the instance folder
db_path = os.path.join(app.instance_path, 'book_tracker.db')
# Create instance folder if it doesn't exist
os.makedirs(app.instance_path, exist_ok=True)
# Configure database URI with absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
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

@app.before_request
def log_request_info():
    logger.debug(f"Request Method: {request.method}")
    logger.debug(f"Request URL: {request.url}")
    logger.debug(f"Request Headers: {dict(request.headers)}")

# API Routes
@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        data = request.get_json()
        new_book = Book(
            title=data['title'],
            author=data['author'],
            description=data.get('description')
        )
        if 'list_id' in data and data['list_id']:
            book_list = List.query.get_or_404(data['list_id'])
            new_book.list = book_list
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_dict())
    else:
        books = Book.query.all()
        return jsonify([book.to_dict() for book in books])

@app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def book_operations(book_id):
    logger.debug(f"Book operation - Method: {request.method}, Book ID: {book_id}")
    
    if request.method == 'DELETE':
        logger.debug("Processing DELETE request")
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        logger.debug("Book deleted successfully")
        return '', 204
    
    elif request.method == 'PUT':
        data = request.get_json()
        book = Book.query.get_or_404(book_id)
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.description = data.get('description', book.description)
        db.session.commit()
        return jsonify(book.to_dict())
    
    else:  # GET
        book = Book.query.get_or_404(book_id)
        return jsonify(book.to_dict())

@app.route('/lists', methods=['GET', 'POST'])
def lists():
    if request.method == 'POST':
        data = request.get_json()
        new_list = List(name=data['name'])
        db.session.add(new_list)
        db.session.commit()
        return jsonify(new_list.to_dict())
    else:
        lists = List.query.all()
        return jsonify([lst.to_dict() for lst in lists])

@app.route('/lists/<int:list_id>/books/<int:book_id>', methods=['POST'])
def add_book_to_list(list_id, book_id):
    book_list = List.query.get_or_404(list_id)
    book = Book.query.get_or_404(book_id)
    book.list = book_list
    db.session.commit()
    return jsonify(book_list.to_dict())

if __name__ == '__main__':
    logger.debug("Starting Flask application...")
    logger.debug("Registered routes:")
    for rule in app.url_map.iter_rules():
        logger.debug(f"{rule} - {rule.methods}")
    app.run(debug=True)
