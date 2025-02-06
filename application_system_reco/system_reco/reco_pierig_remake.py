import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from scipy.spatial.distance import pdist, squareform
from SQL_controleur.SQL_controleur import *
from gensim.models import Word2Vec
import numpy as np

def getData():
    # Récupérer les données des livres
    df = requete(""" SELECT book_genre.book_id, STRING_AGG(genre.genre_name, ', ') AS listegenre
            FROM book_genre
            JOIN genre ON genre.genre_id = book_genre.genre_id
            GROUP BY book_genre.book_id""")
    # transformer lisgenre en liste
    df["listegenre"] = df["listegenre"].apply(lambda x: x.split(", "))
    print("Données des livres :")
    print(df)
    return df

def train_word2vec(df, vector_size=10):
    # Entraîner un modèle Word2Vec sur la liste des genres
    model = Word2Vec(sentences=df["listegenre"], vector_size=vector_size, window=2, min_count=1, workers=4)
    return model

def embed_genres(df, model):
    def get_genre_vector(genres):
        vectors = [model.wv[g] for g in genres if g in model.wv]
        return np.mean(vectors, axis=0) if vectors else np.zeros(model.vector_size)
    
    df["genre_embedding"] = df["listegenre"].apply(get_genre_vector)
    return df


'''
def getFalseData():
    import pandas as pd
    import numpy as np

    # Définition des dimensions
    num_rows = 52000
    num_cols = 20000  # Nombre de colonnes de valeurs

    # Génération de l'identifiant unique
    book_ids = np.arange(1, num_rows + 1)

    # Génération des valeurs aléatoires (0 ou 1)
    random_values = np.random.randint(0, 2, size=(num_rows, num_cols), dtype=np.uint8)

    # Création du DataFrame
    columns = ['book_id'] + [f'valeur_{i}' for i in range(1, num_cols + 1)]
    df = pd.DataFrame(np.column_stack((book_ids, random_values)), columns=columns)

    # Affichage des premières lignes
    print(df.head())

    # Sauvegarde éventuelle
    #df.to_csv("fausses_donnees.csv", index=False)
    return df
'''

def transformeData(df):
    # Transformer la liste des genres en vecteur binaire
    mlb = MultiLabelBinarizer()
    genre_encoded = mlb.fit_transform(df["listegenre"])

    # Créer un DataFrame avec l'index des livres
    df_encoded = pd.DataFrame(genre_encoded, columns=mlb.classes_, index=df["book_id"])
    
    print("Matrice des genres (one-hot encoding) :")
    print(df_encoded)
    
    return df_encoded  # Retourne df_encoded correctement

def calculeDistance(df_encoded, book_id):
    # Calcul de la distance euclidienne entre les livres et le livre donné
    vecteur_book = df_encoded.loc[book_id]
    for book_id, vecteur in df_encoded.iterrows():
        distance = pdist([vecteur_book, vecteur], metric="euclidean")
        print(f"Distance entre le livre {book_id} et le livre {book_id} : {distance[0]}")

def main(book_id):
    df = getData()  # Récupérer les données
    model = train_word2vec(df, vector_size=50)  # Entraîner Word2Vec
    df = embed_genres(df, model)  # Créer les embeddings
    
    # Transformer la liste d'embeddings en DataFrame (pour la distance)
    df_encoded = pd.DataFrame(df["genre_embedding"].to_list(), index=df["book_id"])
    
    print(df_encoded.shape)    
    #calculeDistance(df_encoded, book_id)  # On passe df_encoded ici

if __name__ == "__main__":
    main()
