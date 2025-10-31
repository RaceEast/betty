# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Dict
import secrets

app = FastAPI(title="Auth Demo API")

security = HTTPBasic()

# 🧩 Dummy user database
USERS_DB: Dict[str, str] = {
    "ashish": "supersecret",
    "admin": "password123"
}

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    stored_password = USERS_DB.get(username)

    if not stored_password or not secrets.compare_digest(password, stored_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return username

@app.get("/")
def home():
    return {"message": "Welcome to the Auth Demo API! 🚀"}

@app.get("/secure")
def secure_data(username: str = Depends(authenticate)):
    return {"message": f"Hello, {username}! You have access to secure data 🔐"}

