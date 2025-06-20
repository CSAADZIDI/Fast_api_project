import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv
import secrets

load_dotenv()

security = HTTPBasic()

# Charger et parser les identifiants depuis .env
raw_users = os.getenv("API_USERS", "")
# Exemple : "admin:admin123,user1:pass1"
user_db = dict(user.split(":") for user in raw_users.split(",") if ":" in user)

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    stored_password = user_db.get(username)

    if not stored_password or not secrets.compare_digest(password, stored_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Basic"},
        )
    return username
