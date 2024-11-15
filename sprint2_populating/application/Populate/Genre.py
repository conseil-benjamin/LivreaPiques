import pandas as pd
import numpy as np
import re
import yaml



from SQL_controleur.SQL_controleur import insert, insert_table_assocation

def traitement_data():
    """
    This function is used to read the data from the csv file and to clean it.
    
    Returns:
    unique_genres_df: DataFrame with the column 'genre_name' to insert in the table 'genre'
    book_genre_df: DataFrame with the columns 'book_id', 'genre_id' and 'nb_of_vote' to insert in the table 'book_genre'
    """

    data = 'new_data/books_corrected.csv'

    # Lire le fichier CSV par morceaux
    chunk_size = 1000  # Réduire la taille des morceaux pour éviter les problèmes de mémoire
    output_file = "book_genre.csv"
    data = 'new_data/books_corrected.csv'


    # Créer le fichier CSV avec les en-têtes
    with open(output_file, 'w') as f:
        f.write("id,genre,votes\n")

    for chunk in pd.read_csv(data, delimiter=",", low_memory=False, chunksize=chunk_size):
        # Convertir la colonne 'genre_and_votes' en chaînes de caractères
        chunk['genre_and_votes'] = chunk['genre_and_votes'].astype(str)
        
        # Itérer sur chaque ligne pour extraire les genres et les votes
        for index, row in chunk.iterrows():
            book_id = row['id']  # Assurez-vous que la colonne contenant l'ID du livre est nommée 'id'
            genres_and_votes = row['genre_and_votes']
            
            # Diviser les genres littéraires
            genres_votes_split = genres_and_votes.split(',')
            
            # Utiliser une expression régulière pour extraire le genre et le vote
            pattern = re.compile(r'(.+?)\s(-?\d+)$')
            
            for genre_vote in genres_votes_split:
                match = pattern.match(genre_vote.strip())
                if match:
                    genre = match.group(1).strip()
                    votes = int(match.group(2))
                    
                    # Écrire les résultats intermédiaires dans le fichier CSV
                    with open(output_file, 'a') as f:
                        f.write(f"{book_id},{genre},{votes}\n")

    print("Traitement terminé Genre et résultats sauvegardés dans", output_file)

    # Lire le fichier CSV généré précédemment
    data = pd.read_csv("book_genre.csv")

    # Extraire les genres uniques
    unique_genres = data['genre'].unique()

    # Créer un DataFrame pour les genres uniques
    unique_genres_df = pd.DataFrame(unique_genres, columns=['genre'])

    # Trier les genres dans l'ordre alphabétique
    unique_genres_df = unique_genres_df.sort_values(by='genre').reset_index(drop=True)

    # Sauvegarder les genres uniques dans un nouveau fichier CSV
    unique_genres_df.to_csv("unique_genres.csv", index=False)

    print("Nombre de genres uniques :", len(unique_genres))
    print("Les genres uniques ont été sauvegardés dans unique_genres.csv")

    # Lire le fichier CSV contenant les genres uniques
    unique_genres_df = pd.read_csv("unique_genres.csv")

    # Renommer la colonne pour correspondre au nom de la colonne dans la table
    unique_genres_df.rename(columns={'genre': 'genre_name'}, inplace=True)


    # Lire le fichier CSV contenant les données de book_genre
    book_genre_df = pd.read_csv("book_genre.csv")

    # Renommer les colonnes pour correspondre aux noms des colonnes dans la table book_genre
    book_genre_df.rename(columns={'id': 'book_id', 'votes': 'nb_of_vote'}, inplace=True)

    return unique_genres_df, book_genre_df

def populate_genre():
    """
    This function is used to populate the table 'book_genre' with the data from the CSV file 'book_genre.csv'.

    Returns:
    bool: True if the data has been successfully inserted, False otherwise.

    Raises:
    Exception: An error occurred while populating the database.
    """
    try:
        import pandas as pd
        from sqlalchemy import create_engine, text

        book_genre_df = traitement_data()[1]

        # Import la donnée du fichier yml
        with open('sprint2_populating/application/config.yml', 'r') as file:
            config = yaml.safe_load(file)


        # Paramètres de connexion à la base de données
        database_url = config['adress_sql']
        engine = create_engine(database_url)

        # Lire les genres de la table Genre pour obtenir les IDs des genres
        with engine.connect() as connection:
            genre_df = pd.read_sql("SELECT * FROM genre", connection)


        # Fusionner les DataFrames pour obtenir l'ID du genre
        merged_df = pd.merge(book_genre_df, genre_df, left_on='genre', right_on='genre_name', how='left')

        # Vérifier les résultats de la fusion
        print("Colonnes de merged_df :", merged_df.columns)
        print("Exemples de lignes de merged_df :", merged_df.head())

        # Sélectionner les colonnes nécessaires pour l'insertion dans la table book_genre
        book_genre_insert_df = merged_df[['book_id', 'genre_id', 'nb_of_vote']]

        # Insérer les données dans la table book_genre
        book_genre_insert_df.to_sql('book_genre', engine, if_exists='append', index=False)

        print("Les données ont été insérées dans la table book_genre.")

        return True
    except Exception as e:
        print(f"Error while populating the database: {e}")
        return False

def __main__():
    """
    This function is used to insert the data in the table 'genre' and 'book_genre'

    Raises:
    Exception: An error occurred while populating the database.
    """
    print("Traitement des données des genres")
    try:
        unique_genres_df, book_genre_df = traitement_data()
        insert(unique_genres_df, 'genre')
        populate_genre()
    except Exception as e:
        print(f"Error while populating the database: {e}")
        raise e    

