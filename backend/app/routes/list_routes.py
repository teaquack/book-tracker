from flask import Blueprint, request, jsonify
from app.services.list_service import ListService
from app.services.book_service import BookService

bp = Blueprint('lists', __name__)

@bp.route('/lists', methods=['GET', 'POST'])
def lists():
    if request.method == 'POST':
        data = request.get_json()
        new_list = ListService.create_list(data)
        return jsonify(new_list.to_dict())
    else:
        lists = ListService.get_all_lists()
        return jsonify([lst.to_dict() for lst in lists])

@bp.route('/lists/<int:list_id>', methods=['GET', 'DELETE'])
def list_operations(list_id):
    if request.method == 'DELETE':
        ListService.delete_list(list_id)
        return '', 204
    else:
        book_list = ListService.get_list(list_id)
        return jsonify(book_list.to_dict())

@bp.route('/lists/<int:list_id>/books/<int:book_id>', methods=['POST'])
def add_book_to_list(list_id, book_id):
    book = BookService.add_to_list(book_id, list_id)
    return jsonify(book.to_dict())
