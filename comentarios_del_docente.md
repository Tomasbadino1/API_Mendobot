# Comentarios de la cátedra

Informática (TDS05) · Proyecto Integrador · UM Río Cuarto

Acá va la devolución de cada revisión semanal. Léanlo antes de seguir programando.
Primero está el alcance completo del proyecto; al final, la devolución de cada semana.

**Grupo:** Tomás Badino, Nicolás Molinero
**Tema:** Mendobot — Carreras, sedes y estudiantes

---

# Alcances de este proyecto

Esto es lo que hay que entregar. Lo que no está acá, no se pide.

## Reglas comunes a todos los grupos

### Stack
- Python + **FastAPI** + Uvicorn.
- Datos en **SQLite**. Pueden usar **SQLAlchemy** (ORM, con la guía [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md)) o **`sqlite3` con SQL directo**: las dos formas valen. **Pydantic es opcional**: el cuerpo del `POST` se puede validar con un modelo de Pydantic (`class StudentIn(BaseModel)`) o a mano en `validation.py`. Las dos formas valen.
- Repositorio en GitHub con commits de **todos** los integrantes.
- **Demo local:** la API se corre en la notebook de cada grupo con `uvicorn`. No hace falta desplegarla en la web (ver *Demo local*, abajo).

### Nombres en el código (criterio acordado con la cátedra de Inglés)

> **Actualizado el 15/10:** los nombres de tablas, columnas y rutas en inglés pasan a ser una **recomendación**. Si quedan en español, no es un error.

- **Variables, funciones y clases en inglés**: `list_students`, `get_session`, `class Student(Base)`.
- **Tablas, columnas, rutas y query params:** se recomienda que también vayan en inglés (`__tablename__ = "students"`, columna `career_id`, ruta `GET /students`), pero pueden quedar en español, como figuran en el alcance.
- Lo que sí es obligatorio: usar **el mismo nombre en todos los archivos** (`models.py`, `seed.py`, `crud.py`, `main.py`, `validation.py`). Si la tabla se llama `estudiantes` en el seed, se llama `estudiantes` en todos lados.
- **Documentación en inglés**: `README.md`, docstrings y los mensajes que devuelve la API.
- **Comentarios**: pueden estar en español mientras desarrollan, pero para la **entrega final** tienen que estar en inglés.

### Demo local (sin despliegue)

> **Actualizado el 15/10:** no se despliega a producción. La defensa es **local**, en la notebook del grupo.

`requirements.txt` debe incluir:
```
fastapi
uvicorn
python-dotenv
```
y `sqlalchemy` si lo usan.

Para levantar el proyecto desde cero (lo mismo tiene que estar en el README):
```
python -m venv venv
venv\Scripts\activate          (en Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```
Y abrir http://127.0.0.1:8000/docs.

- El seed se corre **una vez, antes** de levantar el servidor. No va adentro de `main.py`.
- Antes de la defensa, prueben todo esto en la notebook con la que van a presentar.

### Base de datos
- **3 tablas**, cada una con clave primaria (`id`).
- Al menos **1 relación** entre tablas (clave foránea, ej. `equipo_id`).
- **Algunos datos de ejemplo** en cada tabla, los suficientes para ver funcionar los endpoints. No hay mínimo ni máximo. Siempre **datos ficticios**.
- Recomendación: que los datos permitan ver los filtros en acción, por ejemplo productos de varias categorías, para que `?category=` devuelva algo distinto de la lista completa.
- Un script de carga inicial `seed.py` que crea las tablas (con `create_all` o con `CREATE TABLE IF NOT EXISTS`) y carga los datos **solo si la base está vacía**. Se ejecuta antes de levantar el servidor y, si se corre dos veces, no duplica nada.
- El archivo `.db` **puede estar en el repo**. Si lo suben, que esté actualizado (el que genera el seed actual).

### Seguridad: TODOS los endpoints van protegidos

