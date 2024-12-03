import pandas as pd

# Charger le fichier CSV
data = pd.read_csv('C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/formulair_corrected.csv')

# Vérifier si la colonne "origin_of_books" existe dans le fichier source
if 'origin_of_books' not in data.columns:
    raise ValueError("La colonne 'origin_of_books' est manquante dans le fichier CSV.")

# Supprimer les lignes où "origin_of_books" est manquant ou vide
data = data.dropna(subset=['origin_of_books'])
data = data[data['origin_of_books'].str.strip() != ""]

# Extraire les origines uniques en séparant les valeurs par des virgules
origins = data['origin_of_books'].str.split(', ').explode().drop_duplicates()

# Supprimer les valeurs vides (après séparation)
origins = origins[origins.str.strip() != ""]

# Créer un DataFrame avec les origines et des IDs incrémentaux
unique_origins = pd.DataFrame({
    'origin_id': range(1, len(origins) + 1),
    'origin_of_books': origins.values
})

# Enregistrer dans un nouveau fichier CSV
output_file = 'C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/book_source.csv'
unique_origins.to_csv(output_file, index=False)