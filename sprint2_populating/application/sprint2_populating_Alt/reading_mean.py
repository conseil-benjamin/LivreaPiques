import pandas as pd
import re

# Charger le fichier CSV avec gestion des erreurs et du séparateur
file_path = 'C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/formulair_corrected.csv'

# Essayer de charger le fichier CSV en utilisant un séparateur personnalisé (par défaut la virgule)
try:
    data = pd.read_csv(file_path, delimiter=',', quotechar='"', encoding='utf-8')
except pd.errors.ParserError as e:
    raise ValueError(f"Erreur lors de la lecture du fichier CSV : {e}")

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
    if isinstance(text, str):  # S'assurer que l'entrée est une chaîne de caractères
        # Remplacer temporairement les virgules à l'intérieur des parenthèses par un autre caractère unique
        temp_text = re.sub(r'\([^)]*\)', lambda match: match.group(0).replace(',', '###TEMP###'), text)
        
        # Maintenant, séparer par les virgules, en ignorant les virgules temporaires
        parts = temp_text.split(', ')
        
        # Rétablir les virgules temporaires dans chaque partie entre parenthèses
        parts = [part.replace('###TEMP###', ',') for part in parts]
        
        return parts
    else:
        return []

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

# Définir le chemin de sortie
output_file = 'C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/reading_mean.csv'

# Sauvegarder dans un nouveau fichier CSV en gérant les caractères spéciaux et en désactivant les guillemets
expanded_data.to_csv(output_file, index=False, header=True, quoting=3, escapechar='\\')