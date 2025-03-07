import fastapi as fa
from fastapi import HTTPException
from pydantic import BaseModel
import hashlib
from SQL_controleur.SQL_controleur import *
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy import text  # Ajoute cette ligne
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
import os
import uvicorn
from system_reco.reco_esteban import *
from system_reco.reco_benjamin import *

# Pour lancer le serveur : uvicorn api:app --reload (dans le dossier de l'api)

app = fa.FastAPI()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Récupération automatique du port
    uvicorn.run(app, host="0.0.0.0", port=port)
    
# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplace par ton URL front si nécessaire
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permet tous les headers
)

@app.exception_handler(fa.HTTPException)
async def http_exception_handler(request: fa.Request, exc: fa.HTTPException):
    return fa.responses.JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(fa.HTTPException)
async def http_exception_handler(request: fa.Request, exc: fa.HTTPException):
    return fa.responses.JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.get("/")
async def read_root():
    df = requete("SELECT * FROM allbookdata")
    return {"message": "Welcome to the Big Book Society API"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) 
    uvicorn.run(app, host="0.0.0.0", port=port)

# Endpoint to filter books by various attributes
# /api/books/?book_title=<title of the book>&author_name=<name of the author>&genre=<name of the genre>&series=<name of the series>
@app.get("/api/books/")
async def read_api(book_title: str = None, author_name: str = None, genre: str = None, series: str = None):
    # Fetch all data from the database
    df = requete("SELECT * FROM allbookdata")

    # Apply filters based on the provided query parameters
    if book_title:
        df = df[df['book_title'].str.contains(book_title, case=False, na=False)]
    if author_name:
        df = df[df['authors'].str.contains(author_name, case=False, na=False)]
    if genre:
        df = df[df['genres'].str.contains(genre, case=False, na=False)]
    if series:
        df = df[df['series'].str.contains(series, case=False, na=False)]

    if df.empty:
        return fa.Response(status_code=204)

    df = df.fillna(value=False)
    return df.to_dict(orient="records")  # Returns a list of books matching the filters

# Endpoint to search for books containing a query string in any attribute
# /api/books/search?query=<string your searching for>
@app.get("/api/books/search")
async def search_books(query: str):
    # Fetch all data from the database
    df = requete("SELECT * FROM allbookdata")
    df = df.fillna('')

    # Search for the query string in multiple attributes
    filtered_df = df[
        df.apply(
            lambda row: query.lower() in row['book_title'].lower() or
                        query.lower() in row['authors'].lower() or
                        query.lower() in row['genres'].lower() or
                        query.lower() in row['series'].lower(),
            axis=1
        )
    ]

    # Limit the results to 10
    filtered_df = filtered_df.head(10)

    if filtered_df.empty:
        return fa.Response(status_code=204)

    filtered_df = filtered_df.fillna(value=False)
    return filtered_df.to_dict(orient="records")  # Returns up to 10 books containing the query string

    filtered_df = filtered_df.fillna(value=False)
    return filtered_df.to_dict(orient="records")

@app.get("/api/books/{book_id}")
async def read_api(book_id: int):
    df = requete(f"""SELECT * FROM allbookdata WHERE allbookdata.book_id = {book_id}""")    
    if df.empty:
        return fa.Response(status_code=204)
    df = df.fillna(value=False)
    return df.to_dict(orient="records")

# Modèle pour la requête utilisateur
class UserCreate(BaseModel):
    name: str
    password: str
    age: int
    gender: str
    nb_book_per_year: str
    nb_book_pleasure: str
    nb_book_work: str
    initiated_by: str
    reading_time: str
    choice_motivation: str

# Modèle pour la connexion d'utilisateur
class UserLogin(BaseModel):
    name: str
    password: str

def hash_password(password: str):
    """
    Fonction de hashage du mot de passe.
    utilise sha-256 pour le hashage
    """
    # Génération du sel
    # Hashage du mot de passe
    # utiliser un .env pour récupérer le sel
    hashed_password = hashlib.sha256((password ).encode()).hexdigest()
    return hashed_password

