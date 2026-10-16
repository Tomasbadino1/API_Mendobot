import os 
from fastapi import HTTPException, Header 
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("KEY")

def verify(x_api_key: str = Header(None)):
    "Rejects the request if no API Key is set in the environment or if the provided key does not match."
    if not KEY or not x_api_key or x_api_key != KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")