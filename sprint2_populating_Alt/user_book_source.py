import pandas as pd

# Charger les fichiers CSV
data1 = pd.read_csv('C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/user.csv')
data2 = pd.read_csv('C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/book_source.csv')

# Afficher les premiers enregistrements pour inspection (optionnel)
print("Users data preview:")
print(data1.head())
print("\nBook sources data preview:")
print(data2.head())

# Sélectionner les colonnes pertinentes
user_ids = data1[['id']]  # Sélectionner la colonne 'id' de data1
origin_ids = data2[['origin_id']]  # Sélectionner la colonne 'origin_id' de data2

# Créer une table d'association entre chaque utilisateur et chaque origin_id
association_table = pd.merge(user_ids, origin_ids, how='cross')

# Sauvegarder la table d'association dans un fichier CSV
output_file = 'C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/Associations_book_source.csv'
association_table.to_csv(output_file, index=False)