@app.get("/api/check_username_availabitily/{username}")
async def check_username_availabitily(username: str):
    engine, session = conexion_db()

    try:
        # Utilisation de paramètres pour la requête pour éviter l'injection SQL
        check_username_query = text("""SELECT user_id FROM "user" WHERE username = :username """)
        result = session.execute(check_username_query, {"username": username}).fetchone()

        if result:
            # L'utilisateur existe déjà
            raise HTTPException(status_code=409, detail="Nom d'utilisateur déjà pris")

        return {"message": "Nom d'utilisateur disponible"}

    except SQLAlchemyError as e:
        # Capture les erreurs liées à SQLAlchemy et les renvoie sous forme d'exception HTTP
        session.rollback()  # Rétablir la transaction en cas d'erreur
        raise HTTPException(status_code=500, detail="Erreur de base de données: " + str(e))

    finally:
        session.close()  # Fermer la session

@app.post("/api/create_user/")
async def create_user(user: UserCreate):
    user.password = hash_password(user.password)
    
    query = text("""
    INSERT INTO "user" (username, password, age, gender, nb_book_per_year, nb_book_pleasure, nb_book_work, initiated_by, reading_time, choice_motivation) 
    VALUES (:username, :password, :age, :gender, :nb_book_per_year, :nb_book_pleasure, :nb_book_work, :initiated_by, :reading_time, :choice_motivation)
    RETURNING user_id """)
    
    try:
        engine, session = conexion_db()
        result = session.execute(query, {"username": user.name, "password": user.password, "age": user.age, "gender": user.gender, "nb_book_per_year" : user.nb_book_per_year, "nb_book_pleasure" : user.nb_book_pleasure, "nb_book_work" : user.nb_book_work, "initiated_by" : user.initiated_by, "reading_time" : user.reading_time, "choice_motivation" : user.choice_motivation})
        session.commit()
        user_id = result.fetchone()[0]

        return {"message": "Utilisateur créé avec succès", "user_id": user_id}
    except Exception as e:
        print(f"Erreur lors de la création de l'utilisateur: {str(e)}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de l'utilisateur: {str(e)}")
    
    
@app.post("/api/login/")
async def connection(user: UserLogin):
    hashed_password = hash_password(user.password)
    query = text('SELECT * FROM "user" WHERE username = :username AND password = :password')
    
    try:
        engine, session = conexion_db()
        result = session.execute(query, {"username": user.name, "password": hashed_password}).fetchone()

        if result:
            user_id = result[0]  # Si user_id est la première colonne retournée
            return {"message": "Utilisateur connecté avec succès", "user_id": user_id}       
        else:
            raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")
    except Exception as e:
        print(f"Erreur lors de la connexion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la connexion: {str(e)}")


class UserID(BaseModel):
    """
    Modèle représentant un utilisateur avec un identifiant unique.
    """
    id: int

def Ltitle_to_Lid(Ltitle):
    LrecoID = []
    for title in Ltitle:
        #si le titre contient des ' remplacer par ''
        for i in range(len(Ltitle)):
            # Si le titre contient des ' remplacer par ''
            Ltitle[i] = Ltitle[i].replace("'", "''")

        result = requete(f"""select book_id from book where book_title = '{title}' """, True, False)
        LrecoID.append(int(result["book_id"].iloc[0]))
    return LrecoID

@app.post("/api/reco2/")
async def recommendation(user: UserID):
    """
    Génère des recommandations de livres basées sur un système de recommandation avancé.

    Entrée :
    - user (UserID) : Un objet contenant l'identifiant de l'utilisateur (non utilisé ici).

    Sortie :
    - Un dictionnaire contenant une liste de titres de livres recommandés.

    Cette fonction utilise `FinalRecommender` pour obtenir les recommandations, mais l'ID utilisateur n'est
    pas pris en compte dans cette version (valeur fixe de 1).
    """
    try:
        reco_benj = FinalRecommender()
        Lreco = reco_benj.get_recommendations(1, 5)  # L'ID utilisateur est fixé à 1 ici
        Ltitles = [book["title"] for book in Lreco]
        LrecoID = Ltitle_to_Lid(Ltitles)
        return {"recommendations": LrecoID}
    except Exception as e:
        print(f"Erreur lors de la recommandation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la recommandation: {str(e)}")
    
class UserBook (BaseModel):
    user_id: int
    book_id: int

