# api/main.py
from fastapi import FastAPI
from .routes import router, users_data
from fastapi.responses import RedirectResponse
from .models import User
import os
import json

app = FastAPI(
    title="API GitHub Users",
    description="Extraction, filtrage et exposition d'utilisateurs GitHub via une API REST sécurisée.",
    version="1.0.0"
    
    
)

# Chemin vers le fichier JSON ../data/filtered_users.json
current_file = os.path.abspath(__file__)
parent_dir = os.path.dirname(os.path.dirname(current_file))
data_file_path = os.path.join(parent_dir, "data", "filtered_users.json")

# Charger les données une seule fois
try:
    with open(data_file_path, "r", encoding="utf-8") as f:
        users_json = json.load(f)
        users_data.extend([User(**user) for user in users_json])
except Exception as e:
    print(f"Erreur au chargement des utilisateurs : {e}")
    users_data.clear()

# Monter les routes
app.include_router(router)

# Redirection depuis la racine vers /docs
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

