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

router = APIRouter(prefix="/admin", tags=["admin"])


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close


user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    print(user.get("role"))
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(models.Todos).all()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, todo_id: int, db: Session = Depends(get_db)):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = (
        db.query(models.Todos)
        .filter(models.Todos.id == todo_id)
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