@app.post("/api/likedbook/")
async def LikedBook(UserBook: UserBook):
    #mettre sous forme de dataFrame UserBook avec comme colonne user_id et book_id
    df = pd.DataFrame([UserBook.model_dump()])
    try:
        if(insert(df, "liked_books")):
            return {"message": "Liked ajouté"}
        else:
            raise HTTPException(status_code=500, detail=f"Erreur lors de l'insertion")
    except Exception as e:
        print(f"Erreur lors de la recommandation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'insertion: {str(e)}")
    
@app.get("/api/likedbook/{user_id}/{book_id}")
async def check_if_liked(user_id: int, book_id: int):
    """
    Vérifie si un utilisateur a liké un livre.
    """
    try:
        # Requête pour vérifier si une entrée existe dans liked_books pour cet utilisateur et ce livre
        query = text("""
            SELECT * FROM liked_books WHERE user_id = :user_id AND book_id = :book_id
        """)
        
        # Exécution de la requête
        engine, session = conexion_db()
        result = session.execute(query, {"user_id": user_id, "book_id": book_id}).fetchone()
        
        if result:
            # Si une entrée existe, l'utilisateur a liké le livre
            return {"liked": True}
        else:
            # Sinon, l'utilisateur n'a pas liké le livre
            return {"liked": False}
    except SQLAlchemyError as e:
        # Gestion des erreurs SQL
        raise HTTPException(status_code=500, detail="Erreur de base de données: " + str(e))
    finally:
        session.close()  # Assure-toi de fermer la session


@app.get("/api/user/{user_id}/profile")
async def get_user_profile(user_id: int):
    try:
        # Récupération des informations de l'utilisateur
        user_query = text("""
            SELECT username, age, gender, nb_book_per_year, nb_book_pleasure, nb_book_work, initiated_by, reading_time, choice_motivation
            FROM "user" WHERE user_id = :user_id
        """)
        
        # Exécution de la requête pour récupérer les infos de l'utilisateur
        engine, session = conexion_db()
        user_result = session.execute(user_query, {"user_id": user_id}).fetchone()

        if not user_result:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        
        # Récupération des livres likés par l'utilisateur
        liked_books_query = text("""
            SELECT book_id FROM liked_books WHERE user_id = :user_id
        """)
        
        liked_books_result = session.execute(liked_books_query, {"user_id": user_id}).fetchall()
        liked_books = [book[0] for book in liked_books_result]

        # Récupération des informations détaillées des livres likés
        books_query = text("""
            SELECT book_id, book_cover, book_description FROM book WHERE book_id IN :book_ids
        """)
        
        books_result = session.execute(books_query, {"book_ids": tuple(liked_books)}).fetchall()
        books_details = [
            {"book_id": book[0], "book_cover": book[1], "book_description": book[2][:150]}  # Limiter la description à 100 caractères
            for book in books_result
        ]

        # Fermeture de la session
        session.close()

        # Construction de la réponse
        user_profile = {
            "username": user_result[0],
            "age": user_result[1],
            "gender": user_result[2],
            "nb_book_per_year": user_result[3],
            "nb_book_pleasure": user_result[4],
            "nb_book_work": user_result[5],
            "initiated_by": user_result[6],
            "reading_time": user_result[7],
            "choice_motivation": user_result[8],
            "liked_books": books_details
        }

        return user_profile

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des données: " + str(e))
    

@app.delete("/api/user/{user_id}/like/{book_id}")
async def remove_like(user_id: int, book_id: int):
    try:
        # Connexion à la base de données
        engine, session = conexion_db()

        # Vérifier si le livre est déjà liké par l'utilisateur
        liked_book_query = text("""
            SELECT 1 FROM liked_books WHERE user_id = :user_id AND book_id = :book_id
        """)
        result = session.execute(liked_book_query, {"user_id": user_id, "book_id": book_id}).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Like non trouvé")

        # Supprimer le like de la base de données
        delete_like_query = text("""
            DELETE FROM liked_books WHERE user_id = :user_id AND book_id = :book_id
        """)
        session.execute(delete_like_query, {"user_id": user_id, "book_id": book_id})
        session.commit()

        # Fermeture de la session
        session.close()

        return {"message": "Like supprimé avec succès"}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Erreur lors de la suppression du like: " + str(e))
