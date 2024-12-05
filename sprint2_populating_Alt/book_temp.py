import pandas as pd

# Charger les fichiers CSV
formulair_corrected = pd.read_csv('C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/formulair_corrected.csv')
books_corrected = pd.read_csv('C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/books_corrected.csv')

# Extraire les livres de formulair_corrected
books_from_formulair = pd.melt(formulair_corrected, 
                               value_vars=['favorite_book_1', 'favorite_book_2', 'favorite_book_3'], 
                               var_name='favorite_book_column', 
                               value_name='title')

# Supprimer les lignes vides
books_from_formulair = books_from_formulair.dropna(subset=['title'])

# Ajouter une colonne pour indiquer la source
books_from_formulair['source'] = 'formulair_corrected'

# Préparer les données de books_corrected
books_from_books = books_corrected[['title']].copy()
books_from_books['source'] = 'books_corrected'

# Combiner les deux DataFrames
combined_books = pd.concat([books_from_books, books_from_formulair[['title', 'source']]], ignore_index=True)

# Sauvegarder le résultat dans un nouveau fichier CSV (facultatif)
combined_books.to_csv('C:/Users/utilisateur/Documents/Perso/SAE/LivreaPiques/new_data/combined_books.csv', index=False)

print(combined_books.head())
