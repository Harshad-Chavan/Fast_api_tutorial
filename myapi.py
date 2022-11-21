from fastapi import FastAPI, Path
from typing import Optional

# Need to creata the object first
app = FastAPI()

students = {
    1: {"name": "jhon",
        "class": "12",
        "age": 17
        }
}


# command to run server
# uvicorn mypp:app --reload

# create an endpoint (ex url)
# most common endpoint methods GET,POST,PUT,DELETE
@app.get("/index")
def index():
    return {"name": "jhon Doe"}


@app.get("/get_student/{student_id}")
def get_student(student_id: int = Path(None, description="id of the student to be viewed")):
    return students[student_id]

# query parameters with default and non default arguments
@app.get("/get_student_by_name")
def get_student_by_name(name: str | None = None):
    for key, value in students.items():
        if students[key]["name"] == name:
            return students[key]
    else:
        return {"Data": "not found"}
