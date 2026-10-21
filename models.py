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
    __tablename__ = "locations"

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
    __tablename__ = "careers"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10))
    name: Mapped[str] = mapped_column(String(100))
    modality: Mapped[str] = mapped_column(String(20))
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "modality": self.modality,
            "location_id": self.location_id
        }

class Student(Data):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    file: Mapped[str] = mapped_column(String(10))
    name: Mapped[str] = mapped_column(String(50))
    year_study: Mapped[int] = mapped_column()
    career_id: Mapped[int] = mapped_column(ForeignKey("careers.id"))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "file": self.file,
            "name": self.name,
            "year_study": self.year_study,
            "career_id": self.career_id
        }


def create_tables():
    Data.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)

