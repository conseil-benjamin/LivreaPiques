import pandas as pd
from SQL_controleur.SQL_controleur import update 

def traitement_data():
    data = pd.read_csv('new_data/books_id_with_cover.csv')

    data_reordered = data[['id', 'cover_link']].copy()
    data_reordered = data_reordered.rename(columns={'id': 'book_id', 'cover_link': 'book_cover'})

    return data_reordered

def __main__():
    data_reordered = traitement_data()
    update(data_reordered)