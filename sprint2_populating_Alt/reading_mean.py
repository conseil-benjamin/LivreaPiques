import pandas as pd

# Charger le fichier CSV
data = pd.read_csv('C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/formulair_corrected.csv')

# Sélectionner et réorganiser les colonnes souhaitées
columns_to_keep = [
    'reading_mean'
]

# Vérifier si toutes les colonnes existent dans le fichier source
missing_columns = [col for col in columns_to_keep if col not in data.columns]
if missing_columns:
    raise ValueError(f"Colonnes manquantes dans le fichier CSV : {missing_columns}")

# Filtrer les colonnes
filtered_data = data[columns_to_keep]

# Séparer les valeurs en plusieurs lignes
expanded_data = filtered_data.assign(
    reading_mean=filtered_data['reading_mean'].str.split(', ')
).explode('reading_mean')

# Supprimer les doublons et les valeurs manquantes
expanded_data = expanded_data.drop_duplicates().dropna()

# Générer un ID incrémental
expanded_data['mean_id'] = range(1, len(expanded_data) + 1)

# Enregistrer dans un nouveau fichier CSV
output_file = 'C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/reading_mean.csv'
expanded_data.to_csv(output_file, index=False)
