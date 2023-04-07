from typing import Optional

# use path to add vlidation to path paramets
# use Query to add vlidation to Query paramets
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


# this is a pydantic object
# use Field to add validation
class BookRequest(BaseModel):
    # make the id optional
    id: Optional[int] = Field(title="id is not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    # this isa pydantic class
    # editing the example value
    class Config:
        schema_extra = {
            "example": {
                "title": "A new book",
                "author": "codewithroby",
                "description": "A new book description",
                "rating": 5,
                "published_date": 2029,
            }
        }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book", 5, 2012),
    Book(2, "Be Fast with Fast api", "codingwithroby", "This is a greate book", 5, 2015),
    Book(3, "Master Endpoint", "codingwithroby", "awesome  book", 5, 2000),
    Book(4, "HP1", "Author one", " book", 2, 2002),
    Book(5, "HP2", "Author Two", "book", 3, 2004),
    Book(6, "HP1", "Author one", " book", 1, 2015),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


# adding extrra validation using Path
@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="item not found")



@app.get("/books/publish/")
async def get_book_by_publish_date(published_date: int = Query(gt=1999, lt=2031)):
    books_returned = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_returned.append(book)
    return books_returned


@app.get("/books/")
async def get_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_returned = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_returned.append(book)
    return books_returned


# pydantic is used for data modelling,data parsing and efficient error handling
# we are ensuring the the post req is having approprite data before transforming into book object
@app.post("/books/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


@app.put("/books/update_book")
async def update_book(book_request: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_request.id:
            BOOKS[i] = Book(**book_request.dict())
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404 , detail="item not found")



@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404 , detail="item not found")


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
