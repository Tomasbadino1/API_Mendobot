# Mendobot API

REST API for managing university campuses, academic careers, and students. Built with FastAPI and SQLite.

## Authors

- Tomás Badino
- Nicolás Molinero

## Requirements

- Python 3.11 or newer
- Git

## Installation and Execution

1. Clone the repository:
git clone <REPOSITORY_URL>
cd <FOLDER_NAME>

2. Create and activate a virtual environment:
python -m venv venv

- Linux / Mac:
source venv/bin/activate

- Windows:
.\venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Populate database:
python seed.py

5. Run local server:
uvicorn main:app --reload

Local server: http://127.0.0.1:8000
Interactive documentation: http://127.0.0.1:8000/docs

## Authentication

Every endpoint requires an HTTP Header:
- Header name: X-API-Key
- Development key: mendobot123

## Endpoints

- GET /
  Description: Welcome message.

- GET /estudiantes
  Description: List all students. Optional query param: anio_cursada

- GET /estudiantes/{id}
  Description: Get student details by ID.

- GET /carreras/{id}/estudiantes
  Description: List students enrolled in a specific career.

- GET /sedes
  Description: List campuses. Optional query param: ciudad

- GET /resumen
  Description: Summary statistics of students by career and campus.

- POST /estudiantes
  Description: Register a new student.

## Examples

1. Get student by ID:
curl -H "X-API-Key: mendobot123" http://127.0.0.1:8000/estudiantes/1

2. Register a new student:
curl -X POST "http://127.0.0.1:8000/estudiantes" \
     -H "X-API-Key: mendobot123" \
     -H "Content-Type: application/json" \
     -d '{
       "legajo": "EST-2026",
       "nombre": "Mariana López",
       "anio_cursada": 1,
       "carrera_id": 1
     }'

## Deploy

- Render live documentation: https://<YOUR-APP-NAME>.onrender.com/docs

## Use of AI

An AI assistant was used for clarifying SQLAlchemy concepts, structuring modules, and refining error handling. All code was reviewed, adapted, and tested by the team.