> **Actualizado el 15/10:** se **recomienda** guardar la clave en una variable de entorno en lugar de escribirla en el código. No es obligatorio; en la defensa se puede preguntar por qué conviene hacerlo.

- Todos los endpoints piden la API key en el encabezado `X-API-Key`.
- Sin clave o con clave incorrecta → **401**. Con la clave correcta → **200** y los datos.
- **Recomendado:** guardar la clave en un archivo **`.env`** que **no se sube** (va en el `.gitignore`) y leerla con `python-dotenv`. Al repo se sube un **`.env.example`** con el nombre de la variable y sin el valor. Paso a paso en [guias/variables_de_entorno.md](guias/variables_de_entorno.md). Si la dejan como constante en `security.py`, también vale.
- Los datos son todos **ficticios**: esta API no se usa para nada real.

`security.py` con la clave en el `.env` (la forma recomendada):

```python
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

load_dotenv()
API_KEY = os.getenv("API_KEY")
header = APIKeyHeader(name="X-API-Key")


def verify_api_key(key: str = Depends(header)):
    if API_KEY is None or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
```

Y en `main.py` se protege toda la app de una vez:

```python
app = FastAPI(dependencies=[Depends(verify_api_key)])
```

En `/docs` usá el botón **Authorize** para cargar la clave y probar.
---

## Nivel A — obligatorio (igual para todos)

Cada grupo implementa **exactamente estos 6 endpoints**, adaptados a su tema (ver *Alcance de este grupo*):

| # | Tipo | Ejemplo genérico | Qué practica |
|---|---|---|---|
| 1 | Listado con filtro | `GET /cosas?campo=valor` | Query param y filtro en la consulta |
| 2 | Detalle | `GET /cosas/{id}` | Path param, **404** si no existe |
| 3 | Relación | `GET /cosas/{id}/otras` | Cruzar dos tablas por la clave foránea |
| 4 | Segundo listado con filtro | `GET /otras?campo=valor` | Query param sobre otra tabla |
| 5 | Calculado | `GET /resumen` | Contar, sumar o agrupar (en Python o en la consulta) |
| 6 | Alta | `POST /cosas` | Recibir el cuerpo (con un modelo de Pydantic o como `dict` validado a mano), rechazar los datos inválidos con **400** o **422**, e insertar en la base |

Además, en Nivel A:
- **Errores:** 401 (sin clave), 404 (no existe), y la API no se cae si la base no está o falla una consulta (`try/except`).
- **Filtros opcionales:** si no se manda el query param, devuelve todo.
- **Seguridad (recomendado):** API key en variable de entorno (`.env`) en lugar de escrita en el código.
- **README:** qué hace la API, lista de endpoints, cómo usar la API key, cómo correrla localmente, y declaración de uso de IA si la usaron.

## Nivel B — opcional

Existe un Nivel B que suma hasta 1 punto sobre la nota final. **No se preocupen por eso todavía:** lo vemos en clase más adelante, cuando el Nivel A esté andando.

---

## Alcance de este grupo

### Grupo 2 · Mendobot — Carreras, sedes y estudiantes
**Integrantes:** Tomás Badino, Nicolás Molinero

**Tablas**
- `sedes`: id, nombre, ciudad, direccion
- `carreras`: id, codigo, nombre, modalidad, sede_id (FK)
- `estudiantes`: id, legajo, nombre, anio_cursada, carrera_id (FK)

**Endpoints Nivel A**
1. `GET /estudiantes?anio_cursada=1`
2. `GET /estudiantes/{id}`
3. `GET /carreras/{id}/estudiantes`
4. `GET /sedes?ciudad=Rio Cuarto`
5. `GET /resumen` → cantidad de estudiantes por carrera y por sede
6. `POST /estudiantes`


⚠️ **Datos ficticios, sin excepción.** Los nombres y legajos son inventados: nunca carguen datos de compañeros reales. Es parte de lo que se evalúa, y más todavía acá, porque la clave está a la vista en el repo.

