from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

students: Dict[int, Dict[str, Union[int, str]]] = {
    1: {"id": 1, "name": "Junio Layba", "student_number": "T22-35397", "program": "BSIT"},
    2: {"id": 2, "name": "Jose Nathaniel Rodriguez", "student_number": "T23-36998", "program": "BSIT"},
    3: {"id": 3, "name": "Neo Martin Medrano", "student_number": "A22-33909", "program": "BSIT"},
    4: {"id": 4, "name": "Mike Andrei Gomez", "student_number": "A23-36954", "program": "BSIT"}
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Student(BaseModel):
    name: str
    student_number: str
    program: str

def find_student_by_id(student_id: int) -> Dict[str, Union[int, str]]:
    if student_id in students:
        return students[student_id]
    raise HTTPException(status_code=404, detail="Student not found")

def find_student_by_student_number(student_number: str) -> int:
    for id, student in students.items():
        if student["student_number"] == student_number:
            return id
    raise HTTPException(status_code=404, detail="Student not found")

@app.get("/students/{id}")
def get_student_by_id(id: int) -> Dict[str, Dict[str, Union[int, str]]]:
    student = find_student_by_id(id)
    return {"student": student}

@app.get("/students")
def get_students(name: Optional[str] = None, program: Optional[str] = None, student_number: Optional[str] = None) -> List[Dict[str, Union[int, str]]]:
    if name:
        student_list = [student for student in students.values() if student["name"] == name]
        if not student_list:
            raise HTTPException(status_code=404, detail="Student not found")
        return student_list
    elif program:
        student_list = [student for student in students.values() if student["program"] == program]
        if not student_list:
            raise HTTPException(status_code=404, detail="Student not found")
        return student_list
    elif student_number:
        student_id = find_student_by_student_number(student_number)
        return [students[student_id]]
    return list(students.values())

@app.post("/students")
def create_student(student: Student) -> Dict[str, Union[int, Dict[str, Union[int, str]]]]:
    new_id = max(students.keys(), default=0) + 1
    students[new_id] = {"id": new_id, **student.dict()}
    return {"id": new_id, "student": students[new_id]}

@app.put("/students/{id}")
def update_student(id: int, student: Student) -> Dict[str, Dict[str, Union[int, str]]]:
    existing_student = find_student_by_id(id)
    students[id] = {"id": id, **student.dict()}
    return {"student": students[id]}

@app.patch("/students/{id}")
def partial_update_student(id: int, student: Student) -> Dict[str, Dict[str, Union[int, str]]]:
    existing_student = find_student_by_id(id)
    for key, value in student.dict(exclude_unset=True).items():
        existing_student[key] = value
    return {"student": existing_student}

@app.delete("/students/{id}")
def delete_student(id: int) -> Dict[str, str]:
    existing_student = find_student_by_id(id)
    del students[id]
    return {"message": "Student deleted successfully"}