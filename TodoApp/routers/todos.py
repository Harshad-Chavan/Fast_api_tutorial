# Depends stands for dependencies. when one fucntion os dependent on the
# execution of another func we use depends
from fastapi import APIRouter, Depends, HTTPException
import models
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from .auth import get_current_user

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close


def http_exception_404():
    return HTTPException(status_code=404, detail="Item not found")


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="Priority must be between 1 & 5")
    complete: bool


@router.get("/")
# this will get executed after the get_db function
async def read_all(user: user_dependency, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("user_id")).all()


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, todo_id: int, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Todos.owner_id == user.get("user_id"))
        .first()
    )

    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Item not found")


@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Todos.owner_id == user.get("user_id"))
        .first()
    )
    print(todo.dict())
    if todo_model is None:
        raise http_exception_404()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    db.add(todo_model)
    db.commit()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(user: user_dependency, todo_id: int, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .filter(models.Todos.owner_id == user.get("user_id"))
        .first()
    )
    if todo_model is None:
        raise http_exception_404()

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()


@router.post("/todos/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, todo: Todo, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = models.Todos(**todo.dict(), owner_id=user.get("user_id"))
    db.add(todo_model)
    db.commit()
