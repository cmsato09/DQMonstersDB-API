from fastapi import FastAPI
from model import Item
from database import create_db_and_tables, engine
from sqlmodel import Session, select

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World!!"}


@app.get("/dqm1/items")
def read_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return items
