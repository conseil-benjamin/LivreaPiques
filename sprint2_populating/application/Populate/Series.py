import pandas as pd
import numpy as np

from SQL_controleur.SQL_controleur import insert, insert_table_assocation

def traitement_data():
    data = pd.read_csv('new_data/books_corrected.csv')

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

    data3 = pd.read_csv('new_data/books_corrected.csv')

    # keep only the columns that we need (title and series)
    data3 = data3[['title', 'series']]

    data3['series'] = data3['series'].str.strip('()')

    # Split the string at ' #' and take the first part
    data3['series'] = data3['series'].str.split('#').str[0]

    # rename the column to "series_name"
    data3 = data3.rename(columns={'series': 'series_name'})

    data3 = data3.rename(columns={'title': 'book_title'})

    # remove nan values
    data3 = data3.dropna(subset=['series_name'])

    return distinct_values_df, data3

def __main__():
    print("Traitement des données des series")
    data_table, data_association = traitement_data()
    insert(data_table, 'series')
    insert_table_assocation(data_association, 'book', 'series', 'book_title', 'series_name', 'book_id', 'series_id')