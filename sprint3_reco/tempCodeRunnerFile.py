import spacy
from gensim.models import Word2Vec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import SQL_controleur

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

SQL_controleur = SQL_controleur.SQL_controleur()


# Exemple de résumés
resumes = [
    "This is a story of a young boy who discovers a magical world.",
    "In this novel, a young girl faces numerous challenges to save her family.",
    "A detective story full of suspense and unexpected twists."
]

# Appliquer le prétraitement
preprocessed_resumes = [preprocess_text(resume) for resume in resumes]

# Convertir les résumés prétraités en DataFrame
df = pd.DataFrame({'preprocessed_resumes': [' '.join(tokens) for tokens in preprocessed_resumes]})

# Sauvegarder les résumés prétraités dans un fichier CSV
csv_path = '/home/ascud/Documents/LivreaPiques/sprint3_reco/preprocessed_resumes.csv'
df.to_csv(csv_path, index=False)

# Charger les résumés prétraités depuis le fichier CSV
loaded_df = pd.read_csv(csv_path)
loaded_preprocessed_resumes = [text.split() for text in loaded_df['preprocessed_resumes']]

# Entraîner un modèle Word2Vec avec Gensim
w2v_model = Word2Vec(
    sentences=preprocessed_resumes,  # Corpus de phrases
    vector_size=100,                 # Taille des vecteurs
    window=5,                        # Contexte de mots
    min_count=1,                     # Minimum de mots à inclure
    workers=4                        # Utilisation des cœurs de processeur
)

# Fonction pour obtenir le vecteur moyen d'un résumé
def get_sentence_vector(tokens, model):
    # Filtrer les mots qui existent dans le vocabulaire du modèle
    valid_tokens = [token for token in tokens if token in model.wv.key_to_index]
    if not valid_tokens:  # Si aucun mot n'est dans le vocabulaire
        return np.zeros(model.vector_size)
    # Calculer la moyenne des vecteurs des mots
    return np.mean([model.wv[token] for token in valid_tokens], axis=0)


# Générer les vecteurs pour chaque résumé
resume_vectors = [get_sentence_vector(tokens, w2v_model) for tokens in preprocessed_resumes]

# Exemple de similarité entre les résumés


# Calculer une matrice de similarité
similarity_matrix = cosine_similarity(resume_vectors)

# Afficher les similarités
print("Matrice de similarité :")
print(similarity_matrix)
