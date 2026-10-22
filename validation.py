from pydantic import BaseModel, Field, StrictInt


class StudentCreate(BaseModel):
    file: str = Field(min_length=1, max_length=10)
    name: str = Field(min_length=1, pattern=r"\S")
    year_study: StrictInt = Field(ge=1, le=5)
    career_id: StrictInt = Field(gt=0)