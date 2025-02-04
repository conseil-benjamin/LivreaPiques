import pandas as pd
from tqdm import tqdm

from SQL_controleur.SQL_controleur import *

def get_data():
    data = requete("SELECT user_id, STRING_AGG(book_title, ' , ') AS books_liked FROM liked_books NATURAL JOIN book GROUP BY user_id")
    ret = []
    for i in range(len(data)):
        user = {}
        user['user_id'] = data.iloc[i]['user_id']
        user['liked_books'] = data.iloc[i]['books_liked'].split(' , ')
        ret.append(user)
    # transformation du dictionnaire en DataFrame
    return pd.DataFrame(ret)
 

def recoUserBased(user, userDF, k=5):
    dicoRecos = {}
    dicoUserSim = {}
    # On recupere les livres lus par l'utilisateur
    livresLus = set(user['liked_books'])

    # On recupere les livres lus par les autres utilisateurs
    
    for i, u in userDF.iterrows():

        if u['user_id'] != user['user_id']:
            livresLusAutre = set(u['liked_books'])
            # On calcule le nombre de livres en commun entre l'utilisateur et les autres utilisateurs
            nbLivreCommun = len(livresLus.intersection(livresLusAutre))
            # On calcule le score de similarite entre l'utilisateur et les autres utilisateurs
            score = nbLivreCommun
            dicoUserSim[u['user_id']] = score
    
    # On trie les utilisateurs en fonction de leur score de similarite
    dicoUserSim = dict(sorted(dicoUserSim.items(), key=lambda item: item[1], reverse=True))
    
    # quel sont les livre non lu par l'utilisateur qui sont lu par les utilisateurs les plus similaires (le 1er qartile)
    for u in list(dicoUserSim.keys())[:len(dicoUserSim)//4]:
        for livre in userDF[userDF['user_id'] == u]['liked_books'].values[0]:
            if livre not in livresLus:
                if livre in dicoRecos:
                    dicoRecos[livre] += 1
                else:
                    dicoRecos[livre] = 1
    # si le dictionnaire est vide on continue avec les 10 utilisateurs suivants les plus similaires tant que le dictionnaire est vide
    i = 0
    while len(dicoRecos) == 0 and i < 10:
        for u in list(dicoUserSim.keys())[i*len(dicoUserSim)//4:(i+1)*len(dicoUserSim)//4]:
            for livre in userDF[userDF['user_id'] == u]['liked_books'].values[0]:
                if livre not in livresLus:
                    if livre in dicoRecos:
                        dicoRecos[livre] += 1
                    else:
                        dicoRecos[livre] = 1
        i += 1
    # On trie les livres en fonction du nombre de fois qu'ils ont ete recommandes
    dicoRecos = dict(sorted(dicoRecos.items(), key=lambda item: item[1], reverse=True))
    # On retourne les k livres les plus recommandes
    ret = list(dicoRecos.keys())[:k]
    return ret

def reco_esteban(user_id, k=5):
    # Initialisation de la connexion à la base de données
    dataRecoUserBased = get_data()
    try:
        dataUserRecoUserBased = dataRecoUserBased[dataRecoUserBased['user_id'] == user_id].iloc[0]
    except:
        return []
    return recoUserBased(dataUserRecoUserBased, dataRecoUserBased, k)

