import pandas as pd
import random
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from tqdm import tqdm

# Dummy data generation functions
def random_gender():
    return random.choice(['M', 'F', 'A'])

def random_age():
    return random.choice(["10-20", "20-30", "30-40", "40-50", "50+"])

def random_motivation():
    return random.choice(["pleasure", "work", "curiosity"])

nbUsers = 10000
# Simulate user data
user_data = {
    "user_id": [i for i in range(1, nbUsers + 1)],
    "username": [f"user_{i}" for i in range(1, nbUsers + 1)],
    "password": [f"pass_{random.randint(1000, 9999)}" for _ in range(1, nbUsers + 1)],
    "gender": [random_gender() for _ in range(1, nbUsers + 1)],
    "nb_book_per_year": [random.randint(0, 20) for _ in range(1, nbUsers + 1)],
    "nb_book_pleasure": [random.randint(0, 10) for _ in range(1, nbUsers + 1)],
    "nb_book_work": [random.randint(0, 10) for _ in range(1, nbUsers + 1)],
    "initiated_by": [random.choice(["friend", "teacher", "self"]) for _ in range(1, nbUsers + 1)],
    "reading_motivation": [random_motivation() for _ in range(1, nbUsers + 1)],
    "age": [random_age() for _ in range(1, nbUsers + 1)],
}

# Simulate liked books
liked_books = {
    "user_id": [random.randint(1, nbUsers) for _ in range(nbUsers * 2)],
    "book_id": [random.randint(1, 50) for _ in range(nbUsers * 2)],
}

# Simulate liked authors
liked_authors = {
    "user_id": [random.randint(1, nbUsers) for _ in range(int(nbUsers * 1.5))],
    "author_id": [random.randint(1, 50) for _ in range(int(nbUsers * 1.5))],
}

# Simulate liked genres
liked_genres = {
    "user_id": [random.randint(1, nbUsers) for _ in range(nbUsers * 2)],
    "genre_id": [random.randint(1, 10) for _ in range(nbUsers * 2)],
}

# Convert to DataFrames
df_user = pd.DataFrame(user_data)
df_liked_books = pd.DataFrame(liked_books)
df_liked_authors = pd.DataFrame(liked_authors)
df_liked_genres = pd.DataFrame(liked_genres)

# Merge tables to simulate SQL join result
df_merged = (
    df_user
    .merge(df_liked_books, on="user_id", how="left")  # Join with liked_books
    .merge(df_liked_authors, on="user_id", how="left")  # Join with liked_authors
    .merge(df_liked_genres, on="user_id", how="left")  # Join with liked_genres
)

# Vectorisation, un user ne donne que 1 vecteur
listofBooks = []
listofAuthors = []
listofGenres = []
# Get distinct values for book_id, author_id, and genre_id
distinct_books = df_merged['book_id'].dropna().unique().tolist()
distinct_authors = df_merged['author_id'].dropna().unique().tolist()
distinct_genres = df_merged['genre_id'].dropna().unique().tolist()

listofBooks = distinct_books
listofAuthors = distinct_authors
listofGenres = distinct_genres

print(listofBooks)
print(listofAuthors)
print(listofGenres)


# Display the final DataFrame
print("Resulting DataFrame:")
print(df_merged[['user_id', 'username', 'book_id', 'author_id', 'genre_id']].head())

encoder = OneHotEncoder()

encoderL = LabelEncoder()

# Fusionner les colonnes d'intérêt
vector_data = df_merged
# Appliquer l'encodage OneHot
encoded_matrix = encoder.fit_transform(vector_data)

print("Shape of vectorized data:", encoded_matrix.shape)
'''
encoderL_data = df_merged

encoded_matrixL = encoderL.fit_transform(encoderL_data)

print("Shape of vectorized data:", encoded_matrixL.shape)
'''
