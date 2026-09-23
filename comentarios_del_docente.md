# Comentarios de la cátedra

Informática (TDS05) · Proyecto Integrador · UM Río Cuarto

Acá va la devolución de cada revisión semanal. Léanlo antes de seguir programando.
El alcance completo del grupo está en el documento de alcances.

**Grupo:** Tomás Badino, Nicolás Molinero
**Tema:** Mendobot — Carreras, sedes y estudiantes

---

## 23/09

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

**Endpoints a entregar (Nivel A)**
- [ ] `GET /estudiantes?anio_cursada=1`
- [ ] `GET /estudiantes/{id}` (404 si no existe)
- [ ] `GET /carreras/{id}/estudiantes`
- [ ] `GET /sedes?ciudad=Rio Cuarto`
- [ ] `GET /resumen` (estudiantes por carrera y por sede)
- [ ] `POST /estudiantes`
- [ ] Todos protegidos con `X-API-Key` (clave como constante en `main.py`)
