import pandas as pd
import numpy as np
from SQL_controleur.SQL_controleur import insert

def traitement_data():
    data = pd.read_csv('new_data/books_corrected.csv')
    # Remove all unnamed columns
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    # Remove colomns that aren't useful
    data = data.drop(columns=['series', 'publisher', 'genre_and_votes', 'characters', 'awards', 'books_in_series'])

    colonnes_dans_ordre = [
        ''
        'id',
        'title',
        'settings',
        'number_of_pages',
        'isbn', 
        'description',
        'isbn13',
        'original_title',
        'review_count',
        'one_star_ratings',   # Be warned of the plurals that we've to alligned with 'one_star_rating'
        'two_star_ratings',
        'three_star_ratings',
        'four_star_ratings',
        'five_star_ratings'
    ]

    # Reoraganize the columns of the DataFrame
    data_reordered = data[colonnes_dans_ordre].copy()

    # Renaming the columns to fit with the ones of the SQL table
    data_reordered = data_reordered.rename(columns={
        'id': 'book_id',
        'title': 'book_title',
        'number_of_pages': 'nb_of_pages',
        'description': 'book_description',
        'one_star_ratings': 'one_star_rating',
        'two_star_ratings': 'two_star_rating',
        'three_star_ratings': 'three_star_rating',
        'four_star_ratings': 'four_star_rating',
        'five_star_ratings': 'five_star_rating'
    })
    
    return data_reordered

def __main__():
    data = traitement_data()
    insert(data, 'book')
    