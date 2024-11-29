import pandas as pd

# Charger le fichier CSV
data = pd.read_csv('../new_data/formulair_corrected.csv')

# Ajouter un username basé sur l'email
data['username'] = data['email'].apply(lambda x: x.split('@')[0] if '@' in str(x) else x)

# Générer un ID incrémental
data['id'] = range(1, len(data) + 1)

# Ajouter un mot de passe par défaut
data['password'] = 'mdp'

# Sélectionner et réorganiser les colonnes souhaitées
columns_to_keep = [
    'id', 'username', 'password', 
    'gender', 'nb_book_year', 'nb_book_pleasure_year', 
    'nb_book_professional_year', 'initiator', 
    'when_reading', 'makes_you_want_read'
]

# Vérifier si toutes les colonnes existent dans le fichier source
missing_columns = [col for col in columns_to_keep if col not in data.columns]
if missing_columns:
    raise ValueError(f"Colonnes manquantes dans le fichier CSV : {missing_columns}")

# Filtrer les colonnes
final_data = data[columns_to_keep]

# Enregistrer dans un nouveau fichier CSV
output_file = '../new_data/user.csv'
final_data.to_csv(output_file, index=False)