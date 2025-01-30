import spacy
from gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

import sys
sys.path.append('../sprint2_populating/application/')

from SQL_controleur.SQL_controleur import requete

def entrainementModele(resumes):

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
        doc = nlp(text)
        
        # Tokenisation, suppression des stopwords, lemmatisation
        tokens = [
            token.lemma_.lower()
            for token in doc
            if not token.is_stop and not token.is_punct and not token.is_digit
        ]

        return tokens

    # Appliquer le prétraitement
    preprocessed_resumes = [preprocess_text(resume) for resume in resumes]
    return preprocessed_resumes

    # Convertir les résumés prétraités en DataFrame
    df = pd.DataFrame({'preprocessed_resumes': [' '.join(tokens) for tokens in preprocessed_resumes]})

    # Sauvegarder les résumés prétraités dans un fichier CSV
    csv_path = 'preprocessed_resumes.csv'
    df.to_csv(csv_path, index=False)


def get_sentence_vector(tokens, model):
    # Filtrer les mots qui existent dans le vocabulaire du modèle
    valid_tokens = [token for token in tokens if token in model.wv.key_to_index]
    if not valid_tokens:  # Si aucun mot n'est dans le vocabulaire
        return np.zeros(model.vector_size)
    # Calculer la moyenne des vecteurs des mots
    return np.mean([model.wv[token] for token in valid_tokens], axis=0)


def __main__():

    # demander si on utilise les données déja prétraitées ou non
    input_ = input("Voulez-vous utiliser les données prétraitées ? (O/N) : ")
    if input_ == 'O':
        # Charger les résumés prétraités
        df = pd.read_csv('preprocessed_resumes.csv')
        resumes = df['preprocessed_resumes'].apply(str.split).tolist()
    else:
        # Charger les résumés
        resumes = requete("SELECT book_id, book_description FROM book")
        # Prétraiter les résumés
        resumes = preTraitementResume(resumes)
    
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
    resume_vectors = np.array([get_sentence_vector(tokens, w2v_model) for tokens in resumes])
    print(resume_vectors)