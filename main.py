from fastapi import FastAPI
from database.postgres import Base, engine
from models.student import Student
from routers.student import router as student_router


app=FastAPI()

Base.metadata.create_all(
    bind=engine
)


# Include student router
app.include_router(
    student_router
)