---

## Fuera de alcance (para todos)

No se pide y **no suma**:
- Frontend o páginas web.
- Login de usuarios, registro, JWT.
- Bases de datos externas (PostgreSQL, MySQL, etc.).
- Docker.
- Integración con IA o con el chatbot (eso corresponde a Análisis de Sistemas).
- Pagos, facturación, envío de mails, hardware real.

## Entregables

1. Repositorio GitHub: `main.py`, script de seed, `requirements.txt`, `README.md`, commits de todos.
2. Video demo (máx. 5 min): endpoints funcionando con clave, y un pedido **sin** clave mostrando el 401.
3. Defensa oral el **miércoles 28/10**: demo en vivo desde `/docs`, en local, y preguntas sobre el código. El repositorio tiene que estar al día el **miércoles 21/10**.

---

# Devolución semanal

## 23/09

**📌 Novedad:** la base se maneja con **SQLAlchemy** (ORM) y **sin Pydantic**; las validaciones del `POST` van a mano. Hay una guía con ejemplo completo en [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md) y el código en `guias/pokedex/`. Agreguen `sqlalchemy` a `requirements.txt`.

**⚠️ Cambio de alcance.** El tema ya no es ingreso y becas. Las 3 tablas ahora son `sedes`, `carreras` y `estudiantes`. Lo que sigue reemplaza cualquier indicación anterior.

**Lo que hay:** FastAPI levanta y responde en `/`. `requirements.txt` está armado. `data.py` está vacío.

**A corregir**
- La API key va como constante al principio de `main.py`, pero con un nombre claro y en mayúsculas: `CLAVE = "..."` en vez de `x_api_key_x = 123`. Todavía no hace falta variable de entorno.
- Falta agregar `gunicorn` y `uvicorn-worker` a `requirements.txt` para el deploy.
- `data.py` vacío: los datos ahora van en SQLite, así que reemplazalo por `seed.py`.

**Próximos pasos**
1. Proteger toda la app de una vez con `FastAPI(dependencies=[Depends(verificar)])`.
2. `seed.py` con las 3 tablas:
   - `sedes`: id, nombre, ciudad, direccion
   - `carreras`: id, codigo, nombre, modalidad, `sede_id` (FK)
   - `estudiantes`: id, legajo, nombre, anio_cursada, `carrera_id` (FK)
3. Repartir los endpoints entre los dos: los commits tienen que mostrar el aporte de cada uno.

**⚠️ Datos ficticios, sin excepción.** Los nombres y legajos de `estudiantes` son inventados. Nunca carguen datos de compañeros reales: el repo es público y la clave está a la vista. Es parte de lo que se evalúa.

## 24/09

**📌 Criterio de nombres.** Variables, funciones y clases en **inglés**; tablas, columnas y rutas como en el alcance; comentarios en inglés para la entrega final. Está detallado arriba en *Reglas comunes* y la guía ya lo aplica.

**Lo que hay:** primer avance real. `seed.py` crea `headquarters`, `careers` y `students` con 3 + 3 + 20 registros, y `main.py` tiene la verificación de clave y el comienzo de `GET /estudiantes`. Ya hay commits de los dos. 👍

**⚠️ La API rechaza todo.** En `verify`, la línea `x_api_key != KEY` no hace nada (falta el `if`), así que el `raise HTTPException(401)` se ejecuta **siempre**, incluso con la clave correcta. Tiene que ser:
```python
def verify(x_api_key: str = Header(None)):
    if x_api_key != KEY:
        raise HTTPException(status_code=401, detail="API Key inválida o ausente")
```

**A corregir en `main.py`**
- `app = FastAPI()` está definido dos veces. Dejen solo el de `dependencies=[Depends(verify)]`.
- `cursor.execute()` está vacío: el endpoint rompe apenas se lo llama.
- **Pasen la base a SQLAlchemy** (ver [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md)). El `sqlite3` con cursor y SQL a mano ya no va: tablas como clases, consultas con `select(...).where(...)`.

