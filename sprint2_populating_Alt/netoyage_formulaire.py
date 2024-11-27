import pandas as pd
import numpy as np
from datetime import datetime

# Charger le fichier CSV
data = pd.read_csv('../default_data/formulair.csv')

# Exclure certaines colonnes
excluded_columns = ['Horodateur', 'Quels sont vos trois genres préférés ?', 'Numéro 1', 'Numéro 2', 'Consentez vous a ce que vos données soient utilisées à des fins analytiques ?']
regex_pattern = '|'.join(excluded_columns)  # Combiner les noms de colonnes en un motif regex
data = data.loc[:, ~data.columns.str.contains(regex_pattern)]

# Renommer les colone
data = data.rename(columns={
    "Adresse e-mail": "email",
    "Date de naissance ?": "age",
    "Vous êtes ...": "gender",
    "Quelle est votre profession ?": "occupation",
    "Combien de livres lisez-vous en un an ?": "nb_book_year",
    "Parmi ce nombre, combien de livres avez-vous lu pour le plaisir en an ?": "nb_book_pleasure_year",
    "Parmi ce nombre, combien de livres avez-vous lu dans une situation professionnelle/étude en an ?": "nb_book_professional_year",
    "Parmi les modes de lecture suivants, lesquels utilisez-vous ?": "reading_mode",
    "Quelle est la provenance de vos livres papier ?": "origin_of_books",
    "Qui sont les personnes qui vous ont initié.e à la lecture ?": "initiator",
    "Quand préférez vous lire ?": "when_reading",
    "Cochez les 3 genres que vous aimez": "favorite_genre",
    "Choix 1 ?": "favorite_book_1",
    "Choix 2 ?": "favorite_book_2",
    "Choix 3 ?": "favorite_book_3",
    "Quel est votre média préféré ?": "favorite_media",
    "Qu’est-ce qui motive un choix de livre pour vous dans un cadre de loisir? (Plusieurs réponses possibles)": "makes_you_want_read"
})

# Supprimer les lignes où l'email est NaN
data = data.dropna(subset=['email']) 

# Fonction pour calculer l'âge
def calculate_age(birth_date):
    try:
        dob = datetime.strptime(birth_date, "%d/%m/%Y")  # Convertit la chaîne en objet datetime
        today = datetime.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    except Exception as e:
        return None  # Gérer les valeurs incorrectes ou manquantes

# Appliquer la fonction à la colonne "age"
data['age'] = data['age'].apply(calculate_age)

# Mapper les valeurs de la colonne 'gender'
def map_gender(value):
    if value == "Un Homme":
        return "H"
    elif value == "Une Femme":
        return "F"
    else:
        return "A"

# Appliquer la fonction à la colonne 'gender'
data['gender'] = data['gender'].apply(map_gender)

# Sauvegarder le DataFrame corrigé dans un fichier CSV
output_file = '../new_data/formulair_corrected.csv'
data.to_csv(output_file, index=False)  # `index=False` pour éviter de sauvegarder l'index en colonne

# Afficher les colonnes restantes
print(data)

