from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table for books and lists
book_list_association = Table(
    'book_list_association',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('list_id', Integer, ForeignKey('lists.id'))
)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    description = Column(String, nullable=True)
    
    # Relationship with lists through association table
    lists = relationship("List", secondary=book_list_association, back_populates="books")

class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # e.g., "Want to Read", "Currently Reading", etc.
    
    # Relationship with books through association table
    books = relationship("Book", secondary=book_list_association, back_populates="lists")
