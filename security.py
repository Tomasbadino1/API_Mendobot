import os 
from fastapi import HTTPException, Header 
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("KEY")

def verify(x_api_key: str = Header(None)):
    "Si no hay clave cargada o la clave ingresada no coincide, rechaza la petición"
    if x_api_key != KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")   