from database import engine
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select
from typing import Optional, List
from fastapi.staticfiles import StaticFiles

from models import (
    MonsterBreedingLink, MonsterBreedingLinkReadWithInfo,
    MonsterDetail, MonsterDetailWithFamily, MonsterDetailSkill,
    MonsterFamily, MonsterFamilyReadWithMonsterDetail,
    Skill, SkillUpgradeRead, SkillCombine, SkillCombineRead,
    Item,
)
from model_enums import (
    SkillCategory,
    SkillFamily,
    ItemCategory,
    ItemSellLocation,
)

tags_metadata = [
    {
        "name": "dqm1 monsters",
        "description": "Monster list",
    },
    {
        "name": "dqm1 skills",
        "description": "Skills that monsters learn and inherit",
    },
    {
        "name": "dqm1 items",
        "description": "Useful items found in the game and their description",
    },
]

app = FastAPI(
    title="Dragon Quest Monsters Database API",
    description="API to get game information for the original DQMonsters "
                "gameboy game",
    version="1.0.0",
    openapi_tags=tags_metadata
)
app.mount("/static", StaticFiles(directory="static"), name="static")


async def get_session():  # place in database.py?
    with Session(engine) as session:
        yield session


@app.get('/')
def root():
    return {'message': 'Welcome to the DQMonsters API. Go to the Swagger UI'
                       'interface'
            }


@app.get('/dqm1/monsters', response_model=List[MonsterDetailWithFamily],
         tags=["dqm1 monsters"])
async def read_monsters(
        *, session: Session = Depends(get_session),
        family: Optional[int] = None):
    """
    **Parameter Descriptions** <br>
    **new_name** : updated name used in later Dragon Quest games <br>
    **old_name** : name used in the game <br>
    **description** : in game beastiary description <br>
    **family** : a monster is part of one of 10 different monster families <br>
    """
    monsters = select(MonsterDetail)
    if family:
        monsters = monsters.where(MonsterDetail.family_id == family)
    monsters = session.exec(monsters).all()
    return monsters


@app.get('/dqm1/monsters/{monster_id}', response_model=MonsterDetailWithFamily,
         tags=["dqm1 monsters"])
async def read_monster(
        *, session: Session = Depends(get_session), monster_id: int):

    monster = session.get(MonsterDetail, monster_id)
    if not monster:
        raise HTTPException(status_code=404, detail='Monster not found')
    return monster


@app.get('/dqm1/monstersandskill/{monster_id}',
         response_model=MonsterDetailSkill,tags=["dqm1 monsters"])
async def read_monster(
        *, session: Session = Depends(get_session), monster_id: int):

    monster = session.get(MonsterDetail, monster_id)
    if not monster:
        raise HTTPException(status_code=404, detail='Monster not found')
    return monster


@app.get('/dqm1/family/{family_id}',
         response_model=MonsterFamilyReadWithMonsterDetail,
         tags=["dqm1 monsters"])
async def read_family(
        *, session: Session = Depends(get_session), family_id: int):

    family = session.get(MonsterFamily, family_id)
    if not family:
        raise HTTPException(status_code=404, detail='Family not found')
    return family


@app.get('/dqm1/skills', tags=["dqm1 skills"])
async def read_skills(
        *, session: Session = Depends(get_session),
        category: Optional[SkillCategory] = None,
        skill_family: Optional[SkillFamily] = None):

    skills = select(Skill)
    if category:
        skills = skills.where(Skill.category_type == category)
    if skill_family:
        skills = skills.where(Skill.family_type == skill_family)
    skills = session.exec(skills).all()
    return skills


@app.get('/dqm1/skills/{skill_id}', response_model=SkillUpgradeRead,
         tags=["dqm1 skills"])
async def read_skill(
        *, session: Session = Depends(get_session), skill_id: int):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail='Skill not found')
    return skill


@app.get('/dqm1/skillcombine/{skill_id}',
         response_model=List[SkillCombineRead], tags=["dqm1 skills"])
async def get_skill_combo(
        *, session: Session = Depends(get_session), skill_id: int):
    query = select(SkillCombine).where(SkillCombine.combo_skill_id == skill_id)
    skill = session.exec(query).all()
    return skill


@app.get('/dqm1/items', tags=["dqm1 items"])
async def read_items(
        category: Optional[ItemCategory] = None,
        selllocation: Optional[ItemSellLocation] = None,):
    with Session(engine) as session:
        items = select(Item)
        if category:
            items = items.where(Item.item_category == category)
        if selllocation:
            items = items.where(Item.sell_location == selllocation)
        items = session.exec(items).all()
        return items


@app.get('/dqm1/items/{item_id}', tags=["dqm1 items"])
async def read_item(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail='Item not found')
    return item


@app.get('/dqm1/breeding/{monster_id}',
         response_model=List[MonsterBreedingLinkReadWithInfo],
         tags=["dqm1 monsters"])
async def get_breeding_combos(
        *, session: Session = Depends(get_session), monster_id: int):
    """
    Given a monster_id, finds all breeding combination that results in
    the target monster or uses the target monster as a parent
    """
    query = select(MonsterBreedingLink).where(
        (MonsterBreedingLink.child_id == monster_id)
        | (MonsterBreedingLink.pedigree_id == monster_id)
        | (MonsterBreedingLink.parent2_id == monster_id)
    )
    breeding_combos = session.exec(query).all()
    return breeding_combos