**A corregir en `seed.py`**
- Los `id` van como `INTEGER PRIMARY KEY`, no como `TEXT`. Con SQLAlchemy es `mapped_column(primary_key=True)` y no hace falta cargarlos a mano.
- No hay claves foráneas: `careers.sede_id` y `students.careers_id` tienen que ser `ForeignKey`.
- Una carrera tiene **una** sede: `"sede_id": "3, 1"` no es válido. Si Ingeniería está en dos sedes, cárguenla dos veces o elijan una.
- Tipo: en la lista de estudiantes la clave es `carerres_id` pero la columna es `careers_id`.
- El seed carga los datos cada vez que corre, así que en la segunda corrida duplica todo. Tiene que cargar **solo si la base está vacía** (sección 9 de la guía).
- Para **tablas y columnas** usen los nombres del alcance: `sedes`, `carreras`, `estudiantes` con `legajo`, `anio_cursada`, `carrera_id`. Las funciones y variables en inglés (`list_students`, `verify`) están bien: es el criterio del curso. Los endpoints se llaman `GET /estudiantes?anio_cursada=1`, y conviene que las columnas coincidan con los query params.

**A corregir en el repo**
- `data.db` y `__pycache__/` están subidos. Agréguenlos al `.gitignore` y sáquenlos con `git rm --cached data.db -r __pycache__`.
- `requirements.txt` tiene versiones fijadas de todo, incluso de `pydantic` y `requests` que no se usan. Dejen solo: `fastapi`, `uvicorn`, `uvicorn-worker`, `gunicorn`, `sqlalchemy`.

**Próximos pasos**
1. Arreglar `verify` y probar en `/docs` que con la clave responde y sin la clave da 401.
2. Reescribir `seed.py` con SQLAlchemy: 3 clases, FK, carga solo si está vacía.
3. Terminar `GET /estudiantes?anio_cursada=` y `GET /estudiantes/{id}` con 404.

## 08/10

**Lo que hay:** mucho avance, y de los dos. 👍 `verify` ya funciona, `app` quedó definido una sola vez, el `.gitignore` está bien y `data.db` ya no está en el repo. `db.py` tiene las 3 tablas como clases de SQLAlchemy con sus claves foráneas. `main.py` tiene 5 de los 6 endpoints escritos y `validation.py` ya valida los tres tipos de datos.

El problema es que las piezas todavía no están conectadas entre sí, y hoy la API no puede devolver datos. Van los tres puntos importantes, en orden.

**⚠️ 1. `seed.py` está roto y no hay forma de crear la base.**
- Quedaron commiteadas las marcas de un conflicto de merge (`<<<<<<< HEAD`, `=======`, `>>>>>>> 20fac27...`). Con eso el archivo ni siquiera corre: da `SyntaxError`.
- Además, todo el seed está metido adentro de un `"""..."""`, o sea, desactivado.
- Como `data.db` ya no se sube (correcto), sin seed no hay tablas y todos los endpoints fallan.
- Cuando git les marca un conflicto, hay que abrir el archivo, elegir con qué versión se quedan, **borrar las tres marcas** y recién ahí hacer el commit.

**⚠️ 2. Cada archivo usa nombres distintos para lo mismo.**
**Cambio de criterio:** ahora va **todo en inglés**, también tablas, columnas, rutas y query params (ver *Nombres en el código*, arriba). La traducción que hicieron está bien: **no la deshagan**. Si leyeron una versión anterior de esta devolución que pedía volver al español, ignoren ese punto.

Lo que falta es que los tres archivos se pongan de acuerdo:

| Dato | `main.py` | `db.py` | `validation.py` |
|---|---|---|---|
| Año de cursada | `year_study` | `year_student` | `year_student` |
| Sede de la carrera | `location_id` | `sede_id` | `id_locations` |

