from fastapi import HTTPException
from db import obtain_connection

def get_student(id: int):
    con = obtain_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    row = cur.fetchone()
    con.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return dict(row)