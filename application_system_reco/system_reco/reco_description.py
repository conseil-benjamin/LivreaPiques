import spacy
from gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

from SQL_controleur.SQL_controleur import requete
from tqdm import tqdm


def entrainementModele(resumes):
    print(f"le nombre de résumés pour l'entrainement est : {len(resumes)}")
    
    print(f"le nombre de résumés pour l'entrainement est : {len(resumes)}")
    # Entraîner un modèle Word2Vec avec Gensim
    w2v_model = Word2Vec(
        sentences=resumes,  # Corpus de phrases
        vector_size=100,                 # Taille des vecteurs
        window=5,                        # Contexte de mots
        min_count=1,                     # Minimum de mots à inclure
        workers=4                        # Utilisation des cœurs de processeur
    )

    # Sauvegarder le modèle Word2Vec
    w2v_model.save('word2vec.model')

    
def preTraitementResume(resumes):
    # Charger le modèle SpaCy pour l'anglais
    nlp = spacy.load("en_core_web_sm")

    # Prétraitement des textes
    def preprocess_text(text):
        # Charger le texte avec SpaCy
        try:
            doc = nlp(text)
        except:
            return []
        
        # Tokenisation, suppression des stopwords, lemmatisation
        tokens = [
            token.lemma_.lower()
            for token in doc
            if not token.is_stop and not token.is_punct and not token.is_digit
        ]

        return tokens

    # Appliquer le prétraitement
    print(f"le nombre de résumés à prétraiter est : {len(resumes)}")
    
    # resume est un df avec id, description
    # parcourir le dataframe pour prétraiter les descriptions
    new_df = pd.DataFrame()  # Initialiser une fois en dehors de la boucle

    for index, row in tqdm(resumes.iterrows(), total=resumes.shape[0], desc="Prétraitement des résumés"):
        temp_df = pd.DataFrame({
            'book_id': [row['book_id']],
            'preprocessed_resumes': [preprocess_text(row['book_description'])]
        })

        new_df = pd.concat([new_df, temp_df], ignore_index=True)  # Ajouter sans écraser
        #print(f"le nombre de résumés prétraités est : {index+1}")

    # Sauvegarder les résumés prétraités dans un fichier CSV
    csv_path = 'preprocessed_resumes.csv'
    new_df.to_csv(csv_path, index=False)

    return new_df


def get_sentence_vector(tokens, model):
    # Filtrer les mots qui existent dans le vocabulaire du modèle
    valid_tokens = [token for token in tokens if token in model.wv.key_to_index]
    if not valid_tokens:  # Si aucun mot n'est dans le vocabulaire
        return np.zeros(model.vector_size)
    # Calculer la moyenne des vecteurs des mots
    return np.mean([model.wv[token] for token in valid_tokens], axis=0)

def get_most_similar_books(resume_vectors, book_id, top_n=5):
    # Calculer la similarité cosinus entre le résumé donné et les autres résumés
    try:
        resume_vectors_id = resume_vectors[resume_vectors["book_id"] == book_id][1]
    except:
        resume_vectors_id = book_id
    list_similarity = {}
    for book_id, vector in resume_vectors:
        similarity = cosine_similarity([resume_vectors_id], [vector])[0][0]
        list_similarity[book_id] = similarity
    
    # Récupérer les top_n résumés les plus similaires
    most_similar_books = sorted(list_similarity.items(), key=lambda x: x[1], reverse=True)[:top_n]
    most_similar_books = [book_id for book_id, _ in most_similar_books]
    return most_similar_books

def reco_description(user_id, preData=True, preModel=True, vecteur=False):

    if(vecteur):
        # Charger les vecteurs des résumés
        resume_vectors = pd.read_csv('resume_vectors.csv')
    else:
        if(preData):
            # Charger les résumés prétraités
            resumes = pd.read_csv('preprocessed_resumes.csv')
        else:
            # Charger les résumés
            resumes = requete("SELECT book_id, book_description FROM book")
            print(f"le nombre de résumés est : {len(resumes)}")
            # Prétraiter les résumés
            resumes = preTraitementResume(resumes)
        
        if(preModel):
            # Charger le modèle Word2Vec
            w2v_model = Word2Vec.load('word2vec.model')
        else:
            # Entraîner un modèle Word2Vec
            entrainementModele(resumes)
            w2v_model = Word2Vec.load('word2vec.model')
        
        # Calculer les vecteurs des résumés
        resume_vectors = []
        for index, resume in resumes.iterrows():
            tokens = resume['preprocessed_resumes']
            resume_vectors.append([resume['book_id'], get_sentence_vector(tokens, w2v_model)])
        
        # Sauvegarder les vecteurs des résumés dans un fichier CSV
        csv_path = 'resume_vectors.csv'
        pd.DataFrame(resume_vectors).to_csv(csv_path, index=False)
    
    # Récupérer les résumés les plus similaires de l'utilisateur
    list_book_id = requete(f"SELECT book_id FROM liked_books WHERE user_id = {user_id}")
    mean_vector = np.mean([resume_vectors["book_id" == book_id][1] for book_id in list_book_id], axis=0)
    print(mean_vector)
    most_similar_books = get_most_similar_books(resume_vectors, mean_vector)
    return most_similar_books
    
    




def __main__():

    # demander si on utilise les données déja prétraitées ou non
    input_ = input("Voulez-vous utiliser les données prétraitées ? (O/N) : ")
    if input_ == 'O':
        # Charger les résumés prétraités
        resumes = pd.read_csv('preprocessed_resumes.csv')
        
    else:
        # Charger les résumés
        resumes = requete("SELECT book_id, book_description FROM book")
        print(f"le nombre de résumés est : {len(resumes)}")
        # Prétraiter les résumés
        resumes = preTraitementResume(resumes)
        
        print(f"le nombre de résumés prétraités est : {len(resumes)}")
    print(resumes.head())
    
    # demander si on utilise le modèle déja entrainé ou non
    input_ = input("Voulez-vous utiliser le modèle entrainé ? (O/N) : ")
    if input_ == 'O':
        # Charger le modèle Word2Vec
        w2v_model = Word2Vec.load('word2vec.model')
    else:
        # Entraîner un modèle Word2Vec
        entrainementModele(resumes)
        w2v_model = Word2Vec.load('word2vec.model')

    # Calculer les vecteurs des résumés
    resume_vectors = []
    for index, resume in resumes.iterrows():
        tokens = resume['preprocessed_resumes']
        resume_vectors.append([resume['book_id'], get_sentence_vector(tokens, w2v_model)])

    #print la taille de la matrice des vecteurs
    print(f"la taille de la matrice des vecteurs est : {len(resume_vectors)}")
    print(f"la taille de la matrice des vecteurs est : {len(resume_vectors[0][1])}")


    # Récupérer les résumés les plus similaires de l'utilisateur 32
    user_id = 32
    list_book_id = requete(f"SELECT book_id FROM liked_books WHERE user_id = {user_id}")
    print(f"les livres de l'utilisateur {user_id} sont : {list_book_id}")
    mean_vector = np.mean([resume_vectors["book_id" == book_id][1] for book_id in list_book_id], axis=0)
    print(mean_vector)
    most_similar_books = get_most_similar_books(resume_vectors, mean_vector)
    print(f"Les résumés les plus similaires à l'utilisateur {user_id} sont : {most_similar_books}")

if __name__ == "__main__":
    __main__()