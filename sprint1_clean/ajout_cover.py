import pandas as pd

books_with_cover = pd.read_csv("../default_data/books_with_cover.csv")
books_corrected = pd.read_csv("../new_data/books_corrected.csv")

if 'cover_link' not in books_with_cover.columns:
    raise ValueError("La colonne 'cover_link' est absente du fichier books_with_cover.csv")

common_key = 'id'
if common_key not in books_with_cover.columns or common_key not in books_corrected.columns:
    raise ValueError(f"La clé commune '{common_key}' est absente d'un des fichiers")

books_merged = books_corrected.merge(books_with_cover[[common_key, 'cover_link']], on=common_key, how='left')

books_merged.to_csv("new_data/books_corrected.csv", index=False)

print("Mise à jour terminée : 'cover_link' a été ajouté à books_corrected.csv")