Elijan **un** nombre para cada cosa y úsenlo en todos lados. Lo más simple es tomar `db.py` como referencia, cambiando `sede_id` por `location_id` (es el único que quedó en español).

Dos detalles más de nombres:
- La ruta `/career/{id}/students` quedó en singular y las demás en plural: va `/careers/{id}/students`.
- `file` no es una buena traducción de *legajo* (se confunde con "archivo"). Mejor `file_number` o `student_number`.

**⚠️ 3. `main.py` no usa `db.py`.**
`main.py` sigue con `sqlite3`, cursor y SQL escrito a mano. Las clases de `db.py` no se usan en ningún lado. Hay que pasar los endpoints a la sesión de SQLAlchemy (secciones 5 y 8 de la [guía](guias/sqlalchemy_orm.md)). El primero quedaría así:

```python
from sqlalchemy import select
from db import get_session, Student

@app.get("/students")
def list_students(year_student: int = None):
    with get_session() as s:
        query = select(Student)
        if year_student is not None:
            query = query.where(Student.year_student == year_student)
        return [student.to_dict() for student in s.scalars(query)]
```

**A corregir en `db.py`**
- Las clases van con mayúscula y en singular: `Location`, `Career`, `Student` (hoy son `locations`, `careers`, `students`).
- Los largos máximos no coinciden con `validation.py` ni con sus propios datos: `name` admite 30 caracteres y una de las carreras del seed tiene 44; `code` es `String(6)` acá y 10 en la validación; `mode` es 10 acá y 20 allá. Elijan un valor y úsenlo en los dos archivos.

**A corregir en `validation.py`**
- Está bien pensado (incluido el `partial`), pero nadie lo llama: falta el `POST /students`, que es el endpoint 6. `crud.py` está vacío.
- Solo hace falta validar estudiantes; el alcance no pide `POST` de sedes ni de carreras. Pueden dejar las otras dos funciones, pero no pierdan tiempo ahí.
- El mensaje dice "career ID does not exist", pero la función no lo comprueba. Antes de insertar, busquen la carrera con `s.get(Career, career_id)` y, si no existe, devuelvan **400**.
- En `year_student` falta descartar los booleanos, como ya hicieron con `career_id`: hoy `true` pasa como si fuera un 1.
- Variables en inglés: `archivo`, `anio_de_curso` y `carrera_id` son variables de Python.

**A corregir en el repo**
- `requirements.txt` sigue igual que el 24/09. Dejen solo: `fastapi`, `uvicorn`, `uvicorn-worker`, `gunicorn`, `sqlalchemy`. Sin `gunicorn` y `uvicorn-worker` el deploy en Render no arranca.
- El `README.md` tiene solo el título. Tiene que explicar, en inglés, qué hace la API, los endpoints, cómo usar la clave y cómo correrla.
- Falta el `try/except` para que la API no se caiga si la base no está.
- Datos: hay 3 sedes y 4 carreras. Se piden unas 10 filas por tabla; los 20 estudiantes están bien.

**Próximos pasos**
1. Reescribir `seed.py` con SQLAlchemy: importa las clases de `db.py`, llama a `create_tables()` y carga los datos **solo si la tabla está vacía** (sección 9 de la guía). Probar que corre dos veces sin duplicar.
2. Unificar los nombres de tablas y columnas entre `db.py`, `main.py` y `validation.py`, todo en inglés.
3. Pasar los 5 `GET` de `main.py` a la sesión de SQLAlchemy y sacar `sqlite3`.
4. Escribir `POST /students` usando `validation_students` (400 si los datos están mal).
5. Arreglar `requirements.txt` y desplegar en Render. No lo dejen para el final: el deploy siempre trae sorpresas.

Antes de cada commit, levanten la API y prueben los endpoints en `/docs`. Varios de estos problemas se ven en el primer intento.

