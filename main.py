from enum import Enum
from typing import Optional, Union

from fastapi import FastAPI, HTTPException
from model import Item, MonsterDetail, Skill, MonsterFamily
from database import engine
from sqlmodel import Session, select

app = FastAPI()


"""
Start of ENUMERATE Class for Swagger UI dropdown menu
https://fastapi.tiangolo.com/tutorial/path-params/#predefined-values
Question for these enumerate class -- should these classes be in main.py, or 
should it be a subclass in the Item class in model.py?
"""
class ItemCategory(str, Enum):
    """
    Create dropdown menu for read_items() in Swagger UI to filter by
    item_category. Works for predefined choices in item_category.
    For the Item class model
    """
    recovery = "recovery"
    meat = "meat"
    staff = "staff"
    seed = "seed"
    book = "book"
    dungeon_use = "dungeon use"


class ItemSellLocation(str, Enum):
    """
    Create dropdown menu for read_items() in Swagger UI to filter by
    sell_location. For Item class model
    """
    bazzar_shop_1 = "Bazaar shop 1"
    bazzar_shop_2 = "Bazaar shop 2"
    bazzar_shop_3 = "Bazaar shop 3"
    bazzar_shop_4 = "Bazaar shop 4"
    field_shop = "Field shop"
    found_in_field = "found in field"


class SkillCategory(str, Enum):
    """
    Create dropdown menu for read_skill() in Swagger UI to filter by
    category_type. Works for predefined choices in the Skill model class
    """
    attack = "Attack"
    support = "Support"
    recovery = "Recovery"


class SkillFamily(str, Enum):
    """
    Create dropdown menu for read_skill() in Swagger UI to filter by
    family_type. Works for predefined choices in the Skill model class
    """
    frizz = "Frizz"
    sizz = "Sizz"
    bang = "Bang"
    woosh = "Woosh"
    zap = "Zap"
    crack = "Crack"
    whack = "Whack"
    kamikazee = "Kamikazee"
    magic_burst = "Magic Burst"
    help = "Help"
    fire = "Fire"
    ice = "Ice"
    poison = "Poison"
    paralyze = "Paralyze"
    sleep = "Sleep"
    gigaslash = "Gigaslash"
    attack = "Attack"
    dazzle = "Dazzle"
    drain_magic = "Drain Magic"
    fuddle = "Fuddle"
    sap = "Sap"
    curse = "Curse"
    decelerate = "Decelerate"
    ban_dance = "Ban Dance"
    gobstop = "Gobstop"
    lose_turn = "Lose a turn"
    defense = "Defense"
    status_support = "Status support"
    summon = "Summon"
    heal = "Heal"
    status_recovery = "Status recovery"
    revive = "Revive"
    map = "Map"


# Start of actual app pages
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
def read_skill(item_id: int):
    with Session(engine) as session:
        item = session.get(Item, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
