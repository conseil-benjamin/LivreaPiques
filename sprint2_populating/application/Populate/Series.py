import pandas as pd
import numpy as np

from SQL_controleur.SQL_controleur import insert, insert_table_assocation_book

def traitement_data():
    """
    This function is used to read the data from the csv file and to clean it.

    Returns:
    distinct_values_df: DataFrame with the column 'series_name' to insert in the table 'series'
    data3: DataFrame with the columns 'book_title' and 'series_name' to insert in the table 'book_series'
    """
    data = pd.read_csv('new_data/books_corrected_main.csv')

    #get the "series" column of the dataframe

    series = data['series']

    #delete all the NaN values of series
    series = series.dropna()

    # Delete the parenthesis from the string

    s_no_parens = series.str.strip('()')

    # Split the string at ' #' and take the first part
    s_cleaned = s_no_parens.str.split(' #').str[0]

    #Select distinct values from s_cleaned
    distinct_values = s_cleaned.unique()

    #convert numpy array to dataframe
    distinct_values_df = pd.DataFrame(distinct_values)

    # rename the column to "series_name"
    distinct_values_df.columns = ['series_name']

    # add a column for the status of the series
    distinct_values_df['series_status'] = np.nan

    data3 = pd.read_csv('new_data/books_corrected_main.csv')

    # keep only the columns that we need (title and series)
    data3 = data3[['id', 'series']]

    data3['series'] = data3['series'].str.strip('()')

    # Split the string at ' #' and take the first part
    data3['series'] = data3['series'].str.split('#').str[0]

    # rename the column to "series_name"
    data3 = data3.rename(columns={'series': 'series_name'})

    data3 = data3.rename(columns={'id': 'book_id'})

    # remove nan values
    data3 = data3.dropna(subset=['series_name'])

    return distinct_values_df, data3

def __main__():
    """
    This function is used to insert the data in the table 'series' and 'book_series'
    """
    print("Traitement des données des series")
    data_table, data_association = traitement_data()
    insert(data_table, 'series')
    insert_table_assocation_book(data_association, 'series', 'series_name', 'series_id')