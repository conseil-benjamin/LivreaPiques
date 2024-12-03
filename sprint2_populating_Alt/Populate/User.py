import pandas as pd
import numpy as np
from SQL_controleur.SQL_controleur import insert

def traitement_data():
    """
    This function is used to read the data from the csv file and to clean it.
    
    Returns:
    data: DataFrame with the columns of the table 'User' to insert in the table 'User'
    """
    data = pd.read_csv('new_data/user.csv')

    #renommage des champs pour insertion
    data.rename(columns={'id': 'user_id',
                         'nb_book_year': 'nb_book_per_year',
                         'nb_book_pleasure_year': 'nb_book_pleasure',
                         'nb_book_professional_year': 'nb_book_work',
                         'initiator': 'initiated_by',
                         'when_reading': 'reading_time',
                         'makes_you_want_read': 'choice_motivation'
                         }, inplace=True)
    
    # Traitement gender

    # Supprimer les espaces autour
    data['gender'] = data['gender'].str.strip()

    # Remplacer les valeurs incorrectes
    data['gender'] = data['gender'].replace({'H': 'M', 'F': 'F'})  
    
    return data

def __main__():
    """
    This function is used to insert the data in the table 'book'
    """
    print("Traitement des données des utilisateurs")
    data = traitement_data()
    insert(data, 'User')
    