import pandas as pd

# Charger le fichier CSV
data = pd.read_csv('C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/formulair_corrected.csv')

# Sélectionner et réorganiser les colonnes souhaitées
columns_to_keep = ['favorite_media']

# Vérifier si toutes les colonnes existent dans le fichier source
missing_columns = [col for col in columns_to_keep if col not in data.columns]
if missing_columns:
    raise ValueError(f"Colonnes manquantes dans le fichier CSV : {missing_columns}")

# Filtrer les colonnes
filtered_data = data[columns_to_keep]

# Séparer les médias en plusieurs lignes
expanded_data = filtered_data.assign(
    favorite_media=filtered_data['favorite_media'].str.split(', ')
).explode('favorite_media')

# Remplacer "Webtoons" par "Webtoon" et "Manwha" par "Manhwa"
expanded_data['favorite_media'] = expanded_data['favorite_media'].str.replace('Webtoons', 'Webtoon', case=False)
expanded_data['favorite_media'] = expanded_data['favorite_media'].str.replace('Manwha', 'Manhwa', case=False)

# Nettoyer pour garder uniquement le premier mot "Webtoons" ou "Manhwa"
expanded_data['favorite_media'] = expanded_data['favorite_media'].apply(
    lambda x: 'Webtoon' if 'Webtoon' in x else ('Manhwa' if 'Manhwa' in x else x)
)

# Supprimer les doublons, les valeurs manquantes, et les médias vides
expanded_data = expanded_data.drop_duplicates().dropna(subset=['favorite_media'])
expanded_data = expanded_data[expanded_data['favorite_media'].str.strip() != ""]

# Générer un ID incrémental
expanded_data['media_id'] = range(1, len(expanded_data) + 1)

# Enregistrer dans un nouveau fichier CSV
output_file = 'C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/media.csv'
expanded_data.to_csv(output_file, index=False)

print(f"Fichier CSV avec médias uniques et IDs enregistré : {output_file}")
