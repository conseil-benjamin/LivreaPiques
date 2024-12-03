import pandas as pd
import re

# Charger le fichier CSV
data = pd.read_csv('C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/formulair_corrected.csv')

# Sélectionner et réorganiser les colonnes souhaitées
columns_to_keep = ['reading_mean']

# Vérifier si toutes les colonnes existent dans le fichier source
missing_columns = [col for col in columns_to_keep if col not in data.columns]
if missing_columns:
    raise ValueError(f"Colonnes manquantes dans le fichier CSV : {missing_columns}")

# Filtrer les colonnes
filtered_data = data[columns_to_keep]

# Fonction pour gérer la séparation des éléments en ignorant les virgules dans les parenthèses
def split_without_parentheses(text):
    # Remplacer temporairement les virgules à l'intérieur des parenthèses par un autre caractère unique
    temp_text = re.sub(r'\([^)]*\)', lambda match: match.group(0).replace(',', '###TEMP###'), text)
    
    # Maintenant, séparer par les virgules, en ignorant les virgules temporaires
    parts = temp_text.split(', ')
    
    # Rétablir les virgules temporaires dans chaque partie entre parenthèses
    parts = [part.replace('###TEMP###', ',') for part in parts]
    
    return parts

# Séparer les valeurs en plusieurs lignes, en utilisant la fonction personnalisée
expanded_data = filtered_data.assign(
    reading_mean=filtered_data['reading_mean'].apply(split_without_parentheses)
).explode('reading_mean')

# Supprimer les doublons et les valeurs manquantes
expanded_data = expanded_data.drop_duplicates().dropna()

# Supprimer les guillemets autour des valeurs (si présents)
expanded_data['reading_mean'] = expanded_data['reading_mean'].str.replace('"', '', regex=False)

# Générer un ID incrémental
expanded_data['reading_mean_id'] = range(1, len(expanded_data) + 1)

# Enregistrer dans un nouveau fichier CSV sans guillemets, en ajoutant un caractère d'échappement
output_file = 'C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/reading_mean.csv'
expanded_data.to_csv(output_file, index=False, header=True, quoting=3, escapechar='\\')  # `escapechar='\\'` pour gérer les caractères spéciaux