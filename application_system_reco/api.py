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

# Pour lancer le serveur : uvicorn api:app --reload (dans le dossier de l'api)

app = fa.FastAPI()


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
    return df.to_dict(orient="records")

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

def insert(requete: str):
    """
    Fonction simulant l'insertion dans une base de données.
    Dans une vraie application, elle exécuterait une requête SQL.
    """
    print(f"Exécution de la requête : {requete}")

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
