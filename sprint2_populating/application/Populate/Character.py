import pandas as pd
import numpy as np

from utils.SQL_controleur.SQL_controleur import insert, insert_table_assocation_book

def traitement_data():
    """
    This function is used to read the data from the csv file and to clean it.
    
    Returns:
    df_exploded: DataFrame with the columns 'book_title' and 'character_name' to insert in the table 'book_characters'
    data2: DataFrame with the column 'character_name' to insert in the table 'characters'
    """
    # Charger les données et enlever les colonnes 'Unnamed'
    data = pd.read_csv('new_data/books_corrected.csv')
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

    # Garder uniquement les colonnes 'title' et 'characters'
    data = data[['id', 'characters']]

    # Enlever les lignes avec des valeurs manquantes
    data = data.dropna()

    #renommer la colonne 'id' en 'book_id'
    data = data.rename(columns={'id': 'book_id'})

    df = pd.DataFrame(data)

    # Séparer les personnages et garder l'info du titre pour chaque personnage
    df_exploded = df.assign(characters=df['characters'].str.split(', ')).explode('characters').reset_index(drop=True)

    # rename the column to "character_name"
    df_exploded.columns = ['book_id', 'character_name']

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
    """
    This function is used to insert the data in the table 'characters' and 'book_characters'
    """
    print("Traitement des données des personnages")
    data_association, data_table = traitement_data()
    print(data_association.head(20))
    insert(data_table, 'characters')
    insert_table_assocation_book(data_association, 'characters', 'character_name', 'character_id')