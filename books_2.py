from fastapi import FastAPI,Body
from pydantic import BaseModel,Field

app = FastAPI()



class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book", 5),
    Book(2, "Be Fast with Fast api", "codingwithroby", "This is a greate book", 5),
    Book(3, "Master Endpoint", "codingwithroby", "awesome  book", 5),
    Book(4, "HP1", "Author one", " book", 2),
    Book(5, "HP2", "Author Two", "book", 3),
    Book(6, "HP1", "Author one", " book", 1),
]


@app.get("/books")
async def read_all_books():
    return BOOKS

@app.post("/create_book")
async def create_book(book_request : BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(new_book)