from pydantic import BaseModel
from sqlalchemy import select, func

from models import get_session, Student, Career, Location
from security import verify


class StudentCreate(BaseModel):
    legajo: str
    nombre: str
    anio_cursada: str
    carrera_id: str    

def initiation():
    return {"message": "Welcome to Mendobot API. For information about available endpoints, visit /docs."}

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
        
def get_student(id: int):
    with get_session() as s:
        student = s.get(Student, id)
        if student is None: return None        
        return student.to_dict()
        
def get_students_by_career(id: int):
    with get_session() as s:
        career = s.get(Career, id)
        if career is None:
            return None        
        query = select(Student).where(Student.carrera_id == id)
        students = s.scalars(query).all()
        result = []
        for student in students:
            result.append(student.to_dict())
        return result
        
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

def get_summary():
    with get_session() as s:
        #Agrupamiento de estudiantes por carrera
        query_careers = (
            select(Career.nombre.label("carrera"), func.count(Student.id).label("total_estudiantes"))
            .outerjoin(Student, Career.id == Student.carrera_id)
            .group_by(Career.id)
        )
        rows_careers = s.execute(query_careers).all()
        careers_summary = []
        for row in rows_careers:
            careers_summary.append({
                "carrera": row.carrera,
                "total_estudiantes": row.total_estudiantes
            })
            
        #Agrupamiento de estudiantes por sede
        query_locations = (
            select(Location.nombre.label("sede"), func.count(Student.id).label("total_estudiantes"))
            .join(Career, Location.id == Career.sede_id)
            .outerjoin(Student, Career.id == Student.carrera_id)
            .group_by(Location.id)
        )
        rows_locations = s.execute(query_locations).all()
        locations_summary = []
        for row in rows_locations:
            locations_summary.append({
                "sede": row.sede,
                "total_estudiantes": row.total_estudiantes
            })
        return {
            "estudiantes_por_carrera": careers_summary,
            "estudiantes_por_sede": locations_summary
            }
    
def create_student(student: StudentCreate):
    with get_session() as s:
        career = s.get(Career, student.carrera_id)
        if career is None:
            raise ValueError("Career not found")
    
        new_student = Student(
            legajo=student.legajo,
            nombre=student.nombre,
            anio_cursada=student.anio_cursada,
            carrera_id=student.carrera_id,
            )
        s.add(new_student)
        s.commit()
        s.refresh(new_student)
        return new_student.to_dict()