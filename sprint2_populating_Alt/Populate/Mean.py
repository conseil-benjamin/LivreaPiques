import pandas as pd
import numpy as np
from SQL_controleur.SQL_controleur import insert, insert_table_assocation

def traitement_data():
    """
    This function is used to read the data from the csv file and to clean it.
    
    Returns:
    data_associations: DataFrame to insert in the table 'Reads_With'
    data_table: DataFrame to insert in the table 'Reading_Mean'
    """
    user_df = pd.read_csv('new_data/user.csv')
    reading_mean_df = pd.read_csv('new_data/reading_mean.csv')
    associations_df = pd.read_csv('new_data/Associations_mean.csv')

    # Fusionner associations avec user.csv sur "id"
    merged_df = associations_df.merge(user_df[['id', 'username']], left_on='id', right_on='id')

    # Fusionner le résultat avec reading_mean.csv sur "reading_mean_id"
    final_df = merged_df.merge(reading_mean_df, left_on='reading_mean_id', right_on='reading_mean_id')

    # Garder les colonnes nécessaires pour l'association
    data_associations = final_df[['id', 'reading_mean_id', 'username', 'reading_mean']]

    #renommage des champs pour insertion
    data_table = reading_mean_df

    data_table.rename(columns={'reading_mean_id': 'mean_id',
                               'reading_mean': 'mean_name'
                              }, inplace=True)
    
    data_associations.rename(columns={'id': 'user_id',
                                      'reading_mean_id': 'mean_id',
                                      'reading_mean': 'mean_name'
                                     }, inplace=True)
            
    return data_associations, data_table

def __main__():
    """
    This function is used to insert the data in the tables 'Reading_Mean' and 'Reads_With'
    insert(data_table, 'reading_mean')
    """
    print("Traitement des données des sources de livres")
    data_associations, data_table = traitement_data()
    insert_table_assocation(data_associations, 'user', 'reading_mean', 'username', 'mean_name', 'user_id', 'mean_id', table_name='reads_with')
    