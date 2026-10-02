import sqlite3
from fastapi import FastAPI, Depends, HTTPException, Header

KEY = "mendobot123"

def verify(x_api_key: str = Header(None)):
    if x_api_key != KEY:
        raise HTTPException(status_code=401, detail="API Key inválida o ausente")   

app = FastAPI(
    title = "Mendobot API",
    dependencies=[Depends(verify)])


def obtain_connection():
    con = sqlite3.connect("data.db")
    con.row_factory = sqlite3.Row
    return con


# ==ENDPOINTS==
@app.get("/")
def initiation():
    return {"message": "Bienvenido a la API de Mendobot. Para obtener información sobre los endpoints disponibles, visita /docs."}

@app.get("/estudiantes")
def list_students(academic_year: int = None):
    con = obtain_connection()
    cur = con.cursor()
    if academic_year is not None:
        cur.execute("SELECT * FROM estudiantes WHERE anio_cursada=?", (academic_year,))
    else:
        cur.execute("SELECT * FROM estudiantes")
    rows = cur.fetchall()
    con.close()
    resultado = []
    for row in rows:
        resultado.append(dict(row))
    return resultado

@app.get("/estudiantes/{id}")
def get_student(id: int):
    con = obtain_connection()
    cur = con.cursor()
    