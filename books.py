from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {'title': "Title1","author": "Author 1","category": "Science"},
    {'title': "Title2","author": "Author 2","category": "Science"},
    {'title': "Title3","author": "Author 3","category": "History"},
    {'title': "Title4","author": "Author 4","category": "Math"},
    {'title': "Title5","author": "Author 5","category": "Math"},
    {'title': "Title6","author": "Author 6","category": "Math"},
]

@app.get("/books")
async def read_all_books():
    return BOOKS
