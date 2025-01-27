from flask import Blueprint, jsonify, request
from app.services.tag_service import (
    create_tag,
    get_all_tags,
    get_tag_by_id,
    delete_tag
)
from app.services.book_service import BookService

bp = Blueprint('tags', __name__)

@bp.route('/tags', methods=['GET'])
def get_tags():
    """Get all tags"""
    tags = get_all_tags()
    return jsonify([tag.to_dict() for tag in tags])

@bp.route('/tags', methods=['POST'])
def create_new_tag():
    """Create a new tag"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    tag = create_tag(data['name'])
    return jsonify(tag.to_dict()), 201

@bp.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag_route(tag_id):
    """Delete a tag"""
    if delete_tag(tag_id):
        return '', 204
    return jsonify({'error': 'Tag not found'}), 404

@bp.route('/books/<int:book_id>/tags', methods=['POST'])
def add_tags_to_book(book_id):
    """Add tags to a book"""
    data = request.get_json()
    if not data or 'tags' not in data:
        return jsonify({'error': 'Tags are required'}), 400
    
    book = BookService.add_tags(book_id, data['tags'])
    return jsonify(book.to_dict())

@bp.route('/books/<int:book_id>/tags', methods=['DELETE'])
def remove_tags_from_book(book_id):
    """Remove tags from a book"""
    data = request.get_json()
    if not data or 'tags' not in data:
        return jsonify({'error': 'Tags are required'}), 400
    
    book = BookService.remove_tags(book_id, data['tags'])
    return jsonify(book.to_dict())
