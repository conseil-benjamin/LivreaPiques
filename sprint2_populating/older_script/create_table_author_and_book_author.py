import pandas as pd
from sqlalchemy import create_engine, exc

# URL de la base de données Supabase
database_url = 'postgresql://postgres.pczyoeavtwijgtkzgcaz:D0jVgaoGmDAFuaMS@aws-0-eu-west-3.pooler.supabase.com:6543/postgres'


# Création de la table `author` dans la base de données

# Créer une connexion avec la base de données
engine = create_engine(database_url)

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

try:
    # Insérer les données dans la table SQL 'author'
    df.to_sql('author', con=engine, if_exists='append', index=False)
    print("Insertion des données terminée.")

except exc.SQLAlchemyError as e:
    # Gestion des erreurs SQLAlchemy
    print("Une erreur est survenue lors de l'insertion des données :")
    print(e)
except Exception as e:
    # Gestion des autres erreurs éventuelles
    print("Une erreur inattendue est survenue :")
    print(e)

from sqlalchemy import create_engine, select, Table, MetaData
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

# Connexion à la base de données
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

# Créer l'objet MetaData sans `bind`
metadata = MetaData()

# Charger le CSV des livres
csv_book = 'new_data/books_corrected.csv'
df_books = pd.read_csv(csv_book)
df_books = df_books[["title", "author"]]
df_books = df_books.rename(columns={"author": "author_name"})

# Charger les tables book et author en utilisant `autoload_with=engine`
book_table = Table('book', metadata, autoload_with=engine)
author_table = Table('author', metadata, autoload_with=engine)

# Récupérer tous les IDs de livres et d'auteurs en une seule requête pour chaque table
book_records = session.execute(select(book_table.c.book_id, book_table.c.book_title)).all()
author_records = session.execute(select(author_table.c.author_id, author_table.c.author_name)).all()

# Créer des dictionnaires pour une recherche rapide des IDs
book_dict = {book_title: book_id for book_id, book_title in book_records}
author_dict = {author_name: author_id for author_id, author_name in author_records}

# Créer les associations en utilisant les dictionnaires, avec une barre de progression
associations = []
for index, row in tqdm(df_books.iterrows(), total=len(df_books), desc="Création des associations"):
    book_id = book_dict.get(row['title'])
    author_id = author_dict.get(row['author_name'])
    
    # Vérifie que les deux IDs existent avant de les ajouter
    if book_id and author_id:
        associations.append({'book_id': book_id, 'author_id': author_id})
        print(f"Association ajoutée : livre ID {book_id}, auteur ID {author_id}")

# Convertir la liste `associations` en DataFrame et supprimer les doublons
df_associations = pd.DataFrame(associations).drop_duplicates()

# Enregistrer les associations dans un fichier CSV
df_associations.to_csv('book_author.csv', index=False)

# Insérer les associations dans la table SQL 'book_author'
try:
    df_associations.to_sql('book_author', con=engine, if_exists='append', index=False)
    print("Insertion des associations terminée.")
except Exception as e:
    print("Erreur lors de l'insertion des associations :")
    print(e)

# Fermer la session après insertion
session.close()
