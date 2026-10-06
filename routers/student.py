from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.postgres import get_db
from models.student import Student
from schemas.student import StudentCreate, StudentResponse
from database.mongodb import student_collection


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# CREATE
@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    # PostgreSQL
    new_student = Student(
        name=student.name,
        age=student.age,
        department=student.department
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    # MongoDB
    student_collection.insert_one({
        "postgres_id": new_student.id,
        "name": new_student.name,
        "age": new_student.age,
        "department": new_student.department
    })

    return new_student


# GET ALL
@router.get("/",response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db)
):

    students = db.query(Student).all()

    return students


# GET ONE
@router.get("/{student_id}",response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# DELETE
@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

     # Delete from MongoDB
    student_collection.delete_one({
        "postgres_id": student_id
    })

    return {
        "message": "Student deleted successfully"
    }