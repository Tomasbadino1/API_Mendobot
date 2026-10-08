# ===================
# Validación de sedes
# ===================
def validation_locations(data: dict, partial: bool = False) -> dict:
    name = data.get("name")
    city = data.get("city")
    address = data.get("address")
    clean = {}
    if not partial or "name" in data:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name es obligatorio y no puede estar vacío")
        if len(name) > 30:
            raise ValueError("Nombre no puede superar los 30 caracteres")
        clean["name"] = name.strip()
    
    if not partial or "city" in data:
        if not isinstance(city, str) or not city.strip():
                raise ValueError("Ciudad es obligatorio y no puede estar vacío")
        if len(city) > 30:
                raise ValueError("Ciudad no puede superar los 30 caracteres")
        clean["city"] = city.strip()
    
    if not partial or "address" in data:
        if not isinstance(address, str) or not address.strip():
                raise ValueError("Dirección es obligatorio y no puede estar vacío")
        if len(address) > 30:
                raise ValueError("Dirección no puede superar los 30 caracteres")
        clean["address"] = address.strip()

    return clean

# =========================
# Validación de carreras
# =========================

def validation_carrers(data: dict, partial: bool = False) -> dict:
    name = data.get("name")
    code = data.get("code")
    mode = data.get("mode")
    id_locations = data.get("id_locations")
    clean = {}
    
    if not partial or "name" in data:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Nombre es obligatorio y no puede estar vacío")
        if len(name) > 30:
            raise ValueError("Nombre no puede superar los 30 caracteres")
        clean["name"] = name.strip()
    
    if not partial or "code" in data:
        if not isinstance(code, str) or not code.strip():
            raise ValueError("Código es obligatorio y no puede estar vacío")
        if len(code) > 10:
            raise ValueError("Código no puede superar los 10 caracteres")
        clean["code"] = code.strip()
   
    if not partial or "mode" in data:
        if not isinstance(mode, str) or not mode.strip():
            raise ValueError("Modo es obligatorio y no puede estar vacío")
        if len(mode) > 20:
            raise ValueError("Modo no puede superar los 20 caracteres")
        clean["mode"] = mode.strip()
   
    if not partial or "id_locations" in data:
        if not isinstance(id_locations, int) or isinstance(id_locations, bool):
            raise ValueError("ID de sede es obligatorio o la id de la sede no existe")
        clean["id_locations"] = id_locations

    return clean

# =========================
# Validación de estudiantes
# =========================

def validation_students(data: dict, partial:bool = False) -> dict:
    name = data.get("name")
    archivo = data.get("file")
    anio_de_curso = data.get("year_student")
    carrera_id = data.get("career_id")

    clean = {}
   
    if not partial or "name" in data:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Nombre es obligatorio y no puede estar vacío")
        if len(name) > 30:
            raise ValueError("Nombre no puede superar los 30 caracteres")
        clean["name"] = name.strip()
    
    if not partial or "file" in data:
        if not isinstance(archivo, str) or not archivo.strip():
            raise ValueError("Archivo es obligatorio y no puede estar vacío")
        clean["file"] = archivo.strip()

    if not partial or "year_student" in data:
        if not isinstance(anio_de_curso, int) or not 0 < anio_de_curso <= 5:
            raise ValueError("Año de curso es obligatorio y debe estar entre 1 y 5")
        clean["year_student"] = anio_de_curso

    if not partial or "career_id" in data:
        if not isinstance(carrera_id, int) or isinstance(carrera_id, bool):
            raise ValueError("ID de carrera es obligatorio o la id de la carrera no existe")
        clean["career_id"] = carrera_id
    
    return clean