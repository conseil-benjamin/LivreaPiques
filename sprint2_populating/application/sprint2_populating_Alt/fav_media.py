import pandas as pd

# Charger les fichiers CSV
user_data = pd.read_csv('new_data/user.csv')
formulair_corrected_data = pd.read_csv('new_data/formulair_corrected.csv')
favorite_media_data = pd.read_csv('new_data/media.csv')

# Étape 1: Sélectionner les ID des utilisateurs dans 'user.csv'
user_ids = user_data[['id']]  # Supposons que 'id' est la colonne des utilisateurs

# Étape 2: Sélectionner la colonne 'favorite_media' dans 'formulair_corrected.csv'
favorite_media = formulair_corrected_data[['id', 'favorite_media']]  # Associe les ID des utilisateurs aux origines des livres

# Étape 3: Sélectionner la colonne 'media_id' et 'favorite_media' dans 'book_source.csv'
favorite_media_mapping = favorite_media_data[['media_id', 'favorite_media']]  # La colonne contenant l'origine des livres

# Étape 4: Séparer les origines de livres multiples (s'il y en a plusieurs dans une cellule)
favorite_media_split = favorite_media.copy()
favorite_media_split['favorite_media'] = favorite_media_split['favorite_media'].str.split(',')

# Déployer la liste dans des lignes distinctes
favorite_media_split = favorite_media_split.explode('favorite_media').reset_index(drop=True)

# Étape 5: Nettoyer les espaces blancs autour des noms des origines
favorite_media_split['favorite_media'] = favorite_media_split['favorite_media'].str.strip()

# Étape 6: Fusionner les données pour créer une table d'association
# Fusionner avec 'favorite_media_mapping' pour obtenir l'id d'origine
association_table = pd.merge(favorite_media_split, favorite_media_mapping, on='favorite_media', how='left')

# Fusionner ensuite avec les ID des utilisateurs
association_table = pd.merge(association_table, user_ids, on='id', how='left')

# Étape 7: Forcer la conversion de 'media_id' en entier (en supprimant les décimales)
association_table['media_id'] = association_table['media_id'].astype('Int64')  # Utiliser 'Int64' pour gérer les valeurs manquantes

# Supprimer les lignes où 'media_id' est manquant
association_table = association_table.dropna(subset=['media_id'])

# Supprimer la colonne 'favorite_media' maintenant qu'elle n'est plus nécessaire
association_table = association_table.drop(columns=['favorite_media'])

# Afficher l'association pour vérifier le résultat
print("\nAssociation table preview (after removing rows with missing 'media_id'):")
print(association_table.head())

# Sauvegarder la table d'association dans un fichier CSV
output_file = 'new_data/Associations_media.csv'
association_table.to_csv(output_file, index=False)