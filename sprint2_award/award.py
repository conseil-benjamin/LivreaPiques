import pandas as pd

# Charger le fichier CSV d'origine
df = pd.read_csv("C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/books_corrected.csv")

# Sélectionner les colonnes "id" et "awards"
df_awards = df[['id', 'awards']].copy()

# Supprimer les lignes sans récompenses
df_awards.dropna(subset=['awards'], inplace=True)

# Créer une liste pour stocker les informations de récompenses
awards_data = []

# Parcourir chaque livre et ses récompenses
for _, row in df_awards.iterrows():
    book_id = row['id']
    awards = row['awards'].split(',')  # Séparer les différentes récompenses par virgule
    
    for award in awards:
        # Extraire l'année de l'award (s'il y en a une)
        award_year = pd.Series(award).str.extract(r'\((\d{4})\)')[0].values[0]
        
        # Nettoyer le texte de l'award pour supprimer l'année entre parenthèses
        award_name = pd.Series(award).str.replace(r'\s*\(\d{4}\)', '', regex=True).values[0]
        
        # Ajouter l'information à la liste sous forme de dictionnaire
        awards_data.append({
            'award_name': award_name.strip(),
            'book_id': book_id,
            'award_year': award_year
        })

# Convertir la liste en DataFrame
awards_df = pd.DataFrame(awards_data)

# Ajouter un identifiant unique pour chaque récompense
awards_df['award_id'] = awards_df.groupby('award_name').ngroup() + 1

# Réordonner les colonnes pour un affichage clair
awards_df = awards_df[['award_id', 'award_name', 'book_id', 'award_year']]

# Sauvegarder le résultat dans un nouveau fichier CSV
awards_df.to_csv("awards_books.csv")

# Afficher un aperçu du fichier généré
print(awards_df.head())
