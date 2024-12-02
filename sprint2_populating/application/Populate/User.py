import pandas as pd
import numpy as np

from SQL_controleur.SQL_controleur import insert, insert_table_assocation

def traitement_data():
    """
    This function is used to read the data from the csv file and to clean it.

    Returns:
    data: DataFrame with the columns 'book_title' and 'award_name' to insert in the table 'book_awards'
    data_awards: DataFrame with the column 'award_name' to insert in the table 'awards'
    """
    data = pd.read_csv('new_data/user.csv')

    # Remove all unnamed columns
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

    #keep only award and title
    data = data[['user_id', 'username', 'password', 'gender', 'nb_book_per_year', 'nb_book_pleasure', 'nb_book_work', 'initiated_by', 'reading_time', 'choice_motivation']]

    data_user_Series = data[['awards']]
    # Remove the NaN values
    data_user_Series = data_user_Series.dropna()
    # Remove the duplicates
    data_user_Series = data_user_Series.drop_duplicates()

    # Rename the columns names
    data_user_Series = data_user_Series.rename(columns={'awards': 'award_name'})

    # Remove the nan values
    data = data.dropna()

    # rename the columns to fit table User
    data = data.rename(columns={'title': 'book_title', 'awards': 'award_name'})

    return data, data_user_Series

def __main__():
    """
    This function is used to insert the data in the table 'awards' and 'book_awards'
    """
    print("Traitement des données des User")
    data_user, data_user_Series = traitement_data()
    insert(data_user, 'User')
    insert_table_assocation(data_user_Series, 'User', 'Series', 'username', 'series_name', 'user_id', 'series_id')
