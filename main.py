from database import engine
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from typing import Optional, Union, List

from model import MonsterBreedingLink, MonsterBreedingLinkReadWithInfo, \
    MonsterDetail, MonsterDetailWithFamily, MonsterDetailSkill, \
    MonsterFamily, MonsterFamilyReadWithMonsterDetail,  \
    Skill, SkillUpgradeRead, SkillCombine, SkillCombineRead, Item

from model_enum import SkillCategory, SkillFamily, ItemCategory, \
    ItemSellLocation

app = FastAPI()


def get_session():  # place in database.py?
    with Session(engine) as session:
        yield session


@app.get("/")
def root():
    return {"message": "Hello World!!"}


@app.get("/dqm1/monsters", response_model=List[MonsterDetailWithFamily])
def read_monsters(*, session: Session = Depends(get_session),
                  family: Union[int, None] = None):
    monsters = select(MonsterDetail)
    if family:
        monsters = monsters.where(MonsterDetail.family_id == family)
    monsters = session.exec(monsters).all()
    return monsters


@app.get("/dqm1/monsters/{monster_id}",
         response_model=MonsterDetailWithFamily)
def read_monster(*, session: Session = Depends(get_session), monster_id: int):
    monster = session.get(MonsterDetail, monster_id)
    if not monster:
        raise HTTPException(status_code=404, detail="Monster not found")
    return monster


@app.get("/dqm1/monstersandskill/{monster_id}",
         response_model=MonsterDetailSkill)
def read_monster(*, session: Session = Depends(get_session), monster_id: int):
    monster = session.get(MonsterDetail, monster_id)
    if not monster:
        raise HTTPException(status_code=404, detail="Monster not found")
    return monster


@app.get('/dqm1/family/{family_id}',
         response_model=MonsterFamilyReadWithMonsterDetail)
def read_family(*, session: Session = Depends(get_session), family_id: int):
    family = session.get(MonsterFamily, family_id)
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    return family


@app.get("/dqm1/skills")
def read_skills(
        *, session: Session = Depends(get_session),
        category: Union[SkillCategory, None] = None,
        skill_family: Union[SkillFamily, None] = None):
    skills = select(Skill)
    if category:
        skills = skills.where(Skill.category_type == category)
    if skill_family:
        skills = skills.where(Skill.family_type == skill_family)
    skills = session.exec(skills).all()
    return skills


@app.get("/dqm1/skills/{skill_id}", response_model=SkillUpgradeRead)
def read_skill(*, session: Session = Depends(get_session), skill_id: int):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@app.get("/dqm1/skillcombine/{skill_id}",
         response_model=List[SkillCombineRead])
def get_skill_combo(*, session: Session = Depends(get_session), skill_id: int):
    query = select(SkillCombine).where(SkillCombine.combo_skill_id == skill_id)
    skill = session.exec(query).all()
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
def read_item(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/breeding/{child_id}",
         response_model=List[MonsterBreedingLinkReadWithInfo])
def get_parents_for_child(
        *, session: Session = Depends(get_session), child_id: int):
    query = select(MonsterBreedingLink).where(
        MonsterBreedingLink.child_id == child_id)
    parents = session.exec(query).all()
    return parents
