from typing import Optional

from fastapi import FastAPI, HTTPException
from model import Item, MonsterDetail, MonsterBreedingLink, Skill, MonsterFamily
from database import create_db_and_tables, engine
from sqlmodel import Session, select

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World!!"}


@app.get("/dqm1/monsters")
def read_monsters():
    with Session(engine) as session:
        monsters = select(MonsterDetail, MonsterFamily).join(MonsterFamily)
        # if family:
        #     monsters = monsters.where(MonsterDetail.family_eng == family)
        monsters = session.exec(monsters).all()
        return monsters


@app.get("/dqm1/monsters/{monster_id}")
def read_monster(monster_id: int):
    with Session(engine) as session:
        monster = session.get(MonsterDetail, monster_id)
        if not monster:
            raise HTTPException(status_code=404, detail="Monster not found")
        return monster


@app.get("/dqm1/skills")
def read_skills():
    with Session(engine) as session:
        skills = session.exec(select(Skill)).all()
        return skills


@app.get("/dqm1/skills/{skill_id}")
def read_skill(skill_id: int):
    with Session(engine) as session:
        skill = session.get(Skill, skill_id)
        if not skill:
            raise HTTPException(status_code=404, detail="Skill not found")
        return skill


# @app.get("/dqm1/items")
# def read_items(category: Optional[?] = None):
#     with Session(engine) as session:
#         items = select(Item)
#         if category:
#             items = items.where(Item.item_category == category)
#         items = session.exec(items).all()
#         return items


@app.get("/dqm1/items/{item_id}")
def read_skill(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
