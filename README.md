# Mendobot API — Integrative Project

REST API developed with **FastAPI** and **SQLAlchemy** for managing branch campuses, academic careers, and students at the University of Mendoza.


## Authors
* Tomás Badino
* Nicolás Molinero


## Prerequisites

* **Python 3.10** or higher.
* **pip** package manager.


## Installation and Setup

### 1. Clone the repository and create the virtual environment
```bash
git clone https://github.com/Tomasbadino1/API_Mendobot.git

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
Copy the template file `.env.example` to create the local `.env` file:

```bash
# On Linux/macOS:
cp .env.example .env

# On Windows (CMD):
copy .env.example .env
```

Open the newly created `.env` file and make sure to set the development API key:

API_KEY=mendobot123


> **Security Note**: The `.env` file contains local credentials and is excluded from version control via `.gitignore`.



## Database Seeding

Before running the server for the first time, execute the seed script to create the SQLite tables (`data.db`) and load the initial data:

```bash
python seed.py
```


## Running the API

To start the local development server with auto-reload, run:

```bash
uvicorn main:app --reload
```

The API will be available locally at `http://127.0.0.1:8000` and the interactive documentation at `http://127.0.0.1:8000/docs`.


## Authentication in Swagger UI (/docs)

All API routes are protected using the `X-API-Key` HTTP header.

To interactively test the API from your browser:

1. Open your browser and go to **`http://127.0.0.1:8000/docs`**.
2. Click the **Authorize** button (located in the top right corner).
3. In the **`X-API-Key (apiKey)`** field, enter the key configured in your `.env` file (`mendobot123`).
4. Click **Authorize** and then **Close**.

*Once authenticated, the padlocks next to each endpoint will appear closed, and you can test all endpoints by clicking **Try it out** -> **Execute**.*


## Endpoints Usage Guide in /docs

### 1. Home (`GET /`)
* **Description**: Confirms that the API is up and running.
* **Testing in `/docs`**: Expand the `GET /` section, click **Try it out**, and then **Execute**.
* **Expected Response**: `200 OK` with the welcome message.

### 2. List students (`GET /estudiantes`)
* **Description**: Displays all students or allows optional filtering by year of study.
* **Parameters in `/docs`**:
  * `anio_cursada` *(Query param, Optional)*: Enter an integer between `1` and `5` to filter. If left blank, returns all students.
* **Expected Responses**: `200 OK` (list of students) or `500 Internal Server Error` (database failure).

### 3. Get student by ID (`GET /estudiantes/{id}`)
* **Description**: Returns detailed student information based on their ID.
* **Parameters in `/docs`**:
  * `id` *(Path param, Required)*: Integer ID of the student (e.g., `1`).
* **Expected Responses**: 
  * `200 OK`: Returns the student object.
  * `404 Not Found`: If the requested ID does not exist (`{"detail": "Student not found"}`).

### 4. List students by career (`GET /carreras/{id}/estudiantes`)
* **Description**: Displays the list of students enrolled in a specific career.
* **Parameters in `/docs`**:
  * `id` *(Path param, Required)*: Integer ID of the career (e.g., `1`).
* **Expected Responses**: 
  * `200 OK`: List of enrolled students.
  * `404 Not Found`: If the career does not exist (`{"detail": "Career not found"}`).

### 5. List branch campuses (`GET /sedes`)
* **Description**: Returns the list of university branch campuses with an optional filter by city.
* **Parameters in `/docs`**:
  * `ciudad` *(Query param, Optional)*: City name to filter by (e.g., `Mendoza` or `Rio cuarto`). If omitted, lists all campuses.
* **Expected Responses**: `200 OK`.

### 6. Statistical Summary (`GET /resumen`)
* **Description**: Generates a consolidated report with the total count of students grouped by career and by campus.
* **Testing in `/docs`**: Expand `GET /resumen`, click **Try it out**, and then **Execute**.
* **Expected Responses**: `200 OK`.

### 7. Register a student (`POST /estudiantes`)
* **Description**: Inserts a new student into the database.
* **Request body in `/docs`**:
  Select **Try it out** and replace the example JSON object with one containing the exact field names expected by the Pydantic model:

json
{
  "file": "F-099",
  "name": "Mariana López",
  "year_study": 1,
  "careers_id": 1
}


* **Expected Responses**:
  * `201 Created`: Student successfully registered.
  * `422 Unprocessable Entity`: Validation error in the sent JSON structure.
  * `400 Bad Request`: The specified `careers_id` does not exist (`{"detail": "Career ID does not exist"}`).


## AI Usage Statement

An AI assistant was used as support for clarifying concepts regarding SQLAlchemy, modular project structuring, and refining exception handling. All code was reviewed, tested, and adapted by the team members.