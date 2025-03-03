import fastapi as fa
from SQL_controleur.SQL_controleur import *

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
async def read_api(title: str):
    print(title)
    title = title.replace("'", "''")
    df = requete("""    SELECT *
                        FROM allbookdata
                        WHERE TRIM(allbookdata.book_title) ILIKE '{title}'""".format(title=title))  
    if df.empty:
        return fa.Response(status_code=204)
    df = df.fillna(value=False)
    print("Where does it bugs ?")
    return df.to_dict(orient="records")

@app.get("/api/books")
async def read_api():
    df = requete("""    SELECT * 
                        FROM allbookdata""")
    if df.empty:
        return fa.Response(status_code=204)
    df = df.fillna(value=False)
    return df.to_dict(orient="records")

@app.get("/api/books/name={author_name}")
async def read_api(author_name: str):
    print(author_name)
    author_name = author_name.replace("'", "''")
    df = requete("""    SELECT * 
                        FROM allbookdata
                        WHERE TRIM(allbookdata.authors) ILIKE '{author_name}'""".format(author_name=author_name))
    if df.empty:
        return fa.Response(status_code=204)  
    df = df.fillna(value=False)
    return df.to_dict(orient="records")

@app.get("/api/books/genre={genre}")
async def read_api(genre: str):
    print(genre)
    genre = genre.replace("'", "''")
    genre = "%" + genre + "%"
    df = requete("""    SELECT *
                        FROM allbookdata
                        WHERE TRIM(allbookdata.genres) ILIKE '{genre}'""".format(genre=genre))
    if df.empty:
        return fa.Response(status_code=204)
    df = df.fillna(value=False)
    return df.to_dict(orient="records")

@app.get("/api/books/id={book_id}")
async def read_api(book_id: int):
    df = requete("""    SELECT *
                        FROM allbookdata
                        WHERE allbookdata.book_id = {id}""".format(id=book_id))    
    if df.empty:
        return fa.Response(status_code=204)
    df = df.fillna(value=False)
    return df.to_dict(orient="records")