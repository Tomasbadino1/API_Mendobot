# Mendobot API — Proyecto Integrador

REST API desarrollada con **FastAPI** y **SQLAlchemy** para la gestión de sedes, carreras y estudiantes de la Universidad de Mendoza.

## Authors

- Tomás Badino
- Nicolás Molinero

## Requisitos Previos

* **Python 3.10** o superior.
* Gestor de paquetes **pip**.

---

## Instalación y Configuración

### 1. Clonar el repositorio y crear el entorno virtual
git clone https://github.com/Tomasbadino1/API_Mendobot.git

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate


### 2. Instalar dependencias
pip install -r requirements.txt

### 3. Configurar variables de entorno
Copiar el archivo de plantilla `.env.example` para crear el archivo local `.env`:

# En Linux/macOS:
cp .env.example .env

# En Windows (CMD):
copy .env.example .env

Abrir el archivo `.env` recién creado y asegurarse de definir la clave de API para desarrollo:

API_KEY=mendobot123

> **Nota de seguridad**: El archivo `.env` contiene credenciales locales y se encuentra excluido del control de versiones mediante `.gitignore`.


## Poblado de la Base de Datos

Antes de iniciar el servidor por primera vez, se debe ejecutar el script de siembra para crear las tablas en SQLite (`data.db`) y cargar los datos iniciales:

python seed.py


## Ejecución de la API

Para levantar el servidor de desarrollo local con recarga automática, ejecutar:

uvicorn main:app --reload

## Autenticación

Todas las rutas de la API requieren autenticación mediante la `X-API-Key`:

* **Nombre del Header**: `X-API-Key`
* **Valor**: `mendobot123` (o el valor definido en tu `.env`)

### Uso en la documentación interactiva (/docs)
1. Abrir el navegador en `http://127.0.0.1:8000/docs`.
2. Hacer clic en el botón **Authorize** (arriba a la derecha).
3. Ingresar la clave `mendobot123` en el campo `X-API-Key` y presionar **Authorize**.


## Endpoints Disponibles y Ejemplos de Uso

### 1. Inicio (`GET /`)
* **Descripción**: Confirma que la API está activa y lista para operar.
* **Prueba en `/docs`**: Desplegar la sección `GET /`, presionar **Try it out** y luego **Execute**.
* **Respuesta esperada**: `200 OK` con el mensaje de bienvenida.

### 2. Listar estudiantes (`GET /estudiantes`)
* **Descripción**: Muestra todos los estudiantes o permite filtrarlos opcionalmente por año de cursada.
* **Parámetros en `/docs`**:
  * `anio_cursada` *(Query param, Opcional)*: Ingresar un entero entre `1` y `5` para filtrar. Si se deja en blanco, devuelve todos los estudiantes.
* **Respuestas esperadas**: `200 OK` (lista de estudiantes) o `500 Internal Server Error` (falla de base de datos).

### 3. Obtener estudiante por ID (`GET /estudiantes/{id}`)
* **Descripción**: Devuelve la ficha detallada de un estudiante en base a su ID.
* **Parámetros en `/docs`**:
  * `id` *(Path param, Requerido)*: Número entero identificador del estudiante (ejemplo: `1`).
* **Respuestas esperadas**: 
  * `200 OK`: Devuelve el objeto del estudiante.
  * `404 Not Found`: Si el ID buscado no existe (`{"detail": "Student not found"}`).

### 4. Listar estudiantes por carrera (`GET /carreras/{id}/estudiantes`)
* **Descripción**: Muestra la lista de estudiantes inscriptos en una carrera específica.
* **Parámetros en `/docs`**:
  * `id` *(Path param, Requerido)*: Número entero del ID de la carrera (ejemplo: `1`).
* **Respuestas esperadas**: 
  * `200 OK`: Lista de estudiantes inscriptos.
  * `404 Not Found`: Si la carrera no existe (`{"detail": "Career not found"}`).

### 5. Listar sedes (`GET /sedes`)
* **Descripción**: Devuelve el listado de sedes universitarias con opción de filtro por ciudad.
* **Parámetros en `/docs`**:
  * `ciudad` *(Query param, Opcional)*: Nombre de la ciudad para filtrar (ejemplo: `Mendoza` o `Rio cuarto`). Si no se completa, lista todas las sedes.
* **Respuestas esperadas**: `200 OK`.

### 6. Resumen estadístico (`GET /resumen`)
* **Descripción**: Genera un reporte consolidado con la cantidad total de estudiantes agrupados por carrera y por sede.
* **Prueba en `/docs`**: Desplegar `GET /resumen`, presionar **Try it out** y luego **Execute**.
* **Respuestas esperadas**: `200 OK`.

### 7. Registrar un estudiante (`POST /estudiantes`)
* **Descripción**: Inserta un nuevo estudiante en la base de datos.
* **Cuerpo de la Petición (`Request body`) en `/docs`**:
  Seleccionar la opción **Try it out** y reemplazar el objeto JSON de ejemplo por uno con los nombres de campos exactos en inglés exigidos por el modelo Pydantic:
  
Ejemplo de Petición HTTP (`POST`)**:
json
    {
         "file": "F-099",
         "name": "Mariana López",
         "year_study": 1,
         "careers_id": 1
       }'

* **Respuestas posibles**:
  * **`201 Created`**: Estudiante registrado exitosamente.
  * **`422 Unprocessable Entity`**: Error de validación en la estructura del JSON enviado.
  * **`400 Bad Request`**: La carrera especificada en `careers_id` no existe.