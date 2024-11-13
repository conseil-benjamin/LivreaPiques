import pandas as pd
from sqlalchemy import create_engine, exc

# URL de la base de données Supabase
database_url = 'postgresql://postgres.pczyoeavtwijgtkzgcaz:D0jVgaoGmDAFuaMS@aws-0-eu-west-3.pooler.supabase.com:6543/postgres'


# Création de la table `author` dans la base de données

# Créer une connexion avec la base de données
engine = create_engine(database_url)

# Charger le CSV dans un DataFrame
csv_file_path = '../new_data/CleanedAuthors.csv'
df = pd.read_csv(csv_file_path)

# Sélectionner uniquement les colonnes nécessaires
df = df[["author_name", "author_gender", "birthplace"]]

# Renommer les colonnes pour correspondre aux noms de la base de données
df = df.rename(columns={
    "author_name": "name_author"
})

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


# Création de la table association `book_author` dans la base de données

from sqlalchemy import create_engine, select, Table, MetaData
from sqlalchemy.orm import sessionmaker

# Connexion à la base de données
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

# Créer l'objet MetaData sans `bind`
metadata = MetaData()

# Charger le CSV des livres
csv_book = '../new_data/books_corrected.csv'
df_books = pd.read_csv(csv_book)
df_books = df_books[["title", "author"]]
df_books = df_books.rename(columns={
    "author": "name_author"
})

# Charger les tables book et author en utilisant `autoload_with=engine`
book_table = Table('book', metadata, autoload_with=engine)
author_table = Table('author', metadata, autoload_with=engine)

# Fonction pour obtenir les IDs selon le titre ou le nom
def get_id_by_name(table, name_column, name_value, search_column='id'):
    result = session.execute(select(table.c[search_column]).where(table.c[name_column] == name_value)).first()
    return result[0] if result else None

# Parcourir le DataFrame pour créer les associations
associations = []
for index, row in df_books.iterrows():
    book_id = get_id_by_name(book_table, 'title', row['title'], search_column='id_book')
    author_id = get_id_by_name(author_table, 'name_author', row['name_author'], search_column='id_author')
    
    # Vérifie que les deux IDs existent avant de les ajouter à `associations`
    if book_id and author_id:
        associations.append({'id_book': book_id, 'id_author': author_id})
        print(f"Association ajoutée : livre ID {book_id}, auteur ID {author_id}")

# Convertir la liste `associations` en DataFrame
df_associations = pd.DataFrame(associations)

# Supprimer les doublons de paires (id_book, id_author)
df_associations = df_associations.drop_duplicates()

# Enregistrer les associations dans un fichier CSV
df_associations.to_csv('book_author.csv', index=False)

# Insérer les associations dans la table SQL 'book_author'
try:
    df_associations.to_sql('book_author', con=engine, if_exists='append', index=False)
    print("Insertion des associations terminée.")
except Exception as e:
    print("Erreur lors de l'insertion des associations :")
    print(e)

# Ferme la session après insertion
session.close()