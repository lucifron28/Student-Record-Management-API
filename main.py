from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Union

app = FastAPI()

students: Dict[int, Dict[str, str]] = {
    1: {"name": "Ron Vincent Cada", "student_number": "A23-35524", "program": "BSIT"},
    2: {"name": "Peter Bob Domogma", "student_number": "A23-36794", "program": "BSIT"},
    3: {"name": "Gabriel Ballesteros", "student_number": "A23-37009", "program": "BSIT"},
    4: {"name": "Neo Martin Medrano", "student_number": "A22-33909", "program": "BSIT"},
    5: {"name": "Nikko Samson", "student_number": "A23-36823", "program": "BSIT"}
}

class Student(BaseModel):
    name: str
    student_number: str
    program: str

def find_student_by_id(student_id: int) -> Dict[str, str]:
    if student_id in students:
        return students[student_id]
    raise HTTPException(status_code=404, detail="Student not found")

def find_student_by_student_number(student_number: str) -> int:
    for id, student in students.items():
        if student["student_number"] == student_number:
            return id
    raise HTTPException(status_code=404, detail="Student not found")

@app.get("/students/{id}")
def get_student_by_id(id: int) -> Dict[str, Dict[str, str]]:
    student = find_student_by_id(id)
    return {"student": student}

@app.get("/students")
def get_students(name: Optional[str] = None, program: Optional[str] = None, student_number: Optional[str] = None) -> Dict[str, List[Dict[str, str]]]:
    if name:
        student_list = [student for student in students.values() if student["name"] == name]
        if not student_list:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"students": student_list}
    elif program:
        student_list = [student for student in students.values() if student["program"] == program]
        if not student_list:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"students": student_list}
    elif student_number:
        student_id = find_student_by_student_number(student_number)
        return {"students": [students[student_id]]}
    return {"students": list(students.values())}

@app.post("/students")
def create_student(student: Student) -> Dict[str, Union[int, Dict[str, str]]]:
    new_id = max(students.keys()) + 1
    students[new_id] = student.model_dump()
    return {"id": new_id, "student": students[new_id]}

@app.put("/students/{id}")
def update_student(id: int, student: Student) -> Dict[str, Dict[str, str]]:
    existing_student = find_student_by_id(id)
    students[id] = student.model_dump()
    return {"student": students[id]}

@app.patch("/students/{id}")
def partial_update_student(id: int, student: Student) -> Dict[str, Dict[str, str]]:
    existing_student = find_student_by_id(id)
    for key, value in student.model_dump(exclude_unset=True).items():
        existing_student[key] = value
    return {"student": existing_student}

@app.delete("/students/{id}")
def delete_student(id: int) -> Dict[str, str]:
    existing_student = find_student_by_id(id)
    del students[id]
    return {"message": "Student deleted successfully"}