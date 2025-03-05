import fastapi as fa
from fastapi import HTTPException
from pydantic import BaseModel
import hashlib
from SQL_controleur.SQL_controleur import *
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy import text  # Ajoute cette ligne

# Pour lancer le serveur : uvicorn api:app --reload (dans le dossier de l'api)

app = fa.FastAPI()

@app.exception_handler(fa.HTTPException)
async def http_exception_handler(request: fa.Request, exc: fa.HTTPException):
    return fa.responses.JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Big Book Society API"}

@app.get("/api/books/title={book_title}")
async def read_api(book_title: str):
    print(book_title)
    book_title = book_title.replace("'", "''")
    df = requete("SELECT * FROM allbookdata")  
    df = df[df['book_title'].str.contains(book_title, case=False, na=False)]
    if df.empty:
        return fa.Response(status_code=204)
    df = df.fillna(value=False)
    return df.to_dict(orient="records")

@app.get("/api/books")
async def read_api():
    df = requete("SELECT * FROM allbookdata")
    if df.empty:
        return fa.Response(status_code=204)
    df = df.fillna(value=False)
    return df.to_dict(orient="records")

@app.get("/api/books/name={author_name}")
async def read_api(author_name: str):
    print(author_name)
    author_name = author_name.replace("'", "''")
    df = requete("SELECT * FROM allbookdata".format(author_name=author_name))
    df = df[df['authors'].str.contains(author_name, case=False, na=False)]
    if df.empty:
        return fa.Response(status_code=204)  
    df = df.fillna(value=False)
    return df.to_dict(orient="records")

@app.get("/api/books/genre={genre}")
async def read_api(genre: str):
    print(f"Received genre: {genre}")
    genre = genre.replace("'", "''")
    df = requete("SELECT * FROM allbookdata")
    print(df)
    filtered_df = df[df['genres'].str.contains(genre, case=False, na=False)]
    if filtered_df.empty:
        return fa.Response(status_code=204)
    filtered_df = filtered_df.fillna(value=False)
    return filtered_df.to_dict(orient="records")

@app.get("/api/books/id={book_id}")
async def read_api(book_id: int):
    df = requete("""    SELECT *
                        FROM allbookdata
                        WHERE allbookdata.book_id = {id}""".format(id=book_id))    
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
    hashed_password = hashlib.sha256((password ).encode()).hexdigest()
    return hashed_password

@app.post("/create_user/")
async def create_user(user: UserCreate):
    user.password = hash_password(user.password)
    
    query = text("""INSERT INTO "user" (username, password, age, gender, nb_book_per_year, nb_book_pleasure, nb_book_work, initiated_by, reading_time, choice_motivation) 
                 VALUES (:username, :password, :age, :gender, :nb_book_per_year, :nb_book_pleasure, :nb_book_work, :initiated_by, :reading_time, :choice_motivation)""")
    
    try:
        engine, session = conexion_db()
        session.execute(query, {"username": user.name, "password": user.password, "age": user.age, "gender": user.gender, "nb_book_per_year" : user.nb_book_per_year, "nb_book_pleasure" : user.nb_book_pleasure, "nb_book_work" : user.nb_book_work, "initiated_by" : user.initiated_by, "reading_time" : user.initiated_by, "reading_time" : user.reading_time, "choice_motivation" : user.choice_motivation})
        session.commit()
        return {"message": "Utilisateur créé avec succès"}
    except Exception as e:
        print(f"Erreur lors de la création de l'utilisateur: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de l'utilisateur: {str(e)}")
    
    
@app.post("/login/")
async def connection(user: UserLogin):
    hashed_password = hash_password(user.password)
    query = text('SELECT * FROM "user" WHERE username = :username AND password = :password')
    
    try:
        engine, session = conexion_db()
        result = session.execute(query, {"username": user.name, "password": hashed_password}).fetchone()
        
        if result:
            return {"message": "Connexion réussie"}
        else:
            raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")
    except Exception as e:
        print(f"Erreur lors de la connexion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la connexion: {str(e)}")

