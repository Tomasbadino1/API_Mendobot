from sqlalchemy import create_engine, event, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

DB_FILE = "data.db"

engine = create_engine(f"sqlite:///{DB_FILE}")

@event.listens_for(engine, "connect")
def enable_foreign_keys(con, _):
    con.execute("PRAGMA foreign_keys = ON")

class Data(DeclarativeBase):
    pass

class locations(Data):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(30))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "address": self.address
        }

class careers(Data):
    __tablename__ = "careers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    code: Mapped[str] = mapped_column(String(6))
    mode: Mapped[str] = mapped_column(String(10))
    sede_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "mode": self.mode,
            "sede_id": self.sede_id
        }

class students(Data):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    file: Mapped[str] = mapped_column(String(6))
    name: Mapped[str] = mapped_column(String(30))
    year_student: Mapped[int] = mapped_column()
    career_id: Mapped[int] = mapped_column(ForeignKey("careers.id"))
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "file": self.file,
            "name": self.name,
            "year_student": self.year_student,
            "career_id": self.career_id
        }

def create_tables():
    Data.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)