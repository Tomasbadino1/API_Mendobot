import sqlite3
from fastapi import FastAPI, Depends, HTTPException, Header

KEY = "mendobot123"

def verify(x_api_key: str = Header(None)):
    if x_api_key != KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")   

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
    return {"message": "Welcome to Mendobot API. For information about available endpoints, visit /docs."}

@app.get("/students")
def list_students(academic_year: int = None):
    con = obtain_connection()
    cur = con.cursor()
    if academic_year is not None:
        cur.execute("SELECT * FROM students WHERE year_study=?", (academic_year,))
    else:
        cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    con.close()
    result = []
    for row in rows:
        result.append(dict(row))
    return result

@app.get("/students/{id}")
def get_student(id: int):
    con = obtain_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    row = cur.fetchone()
    con.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return dict(row)

@app.get("/career/{id}/students")
def get_students_by_career(id: int):
    con = obtain_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM students WHERE career_id=?", (id,))
    rows = cur.fetchall()
    con.close()
    result = []
    for row in rows:
        result.append(dict(row))
    return result

@app.get("/locations")
def list_campuses(city: str = None):
    con = obtain_connection()
    cur = con.cursor()
    if city is not None:
        cur.execute("SELECT * FROM locations WHERE city=?", (city,))
    else:
        cur.execute("SELECT * FROM locations")
    rows = cur.fetchall()
    con.close()
    result = []
    for row in rows:
        result.append(dict(row))
    return result

@app.get("/summary")
def get_summary():
    con = obtain_connection()
    cur = con.cursor()
    cur.execute("""SELECT c.name AS career, COUNT(e.id) AS total_students 
                FROM careers c 
                LEFT JOIN students e ON c.id = e.career_id 
                GROUP BY c.id""")
    rows_careers = cur.fetchall()
    careers_sumary = []
    for row in rows_careers:
        careers_sumary.append(dict(row))

    cur.execute("""SELECT s.name AS location, COUNT(e.id) AS total_students 
            FROM locations s 
            JOIN careers c ON s.id = c.location_id LEFT JOIN students e ON c.id = e.career_id 
            GROUP BY s.id""")
    rows_location = cur.fetchall()
    locations_summary = []
    for row in rows_location:
        locations_summary.append(dict(row))
    
    con.close()
    return {
        "students_by_career": careers_sumary,
        "students_by_location": locations_summary
    }