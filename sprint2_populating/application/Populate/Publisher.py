import pandas as pd
import numpy as np

from SQL_controleur.SQL_controleur import insert, insert_table_assocation

def traitement_data():
    data = pd.read_csv('new_data/books_corrected.csv')
    # keep only the columns we need (publisher)
    data = data[['publisher']]
    data = data.drop_duplicates()
    data = data.dropna()
    data = data.reset_index(drop=True)
    # add column origin_publisher with all values set to null
    data['origin_publisher'] = np.nan
    # rename columns publisher to name_publisher
    data = data.rename(columns={'publisher': 'name_publisher'})

    data2 = pd.read_csv('new_data/books_corrected.csv')
    data2 = data2[['title', 'publisher']]
    data2 = data2.rename(columns={'publisher': 'name_publisher', 'title': 'book_title'})
    data2 = data2.dropna()

    return data2, data

def __main__():
    print("Traitement des données des éditeurs")
    data_association, data_table = traitement_data()
    insert(data_table, 'publisher')
    insert_table_assocation(data_association, 'book', 'publisher', 'book_title', 'name_publisher', 'book_id', 'publisher_id')