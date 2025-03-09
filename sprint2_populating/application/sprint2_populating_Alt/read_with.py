import pandas as pd

# Charger les fichiers CSV
user_data = pd.read_csv('new_data/user.csv')
formulair_corrected_data = pd.read_csv('new_data/formulair_corrected.csv')
reading_mean_data = pd.read_csv('new_data/reading_mean.csv')

# Étape 1: Sélectionner les ID des utilisateurs dans 'user.csv'
user_ids = user_data[['id']]  # Supposons que 'id' est la colonne des utilisateurs

# Étape 2: Sélectionner la colonne 'reading_mean' dans 'formulair_corrected.csv'
reading_mean = formulair_corrected_data[['id', 'reading_mean']]  # Associe les ID des utilisateurs aux origines des livres

# Étape 3: Sélectionner la colonne 'reading_mean_id' et 'reading_mean' dans 'book_source.csv'
reading_mean_mapping = reading_mean_data[['reading_mean_id', 'reading_mean']]  # La colonne contenant l'origine des livres

# Étape 4: Séparer les origines de livres multiples (s'il y en a plusieurs dans une cellule)
reading_mean_split = reading_mean.copy()
reading_mean_split['reading_mean'] = reading_mean_split['reading_mean'].str.split(',')

# Déployer la liste dans des lignes distinctes
reading_mean_split = reading_mean_split.explode('reading_mean').reset_index(drop=True)

# Étape 5: Nettoyer les espaces blancs autour des noms des origines
reading_mean_split['reading_mean'] = reading_mean_split['reading_mean'].str.strip()

# Étape 6: Fusionner les données pour créer une table d'association
# Fusionner avec 'reading_mean_mapping' pour obtenir l'id d'origine
association_table = pd.merge(reading_mean_split, reading_mean_mapping, on='reading_mean', how='left')

# Fusionner ensuite avec les ID des utilisateurs
association_table = pd.merge(association_table, user_ids, on='id', how='left')

# Étape 7: Forcer la conversion de 'reading_mean_id' en entier (en supprimant les décimales)
association_table['reading_mean_id'] = association_table['reading_mean_id'].astype('Int64')  # Utiliser 'Int64' pour gérer les valeurs manquantes

# Supprimer les lignes où 'reading_mean_id' est manquant
association_table = association_table.dropna(subset=['reading_mean_id'])

# Supprimer la colonne 'reading_mean' maintenant qu'elle n'est plus nécessaire
association_table = association_table.drop(columns=['reading_mean'])

# Afficher l'association pour vérifier le résultat
print("\nAssociation table preview (after removing rows with missing 'reading_mean_id'):")
print(association_table.head())

# Sauvegarder la table d'association dans un fichier CSV
output_file = 'new_data/Associations_mean.csv'
association_table.to_csv(output_file, index=False)
