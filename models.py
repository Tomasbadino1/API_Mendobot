import sqlite3
from sqlalchemy import create_engine, event, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

DB_FILE = "data.db"

engine = create_engine(f"sqlite:///{DB_FILE}")

@event.listens_for(engine, "connect")
def enable_foreign_keys(con, _):
    con.execute("PRAGMA foreign_keys = ON")

class Data(DeclarativeBase):
    pass

class Location(Data):
    __tablename__ = "sedes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(100))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "address": self.address
        }

class Career(Data):
    __tablename__ = "carreras"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10))
    name: Mapped[str] = mapped_column(String(100))
    modality: Mapped[str] = mapped_column(String(20))
    sede_id: Mapped[int] = mapped_column(ForeignKey("sedes.id"))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "modality": self.modality,
            "sede_id": self.sede_id
        }

class Student(Data):
    __tablename__ = "estudiantes"

    id: Mapped[int] = mapped_column(primary_key=True)
    file: Mapped[str] = mapped_column(String(10))
    name: Mapped[str] = mapped_column(String(50))
    year_study: Mapped[int] = mapped_column()
    careers_id: Mapped[int] = mapped_column(ForeignKey("carreras.id"))
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "file": self.file,
            "name": self.name,
            "year_study": self.year_study,
            "careers_id": self.careers_id
        }


def create_tables():
    Data.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)

def obtain_connection():
    con = sqlite3.connect("data.db")
    con.row_factory = sqlite3.Row
    return con
