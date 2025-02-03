import pandas as pd
from sqlalchemy import create_engine, select, Table, MetaData
from sqlalchemy.orm import sessionmaker
import yaml
import time
from tqdm import tqdm

def get_data(query):
    return True

def recoUserBased(user, userDF, k=5):
    dicoRecos = {}
    dicoUserSim = {}
    # On recupere les livres lus par l'utilisateur
    livresLus = set(user['liked_books'])
    # On recupere les livres preferes de l'utilisateur
    livresPref = set(user['favorite_books'])

    #on ajoute les livres preferes dans les livres lus si ils ne sont pas deja presents
    livresLus = livresLus.union(livresPref)
    # On recupere les livres lus par les autres utilisateurs
    
    for i, u in userDF.iterrows():
        if u['username'] != user['username']:
            livresLusAutre = set(u['liked_books'])
            # On calcule le nombre de livres en commun entre l'utilisateur et les autres utilisateurs
            nbLivreCommun = len(livresLus.intersection(livresLusAutre))
            # On calcule le score de similarite entre l'utilisateur et les autres utilisateurs
            score = nbLivreCommun
            dicoUserSim[u['username']] = score
    
    # On trie les utilisateurs en fonction de leur score de similarite
    dicoUserSim = dict(sorted(dicoUserSim.items(), key=lambda item: item[1], reverse=True))
    
    # quel sont les livre non lu par l'utilisateur qui sont lu par les utilisateurs les plus similaires (le 1er qartile)
    for u in list(dicoUserSim.keys())[:len(dicoUserSim)//4]:
        for livre in userDF[userDF['username'] == u]['liked_books'].values[0]:
            if livre not in livresLus:
                if livre in dicoRecos:
                    dicoRecos[livre] += 1
                else:
                    dicoRecos[livre] = 1
    # si le dictionnaire est vide on continue avec les 10 utilisateurs suivants les plus similaires tant que le dictionnaire est vide
    i = 0
    while len(dicoRecos) == 0 and i < 10:
        for u in list(dicoUserSim.keys())[i*len(dicoUserSim)//4:(i+1)*len(dicoUserSim)//4]:
            for livre in userDF[userDF['username'] == u]['liked_books'].values[0]:
                if livre not in livresLus:
                    if livre in dicoRecos:
                        dicoRecos[livre] += 1
                    else:
                        dicoRecos[livre] = 1
        i += 1
    print(i)
    # On trie les livres en fonction du nombre de fois qu'ils ont ete recommandes
    dicoRecos = dict(sorted(dicoRecos.items(), key=lambda item: item[1], reverse=True))
    return dicoRecos

