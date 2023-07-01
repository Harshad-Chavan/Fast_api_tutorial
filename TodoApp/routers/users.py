# Depends stands for dependencies. when one fucntion os dependent on the
# execution of another func we use depends
from fastapi import APIRouter, Depends, HTTPException
import models
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from .auth import get_current_user, bcrypt_context

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close


class ChangePassword(BaseModel):
    old_password: str
    new_password: Field(min_length=6)


user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/info", status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    user = db.query(models.User).filter(models.User.id == user.get("user_id")).first()
    return user


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, passwords: ChangePassword):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    user = db.query(models.User).filter(models.User.id == user.get("user_id")).first()

    # to check if the old password matches
    if not bcrypt_context.verify(passwords.old_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="OLd password did not match")

    user.hashed_password = bcrypt_context.hash(passwords.new_password)
    db.add(user)
    db.commit()
