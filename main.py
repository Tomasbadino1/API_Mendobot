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
    cur.execute("SELECT * FROM estudiantes WHERE id=?", (id,))
    row = cur.fetchone()
    con.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    return dict(row)

@app.get("/carreras/{id}/estudiantes")
def get_students_by_career(id: int):
    con = obtain_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM estudiantes WHERE carrera_id=?", (id,))
    rows = cur.fetchall()
    con.close()
    resultado = []
    for row in rows:
        resultado.append(dict(row))
    return resultado

@app.get("/sedes")
def list_campuses(ciudad: str = None):
    con = obtain_connection()
    cur = con.cursor()
    if ciudad is not None:
        cur.execute("SELECT * FROM sedes WHERE ciudad=?", (ciudad,))
    else:
        cur.execute("SELECT * FROM sedes")
    rows = cur.fetchall()
    con.close()
    resultado = []
    for row in rows:
        resultado.append(dict(row))
    return resultado

@app.get("/resumen")
def get_summary():
    con = obtain_connection()
    cur = con.cursor()
    cur.execute("""SELECT c.nombre AS carrera, COUNT(e.id) AS total_estudiantes 
                FROM carreras c 
                LEFT JOIN estudiantes e ON c.id = e.carrera_id 
                GROUP BY c.id""")
    rows_careers = cur.fetchall()
    careers_sumary = []
    for row in rows_careers:
        careers_sumary.append(dict(row))

    cur.execute("""SELECT s.nombre AS sede, COUNT(e.id) AS total_estudiantes 
            FROM sedes s 
            JOIN carreras c ON s.id = c.sede_id LEFT JOIN estudiantes e ON c.id = e.carrera_id 
            GROUP BY s.id""")
    rows_location = cur.fetchall()
    locations_summary = []
    for row in rows_location:
        locations_summary.append(dict(row))
        con.close()
    
    return {
        "estudiantes_por_carrera": careers_sumary,
        "estudiantes_por_sede": locations_summary
    }