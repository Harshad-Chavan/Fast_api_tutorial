from fastapi import FastAPI
import models
from database import engine

app = FastAPI()

# the line creates the .db sqlite file which contains database
models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def create_database():
    return f"Database: Created"
