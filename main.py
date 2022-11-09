from typing import Optional, Union

from fastapi import FastAPI, HTTPException
from model import Item, MonsterDetail, Skill, MonsterFamily, SkillCategory, \
    SkillFamily, ItemCategory, ItemSellLocation
from database import engine
from sqlmodel import Session, select

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World!!"}


@app.get("/dqm1/monsters")
def read_monsters(family: Union[int, None] = None):
    with Session(engine) as session:
        monsters = select(MonsterDetail, MonsterFamily).join(MonsterFamily)
        if family:
            monsters = monsters.where(MonsterDetail.family_id == family)
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
def read_skills(
        category: Union[SkillCategory, None] = None,
        skill_family: Union[SkillFamily, None] = None):
    with Session(engine) as session:
        skills = select(Skill)
        if category:
            skills = skills.where(Skill.category_type == category)
        if skill_family:
            skills = skills.where(Skill.family_type == skill_family)
        skills = session.exec(skills).all()
        return skills


@app.get("/dqm1/skills/{skill_id}")
def read_skill(skill_id: int):
    with Session(engine) as session:
        skill = session.get(Skill, skill_id)
        if not skill:
            raise HTTPException(status_code=404, detail="Skill not found")
        return skill


@app.get("/dqm1/items")
def read_items(
        category: Union[ItemCategory, None] = None,
        selllocation: Union[ItemSellLocation, None] = None):
    with Session(engine) as session:
        items = select(Item)
        if category:
            items = items.where(Item.item_category == category)
        if selllocation:
            items = items.where(Item.sell_location == selllocation)
        items = session.exec(items).all()
        return items


@app.get("/dqm1/items/{item_id}")
def read_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
