import pandas as pd
import numpy as np
from SQL_controleur.SQL_controleur import insert_table_assocation

def traitement_data():
    # Charger les fichiers CSV
    formulair_corrected_data = pd.read_csv('new_data/formulair_corrected.csv')
    formulair_corrected_data['username'] = formulair_corrected_data['email'].apply(lambda x: x.split('@')[0] if '@' in str(x) else x)
    formulair_corrected_data = formulair_corrected_data[['username','favorite_book_1','favorite_book_2','favorite_book_3']]
    data = formulair_corrected_data.melt(id_vars=['username'], 
                                      value_vars=['favorite_book_1', 'favorite_book_2', 'favorite_book_3'], 
                                      var_name='book_type', 
                                      value_name='book_title')
    data_association = data[['username', 'book_title']]
    return data_association

def __main__():

    print("Traitement des données des liver aimer")
    data_association = traitement_data()
    insert_table_assocation(data_association, 'user', 'book', 'username', 'book_title', 'user_id', 'book_id', 'liked_books')