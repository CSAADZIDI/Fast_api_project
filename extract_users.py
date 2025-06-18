# Script d'extraction depuis l’API GitHub
import requests
from dotenv import load_dotenv
import os
import json
import argparse
import time
from datetime import datetime,timezone
from pathlib import Path

load_dotenv()

USERS_FILE = "data/users.json"
DEFAULT_MIN_NUM_USERS_PER_REQ = 30
DEFAULT_MAX_NUM_USERS_PER_REQ = 100
SINCE_ID = 0
MAX_RETRIES = 5


def _get_headers():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("GITHUB_TOKEN non défini dans le fichier .env")
    return {"Authorization": f"token {token}"}

def _check_rate_limit(response):
    remaining = int(response.headers.get("X-RateLimit-Remaining", "1"))
    reset_ts = int(response.headers.get("X-RateLimit-Reset", time.time()))
    now_ts = int(time.time())

    if remaining == 0:
        wait_time = max(reset_ts - now_ts, 0)

        reset_time = datetime.fromtimestamp(reset_ts, tz=timezone.utc)
        reset_str = reset_time.strftime("%Y-%m-%d %H:%M:%S %Z")

        print(f"Quota API épuisé. Pause jusqu'à {reset_str} ({wait_time} sec)...")
        time.sleep(wait_time + 1)
        return True

    return False
    
def _safe_request(url, headers, retry=0):
    try:
        response = requests.get(url, headers=headers)
        if _check_rate_limit(response):
            return _safe_request(url, headers, retry)

        status = response.status_code

        if status == 200:
            return response

        elif status == 403:
            print("Erreur 403 - Token invalide ou quota dépassé.")
            return None

        elif status == 429:
            wait_time = 2 ** retry
            print(f"Erreur 429 - Trop de requêtes. Pause de {wait_time} secondes...")
            time.sleep(wait_time)
            return _safe_request(url, headers, retry + 1)

        elif 500 <= status < 600:
            wait_time = 2 ** retry
            print(f"Erreur {status} - Serveur GitHub indisponible. Réessai dans {wait_time} secondes...")
            time.sleep(wait_time)
            return _safe_request(url, headers, retry + 1)

        else:
            print(f"Requête échouée avec le code {status}")
            return None

    except requests.RequestException as e:
        print(f"Exception réseau : {e}")
        time.sleep(2 ** retry)
        return _safe_request(url, headers, retry + 1)
    
    
def _extract_user(login):
    
    url = f"https://api.github.com/users/{login}"
    headers = _get_headers()
    
    response = _safe_request(url, headers)

    if not response:
        return None
    
    user_data = response.json()
    
    return {"login" : login,
            "id" : user_data["id"],
           "created_at" : user_data["created_at"],
           "avatar_url" : user_data["avatar_url"],
           "bio" : user_data["bio"] if "bio" in user_data.keys() else "null"
           }


def _extract_batch_users(id, num_users_per_page):
    extracted_users = []
    url = f"https://api.github.com/users?since={id}&per_page={num_users_per_page}"
    headers = _get_headers()
    response = _safe_request(url, headers)

    if not response:
        return None
    
    data_users = response.json()
    #print("keys",data_users[0].keys())
    users_num = len(data_users)
    print(users_num)
    for user in data_users:
        user_login = user["login"]
        print("user_login", user_login)
        user_data = _extract_user(user_login)
        # Append the new extracted user to the list of users
        extracted_users.append(user_data)
    # Save all users to the file
    _save_users(extracted_users)

def _create_users_file():
    fichier = Path(USERS_FILE)

    if not(fichier.exists() and fichier.is_file()):
            print("Le fichier n'existe pas. on va le crée")
            # Crée le dossier data/ s'il n'existe pas
            Path("data").mkdir(parents=True, exist_ok=True)

            # Crée un fichier vide
            
            fichier.touch()
            
    else:
            print("✅ Le fichier existe.")
         
def _save_users(users):
    if users:
        _create_users_file()
            
        with open(USERS_FILE,"w", encoding="utf-8") as file:
            json.dump(users, file, indent=4, ensure_ascii=False) 

def _paging(max_users):
    num_extracted_users = 0
    to_extract = max_users
    since_id_start_batch = SINCE_ID
    while num_extracted_users < max_users:
        batch_size = min(to_extract, DEFAULT_MAX_NUM_USERS_PER_REQ)
        print("batch_size", batch_size)
        _extract_batch_users(since_id_start_batch,batch_size)
        num_extracted_users += batch_size
        print("déja fait num_extracted_users", num_extracted_users)
        to_extract -= batch_size
        print(" reste to_extracted",to_extract)
        since_id_start_batch += batch_size 
        print(" commence à partir de since_id_start_batch",since_id_start_batch)
        
            
        
        
         
        
def main(max_users):
    print(f"Extraction de {max_users} utilisateurs...") 
    
    print("max_users",max_users)
    _paging(max_users)
     
        
    


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Script pour extraire des utilisateurs")

    # Définir l'argument --max-users
    parser.add_argument(
        "--max-users",
        type=int,
        help="Nombre maximum d'utilisateurs à extraire"
    )

    args = parser.parse_args()

    # Appel de la fonction principale avec l'argument
    main(args.max_users)
    