import pandas as pd
import numpy as np

from utils.SQL_controleur.SQL_controleur import insert, insert_table_assocation_book

def traitement_data():
    """
    This function is used to read the data from the csv file and to clean it.

    Returns:
    data: DataFrame with the columns 'book_title' and 'award_name' to insert in the table 'book_awards'
    data_awards: DataFrame with the column 'award_name' to insert in the table 'awards'
    """
    data = pd.read_csv('new_data/books_corrected.csv')

    # Remove all unnamed columns
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

    #keep only award and id
    data = data[['id', 'awards']]

    data_awards = data[['awards']]
    # Remove the NaN values
    data_awards = data_awards.dropna()
    # Remove the duplicates
    data_awards = data_awards.drop_duplicates()

    # Rename the column awards to name_awards
    data_awards = data_awards.rename(columns={'awards': 'award_name'})

    # Remove the nan values
    data = data.dropna()

    # rename the column 'id' to 'book_id' and 'awards' to 'award_name'
    data = data.rename(columns={'id': 'book_id', 'awards': 'award_name'})

    return data, data_awards

def __main__():
    """
    This function is used to insert the data in the table 'awards' and 'book_awards'
    """
    print("Traitement des données des awards")
    data_association, data_table = traitement_data()
    insert(data_table, 'awards')
    insert_table_assocation_book(data_association, 'awards', 'award_name', 'award_id')