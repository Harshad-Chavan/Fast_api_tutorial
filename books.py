from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title1", "author": "Author 1", "category": "Science"},
    {"title": "Title2", "author": "Author 2", "category": "Science"},
    {"title": "Title3", "author": "Author 3", "category": "History"},
    {"title": "Title4", "author": "Author 4", "category": "Math"},
    {"title": "Title5", "author": "Author 5", "category": "Math"},
    {"title": "Title6", "author": "Author 6", "category": "Math"},
]


@app.get("/books")
async def read_all_books():
    return BOOKS

#Order of the urls matter.Fast api looks in chrono logical order.
#if i call mybook dynamic param onr will be called
# @app.get("/books/mybook")
# async def read_all_books():
#     return {'title':"My fav book"}

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book




