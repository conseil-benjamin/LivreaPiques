import fastapi as fa
from SQL_controleur.SQL_controleur import *

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

@app.get("/api/books")
async def read_api():
    df = requete("""    SELECT * 
                        FROM book 
                        JOIN book_author ON book.book_id = book_author.book_id
                        JOIN author ON book_author.author_id = author.author_id
                        UNION
                        SELECT *
                        FROM book
                        LEFT JOIN book_author ON book.book_id = book_author.book_id
                        LEFT JOIN author ON book_author.author_id = author.author_id""")
    if df.empty:
        return fa.Response(status_code=204)
    df = df.fillna(value=False)
    return df.to_dict(orient="records")

@app.get("/api/books/name={book_title}")
async def read_api(book_title: str):
    print(book_title)
    book_title = book_title.replace("'", "''")
    df = requete("""    SELECT * 
                        FROM book 
                        JOIN book_author ON book.book_id = book_author.book_id
                        JOIN author ON book_author.author_id = author.author_id
                        WHERE TRIM(book.book_title) ILIKE '{title}'
                        UNION
                        SELECT *
                        FROM book
                        LEFT JOIN book_author ON book.book_id = book_author.book_id
                        LEFT JOIN author ON book_author.author_id = author.author_id
                        WHERE TRIM(book.book_title) ILIKE '{title}'""".format(title=book_title))  
    if df.empty:
        return fa.Response(status_code=204)  
    df = df.fillna(value=False)
    return df.to_dict(orient="records")

@app.get("/api/books/id={book_id}")
async def read_api(book_id: int):
    df = requete("""    SELECT * 
                        FROM book 
                        JOIN book_author ON book.book_id = book_author.book_id
                        JOIN author ON book_author.author_id = author.author_id
                        WHERE book.book_id = {id}
                        UNION
                        SELECT *
                        FROM book
                        LEFT JOIN book_author ON book.book_id = book_author.book_id
                        LEFT JOIN author ON book_author.author_id = author.author_id
                        WHERE book.book_id = {id}""".format(id=book_id))    
    if df.empty:
        return fa.Response(status_code=204)
    df = df.fillna(value=False)
    return df.to_dict(orient="records")

@app.get("/api/author/{author_name}")
async def read_api(author: str):
    author = author.replace("'", "''")
    df = requete("""    SELECT * 
                        FROM author
                        WHERE TRIM(author_name) ILIKE '{author_name}'""".format(author_name=author))
    if df.empty:
        return fa.Response(status_code=204)
    df = df.fillna(value=False)
    return df.to_dict(orient="records")