## 15/10

**📌 Cambios en las reglas** (están arriba, en *Reglas comunes*):
- **SQLAlchemy es opcional:** también vale `sqlite3` con SQL directo.
- **No hay que desplegar.** La defensa es **local**, en su notebook, el **miércoles 28/10**. El repo tiene que estar al día el **miércoles 21/10**.
- **Recomendado:** la API key en una variable de entorno (`.env`) en lugar de escrita en el código. No es obligatorio, pero en la defensa se puede preguntar dónde está la clave y por qué conviene sacarla del código.

**Lo que hay:** `models.py` está bien armado (claves foráneas, `to_dict`), el seed lo reescribió Nicolás con SQLAlchemy y no duplica, `security.py` lee la clave del `.env` 👍, y la lógica del resumen está bien planteada. Hay commits de los dos.

**⚠️ Hoy no hay API.** `main.py` está **vacío**: el commit `aaa1636` del 14/10 le borró las 106 líneas. La `app` quedó adentro de `crud.py`, pero sin ningún `@app.get` ni `@app.post`, así que no hay rutas. `uvicorn main:app` no puede arrancar.

**Lo probé llamando directamente a las funciones de `crud.py`.** Solo funcionan el listado sin filtro y el detalle con 404. El resto falla porque **`crud.py` y `models.py` usan nombres distintos**:

| En `crud.py` | En `models.py` |
|---|---|
| `anio_cursada` | `year_study` |
| `carrera_id` | `careers_id` |
| `ciudad`, `nombre` | `city`, `name` |
| `legajo` | `file` |

Es el mismo problema del 08/10, ahora entre `crud.py` y `models.py`.

**Lo que falta para la entrega del 21/10**
1. **Recuperar `main.py`.** Está en el historial de git: `git show aaa1636~1:main.py`. Que tenga la `app` y los 6 endpoints cortos, cada uno llamando a una función de `crud.py` (ver [guias/estructura_del_proyecto.md](guias/estructura_del_proyecto.md)). Saquen la `app` de `crud.py`.
2. **Unificar los nombres** de la tabla de arriba: `crud.py` tiene que usar los de `models.py`.
3. **`POST /students` con Pydantic.** Pueden usarlo, pero el modelo `StudentCreate` está mal armado:
   - Los campos tienen los nombres en español (`legajo`, `nombre`, `anio_cursada`, `carrera_id`), y `Student` no los tiene: `create_student` falla con `TypeError` al crear el estudiante. Usen los mismos nombres que en `models.py`.
   - **Todos los campos son `str`.** Así Pydantic no controla nada: el año y la carrera tienen que ser `int`, y entonces FastAPI rechaza solo, con **422**, un año `"abc"`.
   - El rango del año se puede pedir en el mismo modelo: `year_study: int = Field(ge=1, le=5)`.
   - Que la carrera exista ya lo controlan (400 si no existe) 👍.
   - El modelo y el endpoint van en `main.py`, que recibe `student: StudentCreate` y llama a `crud.create_student(...)`.
   - Si validan con Pydantic, `validation.py` sobra: bórrenlo para que no quede código sin usar (o usen ese y saquen Pydantic, pero no los dos).
4. **`try/except`** en las consultas. Hoy, si falta la base, todo da 500 sin control.
5. **La clave:** el `.env.example` vacío está bien. El problema es en `security.py`: si alguien levanta la API sin haber creado el `.env`, `KEY` queda en `None` y **una petición sin clave pasa** (porque `None == None`). Controlen ese caso (`if KEY is None or ...`), como en el ejemplo de *Seguridad*.
6. **README:** sigue con una línea. Hay una guía con plantilla en `guias/`.

