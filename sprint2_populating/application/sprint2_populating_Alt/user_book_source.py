import pandas as pd

# Charger les fichiers CSV
user_data = pd.read_csv('new_data/user.csv')
formulair_corrected_data = pd.read_csv('new_data/formulair_corrected.csv')
origin_of_books_data = pd.read_csv('new_data/book_source.csv')

# Étape 1: Sélectionner les ID des utilisateurs dans 'user.csv'
user_ids = user_data[['id']]  # Supposons que 'id' est la colonne des utilisateurs

# Étape 2: Sélectionner la colonne 'origin_of_books' dans 'formulair_corrected.csv'
origin_of_books = formulair_corrected_data[['id', 'origin_of_books']]  # Associe les ID des utilisateurs aux origines des livres

# Étape 3: Sélectionner la colonne 'origin_id' et 'origin_of_books' dans 'book_source.csv'
origin_of_books_mapping = origin_of_books_data[['origin_id', 'origin_of_books']]  # La colonne contenant l'origine des livres

# Étape 4: Séparer les origines de livres multiples (s'il y en a plusieurs dans une cellule)
origin_of_books_split = origin_of_books.copy()
origin_of_books_split['origin_of_books'] = origin_of_books_split['origin_of_books'].str.split(',')

# Déployer la liste dans des lignes distinctes
origin_of_books_split = origin_of_books_split.explode('origin_of_books').reset_index(drop=True)

# Étape 5: Nettoyer les espaces blancs autour des noms des origines
origin_of_books_split['origin_of_books'] = origin_of_books_split['origin_of_books'].str.strip()

# Étape 6: Fusionner les données pour créer une table d'association
# Fusionner avec 'origin_of_books_mapping' pour obtenir l'id d'origine
association_table = pd.merge(origin_of_books_split, origin_of_books_mapping, on='origin_of_books', how='left')

# Fusionner ensuite avec les ID des utilisateurs
association_table = pd.merge(association_table, user_ids, on='id', how='left')

# Étape 7: Forcer la conversion de 'origin_id' en entier (en supprimant les décimales)
association_table['origin_id'] = association_table['origin_id'].astype('Int64')  # Utiliser 'Int64' pour gérer les valeurs manquantes

# Supprimer la colonne 'origin_of_books' maintenant qu'elle n'est plus nécessaire
association_table = association_table.drop(columns=['origin_of_books'])

# Afficher l'association pour vérifier le résultat
print("\nAssociation table preview (after removing 'origin_of_books'):")
print(association_table.head())

# Sauvegarder la table d'association dans un fichier CSV
output_file = 'new_data/Associations_user_origin.csv'
association_table.to_csv(output_file, index=False)