from flask import Blueprint, request, jsonify
from app.services.book_service import BookService

bp = Blueprint('books', __name__)

@bp.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        data = request.get_json()
        new_book = BookService.create_book(data)
        return jsonify(new_book.to_dict())
    else:
        books = BookService.get_all_books()
        return jsonify([book.to_dict() for book in books])

@bp.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def book_operations(book_id):
    if request.method == 'DELETE':
        BookService.delete_book(book_id)
        return '', 204
    
    elif request.method == 'PUT':
        data = request.get_json()
        book = BookService.update_book(book_id, data)
        return jsonify(book.to_dict())
    
    else:  # GET
        book = BookService.get_book(book_id)
        return jsonify(book.to_dict())
