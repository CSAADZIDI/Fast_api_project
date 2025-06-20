import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:8000"  # Adresse locale de l'API
AUTH = HTTPBasicAuth("admin", "admin123")      # Identifiants pour HTTP Basic Auth

# 🔹 Test GET /users/
def test_get_all_users():
    response = requests.get(f"{BASE_URL}/users/", auth=AUTH)
    print("GET /users/:", response.status_code)
    print(response.json())

# 🔹 Test GET /users/{login}
def test_get_user_by_login(login):
    response = requests.get(f"{BASE_URL}/users/{login}", auth=AUTH)
    print(f"GET /users/{login}:", response.status_code)
    print(response.json())

# 🔹 Test GET /users/search?q=...
def test_search_users(query):
    response = requests.get(f"{BASE_URL}/users/search", params={"q": query}, auth=AUTH)
    print(f"GET /users/search?q={query}:", response.status_code)
    print(response.json())

# 🔹 Mots-clés à tester
BASE_URL_SEARCH = f"{BASE_URL}/users/search"
keywords = {
    "compétence": ["dev", "ai", "python"],
    "prénom ou nom": ["john", "sami"],
    "année ou suffixe": ["2024", "pro", "test"],
    "nom d’équipe": ["team", "gh", "mlops"]
}

def test_search_keywords():
    for category, terms in keywords.items():
        print(f"\nCatégorie : {category}")
        for q in terms:
            response = requests.get(BASE_URL_SEARCH, params={"q": q}, auth=AUTH)
            print(f"→ Mot-clé : '{q}' | Status: {response.status_code}")
            if response.status_code == 200:
                users = response.json()
                print(f"   → Résultats : {len(users)} utilisateur(s)")
                for user in users[:3]:  # affiche max 3 résultats
                    print(f"     - {user['login']}")
            else:
                print(f"   Erreur : {response.text}")

# ------------------------
# Appels de test
# ------------------------
test_get_all_users()
test_get_user_by_login("nitay")        
test_search_users("R&D")
test_search_keywords()
