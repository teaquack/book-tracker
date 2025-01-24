from app.extensions import db
from app.models.list import List

class ListService:
    @staticmethod
    def get_all_lists():
        return List.query.all()

    @staticmethod
    def get_list(list_id):
        return List.query.get_or_404(list_id)

    @staticmethod
    def create_list(data):
        new_list = List(name=data['name'])
        db.session.add(new_list)
        db.session.commit()
        return new_list

    @staticmethod
    def delete_list(list_id):
        book_list = List.query.get_or_404(list_id)
        
        # Remove list_id from all books in the list
        for book in book_list.books:
            book.list_id = None
        
        db.session.delete(book_list)
        db.session.commit()
