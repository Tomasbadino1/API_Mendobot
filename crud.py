from pydantic import BaseModel, Field
from sqlalchemy import select, func

from models import get_session, Student, Career, Location


class StudentCreate(BaseModel):
    file: str = Field(min_length=1, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    year_study: int = Field(ge=1, le=5)
    careers_id: int = Field(gt=0)

def initiation():
    return {"message": "Welcome to Mendobot API. For information about available endpoints, visit /docs."}

def list_students(year_study: int = None):
    with get_session() as s:
        query = select(Student)
        if year_study is not None:
            query = query.where(Student.year_study == year_study)
        students = s.scalars(query).all()
        result = []
        for student in students:
            result.append(student.to_dict())
        return result
        
def get_student(student_id: int):
    with get_session() as s:
        student = s.get(Student, student_id)
        if student is None: return None        
        return student.to_dict()
        
def get_students_by_career(career_id: int):
    with get_session() as s:
        career = s.get(Career, career_id)
        if career is None:
            return None        
        query = select(Student).where(Student.careers_id == career_id)
        students = s.scalars(query).all()
        result = []
        for student in students:
            result.append(student.to_dict())
        return result
        
def list_campuses(city: str = None):
    with get_session() as s:
        query = select(Location)
        if city is not None:
            query = query.where(Location.city == city)
        locations = s.scalars(query).all()
        result = []
        for location in locations:
            result.append(location.to_dict())
        return result

def get_summary():
    with get_session() as s:
        #student grouping by degree program
        query_careers = (
            select(Career.name.label("carrera"), 
            func.count(Student.id).label("total_estudiantes"))
            .outerjoin(Student, Career.id == Student.careers_id)
            .group_by(Career.id)
        )
        rows_careers = s.execute(query_careers).all()
        careers_summary = []
        for row in rows_careers:
            careers_summary.append({
                "carrera": row.carrera,
                "total_estudiantes": row.total_estudiantes
            })
            
        #student grouping by campus
        query_locations = (
            select(Location.name.label("sede"), 
            func.count(Student.id).label("total_estudiantes"))
            .join(Career, Location.id == Career.sede_id)
            .outerjoin(Student, Career.id == Student.careers_id)
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
    
def create_student(student_data: StudentCreate):
    with get_session() as s:
        career = s.get(Career, student_data.careers_id)
        if career is None:
            raise ValueError("Career not found")
    
        new_student = Student(
            file=student_data.file,
            name=student_data.name,
            year_study=student_data.year_study,
            careers_id=student_data.careers_id,
            )
        s.add(new_student)
        s.commit()
        s.refresh(new_student)
        return new_student.to_dict()