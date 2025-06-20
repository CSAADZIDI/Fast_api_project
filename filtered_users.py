import json
from pathlib import Path
import pandas as pd
    
USERS_FILE = "data/users.json"
FILTERED_USERS_FILE = "data/filtered_users.json"
USER_DATA_FIELDS = ['login', 'id', 'created_at', 'avatar_url', 'bio']

def load_users(filepath) -> list:
    loaded_users = []
    ignored_users = 0
    fichier = Path(filepath)

    if fichier.exists() and fichier.is_file():
        with open(filepath, "r", encoding="utf-8") as file:
            data_users = json.load(file)
            
          
    if len(data_users): 
        #print("init loaded",len(data_users))   
        assert isinstance(data_users, list), "data_users doit être une liste"
        
        
        for user in data_users:
            if type(user) == dict:
                loaded_users.append(user)
            else:
                ignored_users += 1
        #print("ignored users", ignored_users)   
        #print("len loaded",len(loaded_users))
        
        assert all(isinstance(user, dict) for user in loaded_users), "Tous les éléments doivent être des dictionnaires"
        
             
        for user in loaded_users:
            assert set(USER_DATA_FIELDS).issubset(user.keys()), \
            f"L'utilisateur {user.get('login')} n'a pas toutes les clés requises"
        return loaded_users
    else:
        return None
    
def remove_duplicates(users:list) -> pd.DataFrame: 
    df = pd.DataFrame(users)
    #print("len df",len(df))
    # Trouver les lignes en double
    duplicates = df[df.duplicated()]
    #if len(duplicates):
    #    print("Doublons trouvés :")
    #   print(duplicates)
    df.drop_duplicates(subset=["id"], inplace=True)
    #print("len df après",len(df))
    return df
    
def filter_users(users:pd.DataFrame)-> pd.DataFrame: 
    df_bio_filter = users[~users['bio'].isna() & (users["bio"] != "null")]
    #print("dim après bio filter", len(df_bio_filter))
    df_avatar_url_filter = df_bio_filter[~df_bio_filter['avatar_url'].isna()]
    #print("dim après url filter", len(df_avatar_url_filter))
    
    df_avatar_url_filter['created_at'] = pd.to_datetime(df_avatar_url_filter['created_at'])
    df_created_at_filter = df_avatar_url_filter[df_avatar_url_filter['created_at']  > pd.to_datetime("2007-01-01T00:00:00Z") ]
    
    # Reconvertir au format ISO string (format d'origine)
    df_created_at_filter['created_at'] = df_created_at_filter['created_at'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    #print("dim après created_at filter", len(df_created_at_filter))
    return df_created_at_filter
    
def _create_users_file(pathfile):
    fichier = Path(pathfile)

    if not(fichier.exists() and fichier.is_file()):
            #print("Le fichier n'existe pas. on va le crée")
            # Crée le dossier data/ s'il n'existe pas
            Path("data").mkdir(parents=True, exist_ok=True)

            # Crée un fichier vide
            
            fichier.touch()
            
    else:
            #print("✅ Le fichier existe.")
            pass
               
def save_filtered_users(users :pd.DataFrame, output_path):
        if not users.empty:
            _create_users_file(output_path)
            
            users.to_json(output_path, orient="records", indent=2)

if __name__ == "__main__":
    users = load_users(USERS_FILE)
    print("Utilisateurs chargés : ", len(users))

    if users:
        users_without_duplicated = remove_duplicates(users)  # dataframe
        print("Doublons supprimés : ", len(users_without_duplicated) - len(users_without_duplicated))

        users_filtered = filter_users(users_without_duplicated)
        print("Utilisateurs filtrés :", len(users_filtered))
        
        save_filtered_users(users_filtered, FILTERED_USERS_FILE)