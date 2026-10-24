from models import create_tables, get_session, Student, Career, Location
from sqlalchemy import select

#put the next code before running "python seed.py".

def seed():
    create_tables()
    with get_session() as s:
        if s.scalars(select(Location)).first() is not None:
            print("The database already has data.")
            return
        location1 = Location(name="Central", city="Mendoza", address="Av. Boulogne Sur Mer 683")
        location2 = Location(name="Rio Cuarto", city="Rio Cuarto",address="Belgrano 200")
        location3 = Location(name="San Rafael", city="San Rafael", address="Bernardo de Irigoyen y España")
        s.add_all([location1, location2, location3])
        s.commit()

        if s.scalars(select(Career)).first() is not None:
            print("The database already has data.")
            return
        career1 = Career(code="CS101", name="University Technical in Software Development", modality="Presencial", location_id=location2.id)
        career2 = Career(code="ME101", name="Public Auctioneer", modality="presencial", location_id=location2.id)
        career3 = Career(code="EE101", name="Computer Engineering", modality="virtual", location_id=location3.id)
        career4 = Career(code="E101", name="Computer Engineering", modality="presencial", location_id=location1.id)
        s.add_all([career1, career2, career3, career4])
        s.commit()

        if s.scalars(select(Student)).first() is not None:
            print("The database already has data.")
            return
        student1 = Student(file="F-001", name="Sofía Martínez", year_study=1, career_id=career2.id)
        student2 = Student(file="F-002", name="Mateo Rossi", year_study=5, career_id=career4.id)
        student3 = Student(file="F-003", name="Valentina Gómez", year_study=3, career_id=career1.id)
        student4 = Student(file="F-004", name="Lucas Fernández", year_study=4, career_id=career3.id)
        student5 = Student(file="F-005", name="Camila López", year_study=2, career_id=career2.id)
        student6 = Student(file="F-006", name="Santiago Rodríguez", year_study=1, career_id=career1.id)
        student7 = Student(file="F-007", name="Isabella Díaz", year_study=3, career_id=career4.id)
        student8 = Student(file="F-008", name="Joaquín Pérez", year_study=3, career_id=career2.id)
        student9 = Student(file="F-009", name="Martina González", year_study=2, career_id=career1.id)
        student10 = Student(file="F-010", name="Tomas Romero", year_study=1, career_id=career2.id)
        student11 = Student(file="F-011", name="Lucía Álvarez", year_study=5, career_id=career4.id)
        student12 = Student(file="F-012", name="Benjamín Torres", year_study=3, career_id=career1.id)
        student13 = Student(file="F-013", name="Elena Castro", year_study=4, career_id=career4.id)
        student14 = Student(file="F-014", name="Felipe Ruiz", year_study=2, career_id=career1.id)
        student15 = Student(file="F-015", name="Victoria Morales", year_study=5, career_id=career3.id)
        student16 = Student(file="F-016", name="Gabriel Sosa", year_study=2, career_id=career2.id)
        student17 = Student(file="F-017", name="Emma Benítez", year_study=1, career_id=career3.id)
        student18 = Student(file="F-018", name="Nicolás Silva", year_study=1, career_id=career1.id)
        student19 = Student(file="F-019", name="Mia Acosta", year_study=3, career_id=career2.id)
        student20 = Student(file="F-020", name="Samuel Medina", year_study=2, career_id=career3.id)
        s.add_all([student1, student2, student3, student4, student5, student6, student7, student8, student9, student10,
                student11, student12, student13, student14, student15, student16, student17, student18, student19, student20])
        s.commit()
        print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed()