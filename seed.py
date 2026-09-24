import sqlite3
con = sqlite3.connect("data.db")
cur = con.cursor()
headquarters = [
    {"ids": "1","name": "Central", "city": "Mendoza", "address": "Av. Boulogne Sur Mer 683"},
    {"ids": "2", "name": "Rio Cuarto", "city": "Rio Cuarto", "address": "Belgrano 200"},
    {"ids": "3", "name": "San Rafael", "city": "San Rafael", "address": "Bernardo de Irigoyen y España"}
]
cur.execute("CREATE TABLE IF NOT EXISTS headquarters "
            "(id TEXT, name TEXT, city TEXT, address TEXT)")
for s in headquarters:
    cur.execute("INSERT INTO headquarters VALUES (?, ?, ?, ?)", (s["ids"], s["name"], s["city"], s["address"]))
con.commit()
careers = [
    {"ids": "1", "code": "CS101", "name": "University Technical in Software Development", "modality": "Presencial", "sede_id": "2"},
    {"ids": "2", "code": "ME101", "name": "Public Auctioneer", "modality": "Presencial", "sede_id": "2"},
    {"ids": "3", "code": "EE101", "name": "Computer Engineering", "modality": "Mixta", "sede_id": "3, 1"}
]
cur.execute("CREATE TABLE IF NOT EXISTS careers"
            "(id TEXT, code TEXT, name TEXT, modality TEXT, sede_id TEXT)")
for c in careers:
    cur.execute("INSERT INTO careers VALUES (?, ?, ?, ?, ?)", (c["ids"], c["code"], c["name"], c["modality"], c["sede_id"]))
con.commit()

students = [
    {"id": 1, "file": "F-001", "name": "Sofía Martínez", "year_study": 1, "carerres_id": 2},
    {"id": 2, "file": "F-002", "name": "Mateo Rossi", "year_study": 5, "carerres_id": 3},
    {"id": 3, "file": "F-003", "name": "Valentina Gómez", "year_study": 3, "carerres_id": 1},
    {"id": 4, "file": "F-004", "name": "Lucas Fernández", "year_study": 4, "carerres_id": 3},
    {"id": 5, "file": "F-005", "name": "Camila López", "year_study": 2, "carerres_id": 2},
    {"id": 6, "file": "F-006", "name": "Santiago Rodríguez", "year_study": 1, "carerres_id": 1},
    {"id": 7, "file": "F-007", "name": "Isabella Díaz", "year_study": 3, "carerres_id": 3},
    {"id": 8, "file": "F-008", "name": "Joaquín Pérez", "year_study": 3, "carerres_id": 2},
    {"id": 9, "file": "F-009", "name": "Martina González", "year_study": 2, "carerres_id": 1},
    {"id": 10, "file": "F-010", "name": "Tomas Romero", "year_study": 1, "carerres_id": 2},
    {"id": 11, "file": "F-011", "name": "Lucía Álvarez", "year_study": 5, "carerres_id": 3},
    {"id": 12, "file": "F-012", "name": "Benjamín Torres", "year_study": 3, "carerres_id": 1},
    {"id": 13, "file": "F-013", "name": "Elena Castro", "year_study": 4, "carerres_id": 3},
    {"id": 14, "file": "F-014", "name": "Felipe Ruiz", "year_study": 2, "carerres_id": 1},
    {"id": 15, "file": "F-015", "name": "Victoria Morales", "year_study": 5, "carerres_id": 3},
    {"id": 16, "file": "F-016", "name": "Gabriel Sosa", "year_study": 2, "carerres_id": 2},
    {"id": 17, "file": "F-017", "name": "Emma Benítez", "year_study": 1, "carerres_id": 3},
    {"id": 18, "file": "F-018", "name": "Nicolás Silva", "year_study": 1, "carerres_id": 1},
    {"id": 19, "file": "F-019", "name": "Mia Acosta", "year_study": 3, "carerres_id": 2},
    {"id": 20, "file": "F-020", "name": "Samuel Medina", "year_study": 2, "carerres_id": 3}
]

cur.execute("CREATE TABLE IF NOT EXISTS students"
            "(id INTEGER, file TEXT, name TEXT, year_study INTEGER, careers_id INTEGER)")
for s in students:
    cur.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)", (s["id"], s["file"], s["name"], s["year_study"], s["carerres_id"]))
con.commit()