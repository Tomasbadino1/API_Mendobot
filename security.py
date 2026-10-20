import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

load_dotenv()

API_KEY = os.getenv("API_KEY")

header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify(key: str = Depends(header)):
    "Rejects the request if no API Key is set in the environment or if the provided key does not match."
    if API_KEY is None or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return key