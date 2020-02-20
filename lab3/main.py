from crud import Database
from fastapi import FastAPI, HTTPException

app = FastAPI()
db = Database("movies.sqlite")

@app.get("/ping")
def return_pong():
    return "pong"

@app.get("/reset")
def write_reset():
    db.reset()
    return "OK"

@app.get("/users")
def read_users():
    return({"data": db.users()})

@app.get("/movies")
def read_movies(title: str = None, year: int = None):
    return({"data": db.movies(title, year)})
    

@app.get("/movies/{imdbKey}")
def search_movies(imdbKey: str):
    return({"data": db.movies_by_key(imdbKey)})


@app.get("/theaters")
def read_theaters():
    return({"data": db.theaters()})


@app.get("/performances")
def read_performances():
    return({"data": db.performances()})

@app.get("/performances/{performance_id}")
def search_performances(performance_id: str):
    return({"data": db.performances_by_key(performance_id)})

@app.post("/performances")
def write_performance(imdb: str, theater: str, date: str, time: str):
    (success, performance_id) = db.add_performance(imdb, theater, date, time)
    if not success:
        raise HTTPException(status_code=400, detail="No such movie or theater")
    return("/performances/{}".format(performance_id))


@app.get("/tickets")
def read_tickets():
    return({"data": db.tickets()})

@app.post("/tickets")
def add_ticket(performance: str, user: str, pwd: str):
    (success, message) = db.add_ticket(performance, user, pwd)
    print(message)

    if not success:
        if 'User does not exist or wrong credentials.' == message:
            raise HTTPException(status_code=404, detail="Wrong password")
        elif 'Insufficient seats' == message:
            raise HTTPException(status_code=500, detail="No tickets left")
    return("/tickets/{}".format(message))

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
