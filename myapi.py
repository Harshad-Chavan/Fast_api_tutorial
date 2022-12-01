from typing import Optional
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

# Need to creata the object first
app = FastAPI()

students = {
    1: {
        "name": "jhon",
        "grade": "12",
        "age": 17
    }
}


class Student(BaseModel):
    name: str
    grade: str | None = None
    age: int


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    grade: Optional[str] = None
    age: Optional[int] = None


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


# query parameters with default and non default argume
@app.get("/get_student_by_name")
def get_student_by_name(name: str | None = Query(default=None, max_length=10)):
    for key, value in students.items():
        if students[key]["name"] == name:
            return students[key]
    else:
        return {"Data": "not found"}


# created a post request endpoint to add student object
@app.post("/add_student")
def add_student(student: Student):
    try:
        new_id = max(students.keys()) + 1
        students[new_id] = dict(student)
        return students
    except Exception as e:
        return str(e)


@app.put("/update_student")
def update_student(student_id: int, student: UpdateStudent):
    try:
        if student_id not in students:
            return {"data": "Student does not exist"}
        if student.name:
            students[student_id]["name"] = student.name
        if student.age:
            students[student_id]["age"] = student.age
        if student.grade:
            students[student_id]["age"] = student.grade
        return students[student_id]
    except Exception as e:
        return str(e)
