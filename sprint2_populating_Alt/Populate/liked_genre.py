import pandas as pd
import numpy as np
from SQL_controleur.SQL_controleur import insert_table_assocation

def traitement_data():
    # Charger le fichier CSV
    data = pd.read_csv('../new_data/formulaire_genre_liked.csv')

    # Transformation pour séparer les genres et les associer à chaque utilisateur
    data_transformed = data.set_index('user')['genre'].str.split(', ', expand=True).stack().reset_index(level=0)
    data_transformed.columns = ['username', 'genre']

    return data_transformed

def __main__():
    data_associations = traitement_data
    insert_table_assocation(data_associations, 'user', 'genre', 'username', 'genre_name', 'user_id', 'genre_id', 'liked_genres')
