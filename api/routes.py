# api/routes.py
from fastapi import APIRouter, HTTPException, Query, Depends
from .models import User
from .security import authenticate
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

# Liste des utilisateurs (remplie depuis main.py)
users_data: list[User] = []

#  GET /users/ → liste complète

@router.get(
    "/users/",
    response_model=list[User],
    summary="Lister tous les utilisateurs",
    description="Retourne la liste complète des utilisateurs filtrés (authentification requise)."
)
def get_all_users(_: str = Depends(authenticate)):
    return users_data


#  GET /users/search?q=ai → recherche floue (contient)

@router.get(
    "/users/search",
    response_model=list[User],
    summary="Rechercher des utilisateurs",
    description=(
        "Recherche dans tous les champs des utilisateurs. Le mot-clé peut être une compétence "
        "(ex: 'dev', 'ai'), un nom, un suffixe (ex: '2024') ou un nom d'équipe (ex: 'mlops'). "
        "L'authentification est requise."
    )
)
def search_users(
    q: str = Query(..., min_length=1, description="Mot-clé à chercher dans tous les champs utilisateur"),
    _: str = Depends(authenticate)  
):
    print(">>> search_users() appelée !")
    q_lower = q.lower()
    print(f"Recherche du mot-clé : {q_lower}")
    logger.info(f"Recherche : {q_lower}")
    result = []
    for user in users_data:
        user_dict = user.dict()
        # Affiche tous les champs (en minuscules) de l'utilisateur courant
        print(f"Utilisateur examiné : {user.login}")
        print(f"Champs utilisateur : {[str(value).lower() for value in user_dict.values()]}")
        logger.info(f"Utilisateur : {user.login}")
        logger.info(f"Champs : {[str(v).lower() for v in user_dict.values()]}")
        # Vérifie si le mot-clé est dans un des champs
        if any(q_lower in str(value).lower() for value in user_dict.values()):
            print(f"--> Mot-clé trouvé dans : {user.login}")
            logger.info(f"✔ trouvé : {user.login}")
            result.append(user)
    print(f"Nombre d'utilisateurs trouvés : {len(result)}")
    logger.info(f"Total : {len(result)} utilisateur(s)")
    return result

#  GET /users/{login} → recherche exacte
@router.get(
    "/users/{login}",
    response_model=User,
    summary="Consulter un utilisateur par login",
    description="Retourne les informations d'un utilisateur via une recherche exacte sur son login. Authentification requise."
)
def get_user_by_login(login: str, _: str = Depends(authenticate)):
    for user in users_data:
        
        if user.login.lower() == login.lower():
            return user
    raise HTTPException(status_code=404, detail=f"Utilisateur '{login}' non trouvé")



