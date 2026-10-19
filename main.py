from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

import crud
from security import verify_api_key

#==ENDPOINTS==
@app.get("/")
initiation()


@app.get("/estudiantes")
def list_students(anio_cursada: int = None):
    with get_session() as s:
        query = select(Student)
        if anio_cursada is not None:
            query = query.where(Student.anio_cursada == anio_cursada)
        students = s.scalars(query).all()
        result = []
        for student in students:
            result.append(student.to_dict())
        return result
        
@app.get("/estudiantes/{id}")
def get_student(id: int):
    with get_session() as s:
        student = s.get(Student, id)
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return student.to_dict()
        
@app.get("/carreras/{id}/estudiantes")
def get_students_by_career(id: int):
    with get_session() as s:
        career = s.get(Career, id)
        if career is None:
            raise HTTPException(status_code=404, detail="Career not found")
        
        query = select(Student).where(Student.carrera_id == id)
        students = s.scalars(query).all()
        result = []
        for student in students:
            result.append(student.to_dict())
        return result
        
@app.get("/sedes")
def list_campuses(ciudad: str = None):
    with get_session() as s:
        query = select(Location)
        if ciudad is not None:
            query = query.where(Location.ciudad == ciudad)
        locations = s.scalars(query).all()
        result = []
        for location in locations:
            result.append(location.to_dict())
        return result

@app.get("/resumen")
def get_summary():
    con = obtain_connection()
    cur = con.cursor()
    cur.execute("""SELECT c.nombre AS carrera, COUNT(e.id) AS total_estudiantes 
                FROM carreras c 
                LEFT JOIN estudiantes e ON c.id = e.carrera_id 
                GROUP BY c.id""")
    rows_careers = cur.fetchall()
    careers_sumary = []
    for row in rows_careers:
        careers_sumary.append(dict(row))

    cur.execute("""SELECT s.nombre AS sede, COUNT(e.id) AS total_estudiantes 
            FROM sedes s 
            JOIN carreras c ON s.id = c.sede_id LEFT JOIN estudiantes e ON c.id = e.carrera_id 
            GROUP BY s.id""")
    rows_location = cur.fetchall()
    locations_summary = []
    for row in rows_location:
        locations_summary.append(dict(row))
    
    con.close()
    return {
        "estudiantes_por_carrera": careers_sumary,
        "estudiantes_por_sede": locations_summary
    }