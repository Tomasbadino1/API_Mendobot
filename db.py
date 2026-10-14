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
    nombre: Mapped[str] = mapped_column(String(50))
    ciudad: Mapped[str] = mapped_column(String(50))
    direccion: Mapped[str] = mapped_column(String(100))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ciudad": self.ciudad,
            "direccion": self.direccion
        }

class Career(Data):
    __tablename__ = "carreras"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    codigo: Mapped[str] = mapped_column(String(10))
    modalidad: Mapped[str] = mapped_column(String(20))
    sede_id: Mapped[int] = mapped_column(ForeignKey("sedes.id"))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "codigo": self.codigo,
            "modalidad": self.modalidad,
            "sede_id": self.sede_id
        }

class Student(Data):
    __tablename__ = "estudiantes"

    id: Mapped[int] = mapped_column(primary_key=True)
    legajo: Mapped[str] = mapped_column(String(10))
    nombre: Mapped[str] = mapped_column(String(50))
    anio_cursada: Mapped[int] = mapped_column()
    carrera_id: Mapped[int] = mapped_column(ForeignKey("carreras.id"))
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "legajo": self.legajo,
            "nombre": self.nombre,
            "anio_cursada": self.anio_cursada,
            "carrera_id": self.carrera_id
        }


def create_tables():
    Data.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)

def obtain_connection():
    con = sqlite3.connect("data.db")
    con.row_factory = sqlite3.Row
    return con
