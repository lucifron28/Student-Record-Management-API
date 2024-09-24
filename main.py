from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {"name": "Alice", "student_number": "001", "program": "BSIT"},
    2: {"name": "Bob", "student_number": "002", "program": "BSCS"},
    3: {"name": "Charlie", "student_number": "003", "program": "BSEMC"},
    4: {"name": "Diana", "student_number": "004", "program": "BSIT"},
    5: {"name": "Eve", "student_number": "005", "program": "BSCS"}
}

class Student(BaseModel):
    name: str
    student_number: str
    program: str

@app.get("/student/{id}")
def read_student(id: int):
    if id in students:
        return {"student": students[id]}
    raise HTTPException(status_code=404, detail="Student not found")

@app.post("/student/")
def create_student(student: Student):
    new_id = max(students.keys()) + 1
    students[new_id] = student.dict()
    return {"id": new_id, "student": students[new_id]}

@app.put("/student/{id}")
def update_student(id: int, student: Student):
    if id in students:
        students[id] = student.dict()
        return {"student": students[id]}
    raise HTTPException(status_code=404, detail="Student not found")

@app.patch("/student/{id}")
def partial_update_student(id: int, student: Student):
    if id in students:
        for key, value in student.dict(exclude_unset=True).items():
            students[id][key] = value
        return {"student": students[id]}
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/student/{id}")
def delete_student(id: int):
    if id in students:
        del students[id]
        return {"message": "Student deleted successfully"}
    raise HTTPException(status_code=404, detail="Student not found")