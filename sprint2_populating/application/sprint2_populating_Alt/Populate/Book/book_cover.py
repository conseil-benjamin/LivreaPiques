import pandas as pd
from SQL_controleur.SQL_controleur import update 

def traitement_data():
    """
    Reads and cleans the book data from CSV, preparing it for SQL update.

    Returns:
    pd.DataFrame: DataFrame containing book_id and book_cover columns.
    """
    data = pd.read_csv('new_data/books_with_cover.csv')

    # Sélection des colonnes nécessaires
    colonnes_dans_ordre = ['id', 'cover+AF8-link']
    data_reordered = data[colonnes_dans_ordre].copy()

    # Renommage des colonnes pour correspondre à la table SQL
    data_reordered = data_reordered.rename(columns={
        'id': 'book_id',
        'cover+AF8-link': 'book_cover'
    })
    
    return data_reordered

def __main__():
    """
    Updates book covers in the database based on book_id.
    """

    data_reordered = traitement_data()

    for index, row in data_reordered.iterrows():
        book_id = row['book_id']
        book_cover = row['book_cover']

        update('book', {'book_cover': book_cover}, {'book_id': book_id})

