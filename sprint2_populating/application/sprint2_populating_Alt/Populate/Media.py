import pandas as pd
import numpy as np
from SQL_controleur.SQL_controleur import insert, insert_table_assocation

def traitement_data():
    """
    This function is used to read the data from the csv file and to clean it.
    
    Returns:
    data_associations: DataFrame to insert in the table 'User_Media'
    data_table: DataFrame to insert in the table 'Media'
    """
    user_df = pd.read_csv('new_data/user.csv')
    media_df = pd.read_csv('new_data/media.csv')
    associations_df = pd.read_csv('new_data/Associations_media.csv')

    # Fusionner associations avec user.csv sur "id"
    merged_df = associations_df.merge(user_df[['id', 'username']], left_on='id', right_on='id')

    # Fusionner le résultat avec reading_mean.csv sur "media_id"
    final_df = merged_df.merge(media_df, left_on='media_id', right_on='media_id')


    # Garder les colonnes nécessaires pour l'association
    data_associations = final_df[['id', 'media_id', 'username', 'favorite_media']]

    #renommage des champs pour insertion
    data_table = media_df

    data_table.rename(columns={'favorite_media': 'media_name'}, inplace=True)
    
    data_associations.rename(columns={'id': 'user_id',
                                      'favorite_media': 'media_name'
                                     }, inplace=True)
                    
    return data_associations, data_table

def __main__():
    """
    This function is used to insert the data in the tables 'Media' and 'Fav_Media'
    """
    print("Traitement des données des sources de livres")
    data_associations, data_table = traitement_data()
    insert(data_table, 'media')
    insert_table_assocation(data_associations, 'user', 'media', 'username', 'media_name', 'user_id', 'media_id', table_name='fav_medias')
    