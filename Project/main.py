from crud import Database
from fastapi import FastAPI, HTTPException

app = FastAPI()
db = Database("cookieProductionDb.sqlite")

@app.get("/ping")
def return_pong():
    return "pong"

@app.post("/reset")
def write_reset():
    db.reset()
    return ({"status": "ok"})

@app.get("/customers")
def read_customers():
    return({"customers": db.get_customers()})

