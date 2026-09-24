import sqlite3
from fastapi import FastAPI, Depends, HTTPException, Header

KEY = "mendobot123"
app = FastAPI()

def verify(x_api_key: str = Header(None)):
    x_api_key != KEY
    raise HTTPException(status_code=401, detail="API Key inválida o ausente")   


app = FastAPI(
    title = "Mendobot API",
    dependencies=[Depends(verify)])


def obtain_connection():
    con = sqlite3.connect("data.db")
    return con




# ==ENDPOINTS==
@app.get("/")
def initiation():
    return {"message": "Bienvenido a la API de Mendobot. Para obtener información sobre los endpoints disponibles, visita /docs."}

@app.get("/estudiantes")
def list_students(academic_year: int = None):
    connection = obtain_connection()
    cursor = connection.cursor()
    if academic_year is not None:
        cursor.execute()