import sys

from starlette.responses import RedirectResponse
from starlette import status

sys.path.append("..")

from typing import Optional, Annotated
from fastapi import Depends, HTTPException, APIRouter, Request, Form
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user, get_user_exception

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/todos", tags=["todos"], responses={404: {"description": "Not found"}})

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: db_dependency):
    todos = db.query(models.Todos).filter(models.Todos.owner_id == 1).all()
    context = {"request": request, "todos": todos}
    return templates.TemplateResponse("home.html", context)


@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("add-todo.html", context)


@router.post("/add-todo", response_class=HTMLResponse)
async def create_todo(
    request: Request,
    db: db_dependency,
    title: str = Form(...),
    description: str = Form(...),
    priority: int = Form(...),
):
    todo_model = models.Todos()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.complete = False
    todo_model.owner_id = 1

    db.add(instance=todo_model)
    db.commit()

    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


@router.get("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id: int, db: db_dependency):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    context = {"request": request, "todo": todo}
    return templates.TemplateResponse("edit-todo.html", context)


@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_todo_commit(
    request: Request,
    todo_id: int,
    db: db_dependency,
    title: str = Form(...),
    description: str = Form(...),
    priority: int = Form(...),
):
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    todo.title = title
    todo.description = description
    todo.priority = priority

    db.add(todo)
    db.commit()

    context = {"request": request, "todo": todo}
    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)
