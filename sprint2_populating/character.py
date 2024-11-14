import pandas as pd
from sqlalchemy import create_engine, select, Table, MetaData
from sqlalchemy.orm import sessionmaker

# Charger les données et enlever les colonnes 'Unnamed'
data = pd.read_csv('new_data/books_corrected.csv')
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# Garder uniquement les colonnes 'title' et 'characters'
data = data[['title', 'characters']]

# Enlever les lignes avec des valeurs manquantes
data = data.dropna()

# Afficher les premières lignes pour vérification

data2 = data[['characters']]

# separer les noms de personnages (s'ils sont plusieurs) en utilisant la virgule
data2 = data2['characters'].str.split(',', expand=True)

# empiler les colonnes pour avoir une seule colonne
data2 = data2.stack()

# supprimer les lignes avec des valeurs manquantes
data2 = data2.dropna()

# supprimer les espaces en trop
data2 = data2.str.strip()


data2 = data2.drop_duplicates()

# retransformer en DataFrame
data2 = data2.to_frame()

# réinitialiser l'index
data2 = data2.reset_index(drop=True)

print(data2.head())

# nommer la colonne
data2.columns = ['character_name']

# conaitre le plus long nom de personnage
max_length = data2['character_name'].str.len().max()
print(f"Le nom de personnage le plus long a {max_length} caractères.")


## URL de la base de données Supabase
database_url = 'postgresql://postgres.pczyoeavtwijgtkzgcaz:D0jVgaoGmDAFuaMS@aws-0-eu-west-3.pooler.supabase.com:6543/postgres'

## Créer une connexion avec la base de données
engine = create_engine(database_url)

## Insérer les données dans la table SQL 'author'
data2.to_sql('characters', con=engine, if_exists='append', index=False)

print("Insertion des données terminée.")

# close the connection
engine.dispose()



#########################################
#renommer la colonne 'title' en 'book_title'
data = data.rename(columns={'title': 'book_title'})

print(data.head())
df = pd.DataFrame(data)

# Séparer les personnages et garder l'info du titre pour chaque personnage
df_exploded = df.assign(characters=df['characters'].str.split(', ')).explode('characters').reset_index(drop=True)

print(df_exploded)

# stoper le programme pour vérifier les données
input("Appuyez sur Entrée pour continuer...")
#########################################
from tqdm import tqdm

# Connexion à la base de données
database_url = 'postgresql://postgres.pczyoeavtwijgtkzgcaz:D0jVgaoGmDAFuaMS@aws-0-eu-west-3.pooler.supabase.com:6543/postgres'
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

# Créer l'objet MetaData
metadata = MetaData()

# Charger les tables book et characters en utilisant `autoload_with=engine`
book_table = Table('book', metadata, autoload_with=engine)
characters_table = Table('characters', metadata, autoload_with=engine)

# Récupérer tous les IDs de livres et de personnages en une seule requête pour chaque table
book_records = session.execute(select(book_table.c.book_id, book_table.c.book_title)).all()
character_records = session.execute(select(characters_table.c.character_id, characters_table.c.character_name)).all()

# Créer des dictionnaires pour une recherche rapide des IDs
book_dict = {title: book_id for book_id, title in book_records}
character_dict = {name: character_id for character_id, name in character_records}

# Parcourir `data` et créer les associations en utilisant les dictionnaires, avec une barre de progression
associations = []
for index, row in tqdm(data.iterrows(), total=len(data), desc="Création des associations"):
    book_id = book_dict.get(row['book_title'])
    character_id = character_dict.get(row['characters'])
    
    # Vérifie que les deux IDs existent avant de les ajouter
    if book_id and character_id:
        associations.append({'book_id': book_id, 'character_id': character_id})
        print(f"Association ajoutée : livre ID {book_id}, personnage ID {character_id}")

# Convertir les associations en DataFrame et supprimer les doublons
df_associations = pd.DataFrame(associations).drop_duplicates()

# Enregistrer les associations dans un fichier CSV
df_associations.to_csv('associations_character.csv', index=False)

# Insérer les associations dans la table SQL 'book_characters'
try:
    df_associations.to_sql('book_characters', con=engine, if_exists='append', index=False)
    print("Insertion des associations terminée.")
except Exception as e:
    print("Erreur lors de l'insertion des associations :")
    print(e)

# Fermer la session après insertion
session.close()

