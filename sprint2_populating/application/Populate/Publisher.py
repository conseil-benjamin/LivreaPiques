import pandas as pd
import numpy as np

from SQL_controleur.SQL_controleur import insert, insert_table_assocation_book

def traitement_data():
    """
    This function is used to read the data from the csv file and to clean it.

    Returns:
    data2: DataFrame with the columns 'book_title' and 'name_publisher' to insert in the table 'book_publisher'
    data: DataFrame with the column 'name_publisher' to insert in the table 'publisher'
    """
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
    data2 = data2[['id', 'publisher']]
    data2 = data2.rename(columns={'publisher': 'name_publisher', 'id': 'book_id'})
    data2 = data2.dropna()

    return data2, data

def __main__():
    """
    This function is used to insert the data in the table 'publisher' and 'book_publisher'
    """
    print("Traitement des données des éditeurs")
    data_association, data_table = traitement_data()
    insert(data_table, 'publisher')
    insert_table_assocation_book(data_association, 'publisher', 'name_publisher', 'publisher_id')