# Comentarios de la cátedra

Informática (TDS05) · Proyecto Integrador · UM Río Cuarto

Acá va la devolución de cada revisión semanal. Léanlo antes de seguir programando.
El alcance completo del grupo está en el documento de alcances.

**Grupo:** Tomás Badino, Nicolás Molinero
**Tema:** Mendobot — Ingreso y beneficios

---

## 23/09

**Lo que hay:** FastAPI levanta y responde en `/`. `requirements.txt` está armado. `data.py` está vacío.

**A corregir**
- La API key va como constante al principio de `main.py`, pero con un nombre claro y en mayúsculas: `CLAVE = "..."` en vez de `x_api_key_x = 123`. Todavía no hace falta variable de entorno.
- Falta agregar `gunicorn` y `uvicorn-worker` a `requirements.txt` para el deploy.
- `data.py` vacío: los datos ahora van en SQLite, así que reemplazalo por `seed.py`.

**Próximos pasos**
1. Proteger toda la app de una vez con `FastAPI(dependencies=[Depends(verificar)])`.
2. `seed.py` con las 3 tablas: `carreras`, `requisitos`, `beneficios`.
3. Repartir los endpoints entre los dos: los commits tienen que mostrar el aporte de cada uno.

**Sobre los datos:** la UM no publica un listado ordenado de becas con porcentajes. Usen la tabla `beneficios` con `tipo` (beca / descuento / convenio) y dejen `porcentaje` vacío cuando no se publique. Sirven las Becas Santander, las deportivas, las de idiomas y el 50% del arancel para hijos de personal.

**Endpoints a entregar (Nivel A)**
- [ ] `GET /beneficios?tipo=beca`
- [ ] `GET /beneficios/{id}` (404 si no existe)
- [ ] `GET /carreras/{id}/requisitos`
- [ ] `GET /carreras?modalidad=presencial`
- [ ] `GET /beneficios/resumen` (cantidad por tipo)
- [ ] `POST /beneficios`
- [ ] Todos protegidos con `X-API-Key` (clave como constante en `main.py`)
