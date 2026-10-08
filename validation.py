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
            raise ValueError("Name is required and cannot be empty")
        if len(name) > 30:
            raise ValueError("Name cannot exceed 30 characters")
        clean["name"] = name.strip()
    
    if not partial or "city" in data:
        if not isinstance(city, str) or not city.strip():
            raise ValueError("City is required and cannot be empty")
        if len(city) > 30:
            raise ValueError("City cannot exceed 30 characters")
        clean["city"] = city.strip()
    
    if not partial or "address" in data:
        if not isinstance(address, str) or not address.strip():
            raise ValueError("Address is required and cannot be empty")
        if len(address) > 30:
            raise ValueError("Address cannot exceed 30 characters")
        clean["address"] = address.strip()

    return clean

# =========================
# Validación de carreras
# =========================

def validation_careers(data: dict, partial: bool = False) -> dict:
    name = data.get("name")
    code = data.get("code")
    mode = data.get("mode")
    id_locations = data.get("id_locations")
    clean = {}
    
    if not partial or "name" in data:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name is required and cannot be empty")
        if len(name) > 30:
            raise ValueError("Name cannot exceed 30 characters")
        clean["name"] = name.strip()
    
    if not partial or "code" in data:
        if not isinstance(code, str) or not code.strip():
            raise ValueError("Code is required and cannot be empty")
        if len(code) > 10:
            raise ValueError("Code cannot exceed 10 characters")
        clean["code"] = code.strip()
   
    if not partial or "mode" in data:
        if not isinstance(mode, str) or not mode.strip():
            raise ValueError("Mode is required and cannot be empty")
        if len(mode) > 20:
            raise ValueError("Mode cannot exceed 20 characters")
        clean["mode"] = mode.strip()
   
    if not partial or "id_locations" in data:
        if not isinstance(id_locations, int) or isinstance(id_locations, bool):
            raise ValueError("Location ID is required or location ID does not exist")
        clean["id_locations"] = id_locations
    
    return clean

#  =========================
#  Validación de estudiantes
#  =========================

def validation_students(data: dict, partial:bool = False) -> dict:
    name = data.get("name")
    archivo = data.get("file")
    anio_de_curso = data.get("year_student")
    carrera_id = data.get("career_id")

    clean = {}
   
    if not partial or "name" in data:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name is required and cannot be empty")
        if len(name) > 30:
            raise ValueError("Name cannot exceed 30 characters")
        clean["name"] = name.strip()
    
    if not partial or "file" in data:
        if not isinstance(archivo, str) or not archivo.strip():
            raise ValueError("File is required and cannot be empty")
        clean["file"] = archivo.strip()

    if not partial or "year_student" in data:
        if not isinstance(anio_de_curso, int) or not 0 < anio_de_curso <= 5:
            raise ValueError("Student year is required and must be between 1 and 5")
        clean["year_student"] = anio_de_curso

    if not partial or "career_id" in data:
        if not isinstance(carrera_id, int) or isinstance(carrera_id, bool):
            raise ValueError("Career ID is required or career ID does not exist")
        clean["career_id"] = carrera_id
    
    return clean