**Recomendaciones:**
- Las tablas (`sedes`, `carreras`, `estudiantes`, `sede_id`) y las claves del JSON del resumen siguen en español. No es un error; si les da el tiempo, pasarlas a inglés deja todo más parejo con el resto del código.
- `requirements.txt` salió de `pip freeze` y funciona bien. Si quieren dejarlo más prolijo, pueden escribirlo a mano con solo lo que usan (`fastapi`, `uvicorn`, `sqlalchemy`, `python-dotenv`, `pydantic`) y guardarlo en UTF-8. Hoy está en UTF-16 porque PowerShell guarda así la salida de `>`.

**Más chico:** `careers_id` debería ser `career_id` (una carrera por estudiante, en singular); `crud.py` no debería lanzar `HTTPException` (eso es de `main.py`); en `models.py` quedó `obtain_connection()` con `sqlite3`, sin usar.

Antes de cada commit, levanten la API y prueben en `/docs`. Un `main.py` vacío se ve en el primer intento.

## 21/10 (entrega)

**Lo que hay:** el avance más grande del proyecto, y de los dos. 👍 `main.py` tiene las 6 rutas y `crud.py` usa los nombres reales de `models.py`. Hay `try/except` en los GET, la clave no deja pasar nada si falta el `.env`, y el README está completo, con la declaración de uso de IA.

**⚠️ Pero el último commit dejó la API sin arrancar.** El commit `c3342c5` ("corrections in crud.py and main.py", 21/10) borró la clase `StudentCreate` de `crud.py`, y `main.py` todavía la importa (`from crud import StudentCreate`, línea 5). Al levantar da `ImportError` y no responde ningún endpoint. Seguramente la quisieron mover a `main.py`, como sugería la devolución del 15/10, y quedó a medio camino. **Se arregla pegando la clase en `main.py`**, arriba de los endpoints, y sacando el import:

```python
from pydantic import BaseModel, Field

class StudentCreate(BaseModel):
    file: str = Field(min_length=1, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    year_study: int = Field(ge=1, le=5)
    career_id: int = Field(gt=0)
```

En `crud.py`, cambien la anotación de `create_student` por `student_data` a secas (o importen la clase desde `main.py`).

**Con la clase restaurada, probé todo en una copia** y funciona:

| # | Endpoint | Resultado |
|---|---|---|
| 1 | `GET /estudiantes?anio_cursada=` | ✅ 20 en total; año 1 trae 5 |
| 2 | `GET /estudiantes/{id}` | ✅ `/999` da 404 |
| 3 | `GET /carreras/{id}/estudiantes` | ✅ Coincide con el seed; carrera inexistente da 404 |
| 4 | `GET /sedes?ciudad=` | ✅ Filtra bien |
| 5 | `GET /resumen` | ✅ Estudiantes por carrera y por sede, con los números correctos |
| 6 | `POST /estudiantes` | ✅ 201 con datos válidos; 422 si falta un campo o el año está fuera de rango; 400 si la carrera no existe o el legajo está repetido |

Más 401 sin clave o con clave mala, y el seed sin duplicar. **Es decir: con esa corrección, el Nivel A está completo.**

**Lo que conviene corregir también:**
- **README:** la clave de desarrollo que figura (`mendobot123`) no está configurada en ningún lado. Agreguen el paso "copiar `.env.example` a `.env` y escribir `API_KEY=...`". El ejemplo del `POST` usa `legajo`, `nombre`, `anio_cursada` y `carrera_id`, pero el modelo espera `file`, `name`, `year_study` y `career_id`: tal como está, da 422.
- **El `POST` no tiene `try/except` de base:** sin la base da 500 sin control (los GET ya lo manejan).
- **Pydantic acepta algunas cosas:** `true` y `"3"` como año, y un nombre de solo espacios. Si quieren cerrarlo: `year_study: StrictInt = Field(ge=1, le=5)` y `name: str = Field(min_length=1, pattern=r"\S")`.

**Para la defensa (28/10):** prueben la demo completa en la notebook con la que van a presentar, siguiendo el README desde cero. Este último error se hubiera visto con solo levantar la API antes del commit.
