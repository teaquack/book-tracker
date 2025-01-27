from app.extensions import db
from app.models.book import Book
from app.models.list import List
from app.services.tag_service import get_or_create_tags

class BookService:
    @staticmethod
    def get_all_books():
        return Book.query.all()

    @staticmethod
    def get_book(book_id):
        return Book.query.get_or_404(book_id)

    @staticmethod
    def create_book(data):
        new_book = Book(
            title=data['title'],
            author=data['author'],
            description=data.get('description')
        )
        if 'list_id' in data and data['list_id']:
            book_list = List.query.get_or_404(data['list_id'])
            new_book.list = book_list

        # Handle tags if provided
        if 'tags' in data and data['tags']:
            new_book.tags = get_or_create_tags(data['tags'])
        
        db.session.add(new_book)
        db.session.commit()
        return new_book

    @staticmethod
    def update_book(book_id, data):
        book = Book.query.get_or_404(book_id)
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.description = data.get('description', book.description)
        
        # Handle tags if provided
        if 'tags' in data:
            book.tags = get_or_create_tags(data['tags'])
            
        db.session.commit()
        return book

    @staticmethod
    def delete_book(book_id):
        book = Book.query.get_or_404(book_id)
        # Tags will be automatically removed from the book_tags table
        db.session.delete(book)
        db.session.commit()

    @staticmethod
    def add_to_list(book_id, list_id):
        book = Book.query.get_or_404(book_id)
        book_list = List.query.get_or_404(list_id)
        book.list = book_list
        db.session.commit()
        return book

    @staticmethod
    def add_tags(book_id, tag_names):
        """Add tags to a book"""
        book = Book.query.get_or_404(book_id)
        new_tags = get_or_create_tags(tag_names)
        book.tags.extend(tag for tag in new_tags if tag not in book.tags)
        db.session.commit()
        return book

    @staticmethod
    def remove_tags(book_id, tag_names):
        """Remove tags from a book"""
        book = Book.query.get_or_404(book_id)
        tag_names = [name.lower() for name in tag_names]
        book.tags = [tag for tag in book.tags if tag.name not in tag_names]
        db.session.commit()
        return book
