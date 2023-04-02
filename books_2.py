from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

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


# this is a pydantic object
# use Field to add validation
class BookRequest(BaseModel):
    # make the id optional
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)

    # this isa pydantic class
    # editing the example value
    class Config:
        schema_extra = {
            "example": {
                "title": "A new book",
                "author": "codewithroby",
                "description": "A new book description",
                "rating": 5,
            }
        }


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


# pydantic is used for data modelling,data parsing and efficient error handling
# we are ensuring the the post req is having approprite data before transforming into book object
@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


# creating this function to get the max id in the list and assign it to the book
def find_book_id(book: Book):
    # another way
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    # way 2
    # if len(BOOKS):
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1

    return book
