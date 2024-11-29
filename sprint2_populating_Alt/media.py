import pandas as pd

# Charger le fichier CSV
data = pd.read_csv('C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/formulair_corrected.csv')

# Sélectionner et réorganiser les colonnes souhaitées
columns_to_keep = [
    'id', 'favorite_media'
]

# Vérifier si toutes les colonnes existent dans le fichier source
missing_columns = [col for col in columns_to_keep if col not in data.columns]
if missing_columns:
    raise ValueError(f"Colonnes manquantes dans le fichier CSV : {missing_columns}")

# Filtrer les colonnes
filtered_data = data[columns_to_keep]

# Renommer 'id' en 'id_user'
filtered_data.rename(columns={'id': 'id_user'}, inplace=True)

# Séparer les médias en plusieurs lignes
expanded_data = filtered_data.assign(
    favorite_media=filtered_data['favorite_media'].str.split(', ')
).explode('favorite_media')

# Enregistrer dans un nouveau fichier CSV
output_file = 'C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/media_with_ids.csv'
expanded_data.to_csv(output_file, index=False)