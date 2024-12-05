import pandas as pd

# Charger le fichier CSV
data = pd.read_csv('C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/formulair_corrected.csv')

# Sélectionner et réorganiser les colonnes souhaitées
columns_to_keep = ['id', 'favorite_book_1', 'favorite_book_2', 'favorite_book_3']
filtered_data = data[columns_to_keep]

# Renommer 'id' en 'id_user'
filtered_data.rename(columns={'id': 'id_user'}, inplace=True)

# Transformer les colonnes des livres en une seule colonne
melted_data = filtered_data.melt(id_vars=['id_user'], 
                                 value_vars=['favorite_book_1', 'favorite_book_2', 'favorite_book_3'], 
                                 var_name='rank', 
                                 value_name='id')

# Remplacer les valeurs dans la colonne 'rank'
melted_data['rank'] = melted_data['rank'].replace({
    'favorite_book_1': 1,
    'favorite_book_2': 2,
    'favorite_book_3': 3
})

# Supprimer les lignes où la colonne 'id' est vide (NaN)
melted_data.dropna(subset=['id'], inplace=True)

# Enregistrer dans un nouveau fichier CSV
output_file = 'C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/book_fav.csv'
melted_data.to_csv(output_file, index=False)
