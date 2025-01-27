from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.database.models import ListType

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    
    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    tags: Optional[List[str]] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    
    class Config:
        orm_mode = True

class ListBase(BaseModel):
    type: ListType

class ListCreate(ListBase):
    pass

class List(ListBase):
    id: int
    books: List[Book] = []
    
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    lists: List[List] = []
    
    class Config:
        orm_mode = True
