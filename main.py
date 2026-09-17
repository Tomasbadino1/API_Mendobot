from fastapi import FastAPI, HTTPException, Header
import os
x_api_key_x = 123
app = FastAPI()

@app.get("/")
def inicio():
    return {"message": "Bienvenido a la API de Mendobot. Para obtener información sobre los endpoints disponibles, visita /docs."}