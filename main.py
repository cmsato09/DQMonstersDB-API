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
    """Creates a database session and yields it for use in API routes."""
    with Session(engine) as session:
        yield session


@app.get('/')
def root():
    """Default route for the API, returns a welcome message."""
    return {'message': 'Welcome to the DQMonsters API. Go to the Swagger UI'
                       'interface'
            }


@app.get('/dqm1/monsters', response_model=List[MonsterDetailWithFamily],
         tags=["dqm1 monsters"])
async def read_monsters(
        *, session: Session = Depends(get_session),
        family: Optional[int] = None):
    """
    Retrieves a list of monsters with optional filtering by family.

    Args:
        session (Session): The database session.
        family (int, optional): Filter list by monster family ID.

    Returns:
        List[MonsterDetailWithFamily]: List of dicts of monster information.
        For example:
        [
            {
                "new_name": "Drake Slime",
                "old_name": "DrakSlime",
                "description": "Moves & jumps with its tail and wings",
                "family_id": 1,
                "id": 1,
                "family": {
                    "family_eng": "SLIME",
                    "id": 1
                }
            },
            ...
        ]
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
    """
    Endpoint returns detailed info of a specific monster based on unique ID.
    Monster details include its name, description, and family.

    Args:
        session (Session): The database session.
        monster_id (int): Filter by monster ID

    Returns:
        MonsterDetailWithFamily: A dict of monster information.

    Raises:
        HTTPException: If the provided monster_id does not correspond to any
        existing monster, a 404 HTTP exception is raised.
    """

    monster = session.get(MonsterDetail, monster_id)
    if not monster:
        raise HTTPException(status_code=404, detail='Monster not found')
    return monster


@app.get('/dqm1/monstersandskill/{monster_id}',
         response_model=MonsterDetailSkill,tags=["dqm1 monsters"])
async def read_monster(
        *, session: Session = Depends(get_session), monster_id: int):
    """
    Endpoint returns detailed info of a specific monster based on unique ID.
    Monster details include its name, description, family, and skills.

    Args:
        session (Session): The database session.
        monster_id (int, optional): Filter by monster ID

    Returns:
        MonsterDetailWithSkill: Dictionary of monster info with associated 
          family and skills info as dicts
    
    Raises:
        HTTPException: If monster_id does not exist, a 404 HTTP exception is 
        raised.
    """

    monster = session.get(MonsterDetail, monster_id)
    if not monster:
        raise HTTPException(status_code=404, detail='Monster not found')
    return monster


@app.get('/dqm1/family/{family_id}',
         response_model=MonsterFamilyReadWithMonsterDetail,
         tags=["dqm1 monsters"])
async def read_family(
        *, session: Session = Depends(get_session), family_id: int):
    """
    Endpoint returns list of monster of specific family type. 

    Args:
        session (Session): The database session.
        family_id (int): Filter all monsters by associated family ID

    Returns:
        MonsterFamilyReadwithMonsterDetail: List of dicts of all monsters of
          selected family
    
    Raises:
        HTTPException: If family_id does not exist, a 404 HTTP exception is 
        raised.
    """

    family = session.get(MonsterFamily, family_id)
    if not family:
        raise HTTPException(status_code=404, detail='Family not found')
    return family


@app.get('/dqm1/skills', tags=["dqm1 skills"])
async def read_skills(
        *, session: Session = Depends(get_session),
        category: Optional[SkillCategory] = None,
        skill_family: Optional[SkillFamily] = None):
    """
    Endpoint returns list of monster skills with optional filtering by category 
    and skill_family.

    Args:
        session (Session): The database session.
        category: optional filtering using predefined strings
        skill_family: optional filtering using predefined strings

    Returns:
        List[Skill]: List of dicts of filtered skill information
    """

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
    """
    Endpoint returns detailed information of specific skill.
    Skill details include name, type, description, required stats, etc.

    Args:
        session (Session): The database session.
        skill_id: Search by skill ID

    Returns:
        SkillUpgradeRead: Skill information as a dict.
    
    Raises:
        HTTPException: If skill_id does not exist, a 404 HTTP exception is 
        raised.
    """

    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail='Skill not found')
    return skill


@app.get('/dqm1/skillcombine/{skill_id}',
         response_model=List[SkillCombineRead], tags=["dqm1 skills"])
async def get_skill_combo(
        *, session: Session = Depends(get_session), skill_id: int):
    """
    Endpoint returns detailed information of specific skills needed to learn a 
    higher level skill.
    
    Args:
        session (Session): The database session.
        skill_id: Search by skill ID

    Returns:
        List[SkillCombineRead]: Skill information as a list of dicts.
    """

    query = select(SkillCombine).where(SkillCombine.combo_skill_id == skill_id)
    skill = session.exec(query).all()
    return skill


@app.get('/dqm1/items', tags=["dqm1 items"])
async def read_items(
        category: Optional[ItemCategory] = None,
        selllocation: Optional[ItemSellLocation] = None,):
    """
    Endpoint returns detailed info of items.
    Item details include its name, description, price, sell price, and sell 
    location.

    Args:
        category: optional filtering using predefined strings
        selllocation: optional filtering using predefined strings

    Returns:
        List[Item]: A list of item information.
    """

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
    """
    Endpoint returns detailed info of a specific item based on unique ID.

    Args:
        session (Session): The database session.
        item_id (int, optional): Filter by item ID

    Returns:
        Item: Dictionary of item info
    
    Raises:
        HTTPException: If item_id does not exist, a 404 HTTP exception is 
        raised.
    """

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
    Endpoint returns detailed breeding info of a specific monster based on 
    unique ID.
    Finds all breeding combinations that results in the target monster or uses the target monster as a parent.

    Args:
        session (Session): The database session.
        monster_id (int): Search combinations by monster ID

    Returns:
        List[MonsterBreedingLinkReadWithInfo: A list of dicts of monster 
        information.
    """

    query = select(MonsterBreedingLink).where(
        (MonsterBreedingLink.child_id == monster_id)
        | (MonsterBreedingLink.pedigree_id == monster_id)
        | (MonsterBreedingLink.parent2_id == monster_id)
    )
    breeding_combos = session.exec(query).all()
    return breeding_combos
