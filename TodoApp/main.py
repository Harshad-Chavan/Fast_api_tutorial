# Depends stands for dependencies. when one fucntion os dependent on the
# execution of another func we use depends
from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from starlette import status

app = FastAPI()

# the line creates the .db sqlite file which contains database
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close

def http_exception_404():
    return HTTPException(status_code=404, detail="Item not found")

@app.get("/")
# this will get executed after the get_db function
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model
    raise http_exception_404()
