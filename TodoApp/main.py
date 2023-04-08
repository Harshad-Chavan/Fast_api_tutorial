# Depends stands for dependencies. when one fucntion os dependent on the
# execution of another func we use depends
from fastapi import FastAPI, Depends
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# the line creates the .db sqlite file which contains database
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close


@app.get("/")
# this will get executed after the get_db function
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()
