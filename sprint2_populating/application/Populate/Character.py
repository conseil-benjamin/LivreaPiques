import pandas as pd
import numpy as np

from SQL_controleur.SQL_controleur import insert, insert_table_assocation

def traitement_data():
    # Charger les données et enlever les colonnes 'Unnamed'
    data = pd.read_csv('new_data/books_corrected.csv')
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

    # Garder uniquement les colonnes 'title' et 'characters'
    data = data[['title', 'characters']]

    # Enlever les lignes avec des valeurs manquantes
    data = data.dropna()

    #renommer la colonne 'title' en 'book_title'
    data = data.rename(columns={'title': 'book_title'})

    df = pd.DataFrame(data)

    # Séparer les personnages et garder l'info du titre pour chaque personnage
    df_exploded = df.assign(characters=df['characters'].str.split(', ')).explode('characters').reset_index(drop=True)

    # rename the column to "character_name"
    df_exploded.columns = ['book_title', 'character_name']

    data2 = data[['characters']]

    # separer les noms de personnages (s'ils sont plusieurs) en utilisant la virgule
    data2 = data2['characters'].str.split(',', expand=True)

    # empiler les colonnes pour avoir une seule colonne
    data2 = data2.stack()

    # supprimer les lignes avec des valeurs manquantes
    data2 = data2.dropna()

    # supprimer les espaces en trop
    data2 = data2.str.strip()


    data2 = data2.drop_duplicates()

    # retransformer en DataFrame
    data2 = data2.to_frame()

    # réinitialiser l'index
    data2 = data2.reset_index(drop=True)

    # nommer la colonne
    data2.columns = ['character_name']
    

    return df_exploded, data2

def __main__():
    data_association, data_table = traitement_data()
    # insert(data_table, 'characters')
    #insert_table_assocation(data_association, 'book', 'characters', 'book_title', 'character_name', 'book_id', 'character_id')