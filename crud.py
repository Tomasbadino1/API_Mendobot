import validation
from sqlalchemy import select, func

from models import get_session, Student, Career, Location


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
            .outerjoin(Student, Career.id == Student.career_id)
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
            .join(Career, Location.id == Career.location_id)
            .outerjoin(Student, Career.id == Student.career_id)
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
    
def data_student(student_data: validation.StudentCreate):
    with get_session() as s:
        career = s.get(Career, student_data.career_id)
        if career is None:
            raise ValueError("Career not found")
        
        student_exist = s.scalars(select(Student).where(Student.file == student_data.file)).first()
        if student_exist is not None:
            raise ValueError("Student already exists")
        

        new_student = Student(
            file=student_data.file,
            name=student_data.name,
            year_study=student_data.year_study,
            career_id=student_data.career_id,
            )
        s.add(new_student)
        s.commit()
        s.refresh(new_student)
        return new_student.to_dict()