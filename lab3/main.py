from crud import Database
from fastapi import FastAPI

app = FastAPI()
db = Database("movies.sqlite")

@app.get("/ping")
def return_pong():
    return "pong"

@app.get("/reset")
def write_reset():
    db.reset()


@app.get("/users")
def read_users():
    return({"data": db.users()})


@app.get("/movies")
def read_movies():
    return({"data": db.movies()})


@app.get("/theaters")
def read_theaters():
    return({"data": db.theaters()})


@app.get("/performances")
def read_performances():
    return({"data": db.performances()})


@app.get("/tickets")
def read_tickets():
    return({"data": db.tickets()})


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
