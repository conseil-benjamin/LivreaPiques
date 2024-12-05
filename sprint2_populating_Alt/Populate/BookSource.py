import pandas as pd
import numpy as np
from SQL_controleur.SQL_controleur import insert, insert_table_assocation

def traitement_data():
    """
    This function is used to read the data from the csv file and to clean it.
    
    Returns:
    data_associations: DataFrame to insert in the table 'User_Book_Source'
    data_table: DataFrame to insert in the table 'Book_Source'
    """
    user_df = pd.read_csv('new_data/user.csv')
    book_source_df = pd.read_csv('new_data/book_source.csv')
    associations_df = pd.read_csv('new_data/Associations_book_source.csv')

    # Fusionner associations avec user.csv sur "id"
    merged_df = associations_df.merge(user_df[['id', 'username']], left_on='id', right_on='id')

    # Fusionner le résultat avec book_source.csv sur "origin_id"
    final_df = merged_df.merge(book_source_df, left_on='origin_id', right_on='origin_id')

    # Garder les colonnes nécessaires pour l'association
    data_associations = final_df[['id', 'origin_id', 'username', 'origin_of_books']]

    #renommage des champs pour insertion
    data_table = book_source_df

    data_table.rename(columns={'origin_id': 'source_id',
                               'origin_of_books': 'source_name'
                              }, inplace=True)
    
    data_associations.rename(columns={'id': 'user_id',
                                      'origin_id': 'source_id',
                                      'origin_of_books': 'source_name'
                                     }, inplace=True)
            
    return data_associations, data_table

def __main__():
    """
    This function is used to insert the data in the tables 'Book_Source' and 'User_Book_Source'
    """
    print("Traitement des données des sources de livres")
    data_associations, data_table = traitement_data()
    insert(data_table, 'book_source')
    insert_table_assocation(data_associations, 'user', 'book_source', 'username', 'source_name', 'user_id', 'source_id')
    