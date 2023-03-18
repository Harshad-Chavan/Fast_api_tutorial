from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "Science"},
    {"title": "Title Two", "author": "Author Two", "category": "Science"},
    {"title": "Title Three", "author": "Author Three", "category": "History"},
    {"title": "Title Four", "author": "Author Four", "category": "Math"},
    {"title": "Title Five", "author": "Author Five", "category": "Math"},
    {"title": "Title Six", "author": "Author Two", "category": "Math"},
]


@app.get("/books")
async def read_all_books():
    return BOOKS


# Order of the urls matter.Fast api looks in chrono logical order.
# if i call mybook dynamic param onr will be called
# @app.get("/books/mybook")
# async def read_all_books():
#     return {'title':"My fav book"}


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book

# think of query parameter to filter data
# want to filter books based on category
@app.get("/books/")
async def read_category_by_query(category : str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author : str, category : str):
    try:
        books_to_return = []
        for book in BOOKS:
            if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
                books_to_return.append(book)
        return books_to_return
    except Exception as e:
        return {"Exception": e}