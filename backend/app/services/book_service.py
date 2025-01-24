from app.extensions import db
from app.models.book import Book
from app.models.list import List

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
        
        db.session.add(new_book)
        db.session.commit()
        return new_book

    @staticmethod
    def update_book(book_id, data):
        book = Book.query.get_or_404(book_id)
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.description = data.get('description', book.description)
        db.session.commit()
        return book

    @staticmethod
    def delete_book(book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()

    @staticmethod
    def add_to_list(book_id, list_id):
        book = Book.query.get_or_404(book_id)
        book_list = List.query.get_or_404(list_id)
        book.list = book_list
        db.session.commit()
        return book
