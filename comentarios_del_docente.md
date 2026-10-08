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
- Datos en **SQLite** usando **SQLAlchemy** (ORM): las tablas se definen como clases de Python y las consultas se hacen con métodos, sin escribir SQL a mano. **No se usa Pydantic**: las validaciones se hacen a mano en Python. Guía con ejemplo completo: [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md).
- Repositorio en GitHub con commits de **todos** los integrantes.
- API desplegada **en producción con Gunicorn** en Render, con URL pública y `/docs` funcionando (ver abajo).

### Nombres en el código (criterio acordado con la cátedra de Inglés)

> **Actualizado el 08/10:** ahora va **todo en inglés**, también tablas, columnas y rutas. Reemplaza el criterio del 24/09.

- **Variables, funciones y clases en inglés**: `list_students`, `get_session`, `class Student(Base)`.
- **Tablas, columnas, rutas y query params también en inglés**. Ejemplo: `class Student(Base)` con `__tablename__ = "students"`, columna `career_id` y ruta `GET /students`.
- El alcance de cada grupo lista las tablas y los endpoints en español **solo como referencia**: tradúzcanlos al inglés y usen **el mismo nombre en todos los archivos** (`db.py`, `seed.py`, `main.py`, `validation.py`).
- **Documentación en inglés**: `README.md`, docstrings y los mensajes que devuelve la API.
- **Comentarios**: pueden estar en español mientras desarrollan, pero para la **entrega final** tienen que estar en inglés.

### Despliegue a producción (Render + Gunicorn)

En tu compu desarrollás con `uvicorn main:app --reload`. En producción corre **Gunicorn** como administrador de procesos, con workers de Uvicorn adentro.

> Gunicorn **no funciona en Windows**. Localmente seguí usando `uvicorn`; Gunicorn corre en el servidor (Linux).

`requirements.txt` debe incluir:
```
fastapi
uvicorn
uvicorn-worker
gunicorn
sqlalchemy
```

En Render → **New → Web Service** → conectás el repo, y configurás:

| Campo | Valor |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python seed.py && gunicorn main:app -k uvicorn_worker.UvicornWorker -w 2 -b 0.0.0.0:$PORT` |

La clave viaja en el código, así que no hay que configurar nada más en Render.

- El seed corre **una sola vez antes** de levantar Gunicorn. Si lo pusieras adentro de `main.py`, cada worker lo ejecutaría por su cuenta y podrían cargar los datos duplicados.
- El plan gratis se duerme tras ~15 min sin uso (la primera visita tarda ~1 min) y su disco se borra al reiniciar: por eso el seed.

### Base de datos
- **3 tablas**, cada una con clave primaria (`id`).
- Al menos **1 relación** entre tablas (clave foránea, ej. `equipo_id`).
- Unos **10 registros de ejemplo** por tabla. Siempre **datos ficticios**.
- Un script de carga inicial `seed.py` que crea las tablas (`create_all`) y carga los datos **si la base está vacía** (ver sección 9 de la guía). Se ejecuta antes de levantar el servidor. En Render el disco se borra al reiniciar: así la API siempre arranca con datos.
- El archivo `.db` **no se sube** a GitHub (agregalo al `.gitignore`); se genera solo.

### Seguridad: TODOS los endpoints van protegidos
- Todos los endpoints piden la API key en el encabezado `X-API-Key`.
- La clave se define como una constante al principio de `main.py`. Más adelante en la carrera van a ver cómo sacarla del código con variables de entorno; por ahora, así.
- Como la clave está a la vista en el repo, **los datos son todos ficticios** y no se usa esta API para nada real.
- Sin clave o con clave incorrecta → **401**.

Se protege toda la app de una vez:

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader

CLAVE = "clave-de-prueba-2026"   # clave del grupo
header = APIKeyHeader(name="X-API-Key")

def verificar(clave: str = Depends(header)):
    if clave != CLAVE:
        raise HTTPException(status_code=401, detail="API key invalida")

app = FastAPI(dependencies=[Depends(verificar)])
```

En `/docs` usá el botón **Authorize** para cargar la clave y probar.

---

## Nivel A — obligatorio (igual para todos)

Cada grupo implementa **exactamente estos 6 endpoints**, adaptados a su tema (ver *Alcance de este grupo*):

| # | Tipo | Ejemplo genérico | Qué practica |
|---|---|---|---|
| 1 | Listado con filtro | `GET /cosas?campo=valor` | Query param, `select(...).where(...)` |
| 2 | Detalle | `GET /cosas/{id}` | Path param, **404** si no existe |
| 3 | Relación | `GET /cosas/{id}/otras` | Cruzar dos tablas por la clave foránea (`relationship` o filtro por FK) |
| 4 | Segundo listado con filtro | `GET /otras?campo=valor` | Query param sobre otra tabla |
| 5 | Calculado | `GET /resumen` | Contar, sumar o agrupar (en Python o con `func` de SQLAlchemy) |
| 6 | Alta | `POST /cosas` | Recibir el cuerpo como `dict`, **validar a mano** (400 si está mal) e insertar con la sesión |

Además, en Nivel A:
- **Errores:** 401 (sin clave), 404 (no existe), y la API no se cae si la base no está o falla una consulta (`try/except`).
- **Filtros opcionales:** si no se manda el query param, devuelve todo.
- **Deploy:** URL pública en Render con `/docs` operativo.
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
2. URL pública en Render con `/docs` funcionando.
3. Video demo (máx. 5 min): endpoints funcionando con clave, y un pedido **sin** clave mostrando el 401.
4. Defensa oral: demo en vivo desde `/docs` y preguntas sobre el código.

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
