import fastapi as fa

app = fa.FastAPI()

@app.get("/")
async def read_root():
    return {"message": "This is a FastAPI application."}

@app.get("/api")
async def read_api():
    return {"message": "It should exist"}