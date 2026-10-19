from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

import crud
from crud import StudentCreate
from security import verify

app = FastAPI(
    title = "Mendobot API",
    dependencies=[Depends(verify)])

#==ENDPOINTS==
@app.get("/")
def initiation():
    """Confirms that the API is up and running"""
    return crud.initiation()

@app.get("/estudiantes")
def list_students(anio_cursada: int = None):
    try:
        return crud.list_students(anio_cursada=anio_cursada)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error")
        
@app.get("/estudiantes/{id}")
def get_student(id: int):
    student = crud.get_student(id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
        
@app.get("/carreras/{id}/estudiantes")
def get_students_by_career(id: int):
    students = crud.get_students_by_career(id)
    if students is None:
        raise HTTPException(status_code=404, detail="Career not found")
    return students


@app.get("/sedes")
def list_campuses(ciudad: str = None):
    try:
        return crud.list_campuses(ciudad=ciudad)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/resumen")
def get_summary():
    try:
        return crud.get_summary()
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error")
    
@app.post("/estudiantes", status_code=201)
def create_student(student: StudentCreate):
    try:
        return crud.create_student(student=student)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Career ID does not exist")