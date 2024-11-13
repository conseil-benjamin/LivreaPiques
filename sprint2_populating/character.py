import pandas as pd
from sqlalchemy import create_engine, select, Table, MetaData
from sqlalchemy.orm import sessionmaker

# Charger les données et enlever les colonnes 'Unnamed'
data = pd.read_csv('../new_data/books_corrected.csv')
data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

# Garder uniquement les colonnes 'title' et 'characters'
data = data[['title', 'characters']]

# Enlever les lignes avec des valeurs manquantes
data = data.dropna()

# Afficher les premières lignes pour vérification
print(data.head())

# Connexion à la base de données
database_url = 'postgresql://postgres.pczyoeavtwijgtkzgcaz:D0jVgaoGmDAFuaMS@aws-0-eu-west-3.pooler.supabase.com:6543/postgres'
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

# Créer l'objet MetaData
metadata = MetaData()

# Charger les tables book et awards en utilisant `autoload_with=engine`
book_table = Table('book', metadata, autoload_with=engine)
characters_table = Table('characters', metadata, autoload_with=engine)

# Requête pour obtenir les IDs de livres et de personnages selon leurs noms
def get_id_by_name(table, name_column, name_value, search_column='id'):
    result = session.execute(select(table.c[search_column]).where(table.c[name_column] == name_value)).first()
    return result[0] if result else None

# Parcours du DataFrame pour récupérer les IDs et afficher un message après chaque insertion dans `associations`
associations = []
for index, row in data.iterrows():
    book_id = get_id_by_name(book_table, 'title', row['title'], search_column='id_book')
    character_id = get_id_by_name(characters_table, 'name', row['characters'], search_column='id_character')
    
    # Vérifie que les deux IDs existent avant de les insérer
    if book_id and character_id:
        associations.append({'id_book': book_id, 'id_character': character_id})
        print(f"Association ajoutée : livre ID {book_id}, personnage ID {character_id}")

# Sauvegarder les associations dans un fichier CSV
df_associations = pd.DataFrame(associations)
df_associations.to_csv('associations_character.csv', index=False)

# Charger les associations depuis le fichier CSV
associations = pd.read_csv('associations_character.csv')

# Enlever les doublons
associations = associations.drop_duplicates()

# Insérer les associations dans la table SQL 'book_characters'
associations.to_sql('book_characters', con=engine, if_exists='append', index=False)

# Ferme la session après insertion
session.close()
print("Insertion des données terminée.")
