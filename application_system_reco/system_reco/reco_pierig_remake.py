import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from scipy.spatial.distance import pdist, squareform
from SQL_controleur.SQL_controleur import *
from gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity



def getData():
    # Récupérer les données des livres
    df = requete(""" SELECT
                b.book_id,
                b.nb_of_pages,
                b.review_count,
                genre_list.listegenre,
                CASE
                    WHEN award_count.award_count > 0 THEN 1
                    ELSE 0
                END AS award
            FROM
                book b
            JOIN
                (SELECT
                    bg.book_id,
                    COALESCE(STRING_AGG(g.genre_name, ', ')) AS listegenre
                FROM
                    book_genre bg
                JOIN
                    genre g ON g.genre_id = bg.genre_id
                GROUP BY
                    bg.book_id) AS genre_list ON b.book_id = genre_list.book_id
            LEFT JOIN
                (SELECT
                    ba.book_id,
                    COUNT(ba.award_id) AS award_count
                FROM
                    book_awards ba
                GROUP BY
                    ba.book_id) AS award_count ON b.book_id = award_count.book_id
        """)
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

def calculeDistance(df_encoded, book_id, top_n=5):
    # Calculer la similarité cosinus entre le résumé donné et les autres résumés
    try:
        df_encoded_id = df_encoded[df_encoded["book_id"] == book_id]["vector"].values[0]
    except:
        df_encoded_id = book_id
    list_similarity = {}
    erreur = 0
    for index, row in df_encoded.iterrows():
        book_id = row['book_id']
        vector = row['vector']
        try:
            similarity = cosine_similarity([df_encoded_id], [vector])[0][0]
        except:
            erreur += 1
            similarity = 1000000
        list_similarity[book_id] = similarity
    print(f"il y a eu {erreur} erreurs")
    
    # Récupérer les top_n résumés les plus similaires
    most_similar_books = sorted(list_similarity.items(), key=lambda x: x[1], reverse=True)[:top_n]
    most_similar_books = [book_id for book_id, _ in most_similar_books]
    return most_similar_books

def main(user_id):
    df = getData()
    model = train_word2vec(df, vector_size=50)
    df = embed_genres(df, model)
    
    # Convertir la liste d'embeddings en colonnes séparées
    embeddings_df = pd.DataFrame(df["genre_embedding"].to_list(), index=df["book_id"])
    
    # Conserver toutes les colonnes originales sauf 'listegenre' (inutile après encodage)
    df_encoded = df.drop(columns=["listegenre", "genre_embedding"]).set_index("book_id").join(embeddings_df)
    print(df_encoded.shape)
    print(df_encoded.head())
    # normaliser les données
    df_encoded = (df_encoded - df_encoded.mean()) / df_encoded.std()

    df_encoded = df_encoded.reset_index()
    # Créer la colonne 'vector' avec les 53 autres colonnes sous forme de liste
    df_encoded['vector'] = df_encoded.drop(columns=['book_id']).values.tolist()

    # Maintenant, tu peux ne garder que les colonnes 'book_id' et 'vector'
    df_encoded = df_encoded[['book_id', 'vector']]

    
    print(df_encoded.columns)
    print(df_encoded.shape)
    print(df_encoded.head())
    

    # Récupérer les résumés les plus similaires de l'utilisateur
    list_book_id = requete(f"SELECT book_id FROM liked_books WHERE user_id = {user_id}")
    print(f"les livres de l'utilisateur {user_id} sont : {list_book_id}")
    # transformer en liste le dataframe
    list_book_id = list_book_id.values.flatten().tolist()
    vectors = [np.array(df_encoded[df_encoded["book_id"] == book_id]["vector"].values[0])
               for book_id in list_book_id if not df_encoded[df_encoded["book_id"] == book_id]["vector"].empty]
    if(len(vectors) == 0):
        print("Aucun livre avec des genre n'a été trouvé")
        return []
    mean_vector = np.mean(vectors, axis=0)
    print(mean_vector)

    # Récupérer les résumés les plus similaires
    most_similar_books = calculeDistance(df_encoded, mean_vector)
    print(f"les livres les plus similaires sont : {most_similar_books}")

    # requete pour avoir les titres des livres
    most_similar_books = requete(f"SELECT book_title FROM book WHERE book_id IN {tuple(most_similar_books)}")

    return most_similar_books

if __name__ == "__main__":
    main(1)

