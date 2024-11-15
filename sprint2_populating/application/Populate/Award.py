import pandas as pd
import numpy as np

from SQL_controleur.SQL_controleur import insert, insert_table_assocation

def traitement_data():
    data = pd.read_csv('new_data/books_corrected.csv')

    # Remove all unnamed columns
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

    #keep only award and title
    data = data[['title', 'awards']]

    data_awards = data[['awards']]
    # Remove the NaN values
    data_awards = data_awards.dropna()
    # Remove the duplicates
    data_awards = data_awards.drop_duplicates()

    # Rename the column awards to name_awards
    data_awards = data_awards.rename(columns={'awards': 'award_name'})

    # Remove the nan values
    data = data.dropna()

    # rename the column 'title' to 'book_title' and 'awards' to 'award_name'
    data = data.rename(columns={'title': 'book_title', 'awards': 'award_name'})

    return data, data_awards

def __main__():
    data_association, data_table = traitement_data()
    #insert(data_table, 'awards')
    #insert_table_assocation(data_association, 'book', 'awards', 'book_title', 'award_name', 'book_id', 'award_id')
