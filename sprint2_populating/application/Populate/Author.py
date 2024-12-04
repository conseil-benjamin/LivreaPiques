import pandas as pd
import numpy as np

from SQL_controleur.SQL_controleur import insert, insert_table_assocation_book

def traitement_data():
    """
    This function reads the CSV file containing the authors data, cleans it and returns a DataFrame with the cleaned data.
    
    Returns:
    - df: DataFrame with the cleaned data
    - df_books: DataFrame with the cleaned data of the books
    """

    # Charger le CSV dans un DataFrame
    csv_file_path = 'new_data/CleanedAuthors.csv'
    df = pd.read_csv(csv_file_path)

    # Sélectionner uniquement les colonnes nécessaires
    df = df[["author_name", "author_gender", "birthplace"]]

    # Supprimer les ligne avec le même nom d'auteur
    df = df.drop_duplicates(subset=['author_name'])



    # Remplacer "female" par "F", "male" par "M" et autres par "A" dans la colonne `author_gender`
    df['author_gender'] = df['author_gender'].replace({
        'female': 'F',
        'male': 'M'
    }).fillna('A')

    # Filtrer les valeurs de `author_gender` pour n'autoriser que les valeurs de l'ENUM
    valid_genders = ['M', 'F', 'A']
    df = df[df['author_gender'].isin(valid_genders)]

    # Charger le CSV des livres
    csv_book = 'new_data/books_corrected.csv'
    df_books = pd.read_csv(csv_book)
    df_books = df_books[["id", "author"]]
    df_books = df_books.rename(columns={"author": "author_name", "id": "book_id"})

    return df_books, df

def __main__():
    """
    This function processes the authors data and inserts it into the database.
    """
    print("Traitement des données des auteurs")
    data_association, data_table = traitement_data()
    insert(data_table, 'author')
    insert_table_assocation_book(data_association, 'author', 'author_name', 'author_id')