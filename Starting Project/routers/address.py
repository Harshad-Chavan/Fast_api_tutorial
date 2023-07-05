import sys

sys.path.append("..")

from typing import Optional, Annotated

import models
from database import SessionLocal, engine
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .auth import get_current_user, get_user_exception

router = APIRouter(
    prefix="/address", tags=["address"], responses={404: {"description": "Not found"}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Address(BaseModel):
    address1: str
    address2: Optional[str]
    city: str
    state: str
    country: str
    postalcode: str
    apt_num: int

user_dependency = Annotated[dict,Depends(get_current_user)]
db_dependecy = Annotated[Session,Depends(get_db)]

@router.post("/")
async def create_address(user:user_dependency,address_request:Address,db: db_dependecy):
    if user is None:
        raise get_user_exception()
    address_model = models.Address()
    address_model.address1 = address_request.address1
    address_model.address2 = address_request.address2
    address_model.city = address_request.city
    address_model.state = address_request.state
    address_model.country = address_request.country
    address_model.postalcode = address_request.postalcode
    address_model.apt_num = address_request.apt_num

    db.add(address_model)
    # flush retuns id
    db.flush()

    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()
    user_model.address_id = address_model.id

    db.add(user_model)

    db.commit()

