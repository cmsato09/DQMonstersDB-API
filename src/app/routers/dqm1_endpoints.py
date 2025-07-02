from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.app.database import get_session
from src.app.model_enums import (
    ItemCategory,
    ItemSellLocation,
    SkillCategory,
    SkillFamily,
)
from src.app.models.dqm1.item import Item
from src.app.models.dqm1.monster import (
    MonsterBreedingLink,
    MonsterBreedingLinkReadWithInfo,
    MonsterDetail,
    MonsterDetailWithFamily,
    MonsterFamily,
    MonsterFamilyReadWithMonsterDetail,
)
from src.app.models.dqm1.skill import (
    MonsterDetailSkill,
    Skill,
    SkillCombine,
    SkillCombineRead,
    SkillUpgradeRead,
)

router = APIRouter(
    prefix="/dqm1",
)


@router.get(
    "/monsters",
    response_model=List[MonsterDetailWithFamily],
    tags=["dqm1 monsters"],
)
async def read_monsters(
    *, session: Session = Depends(get_session), family: Optional[int] = None
):
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
    monsters_result = session.exec(monsters).all()
    return monsters_result


@router.get(
    "/monsters/{monster_id}",
    response_model=MonsterDetailWithFamily,
    tags=["dqm1 monsters"],
)
async def read_monster(*, session: Session = Depends(get_session), monster_id: int):
    monster = session.get(MonsterDetail, monster_id)
    if not monster:
        raise HTTPException(status_code=404, detail="Monster not found")
    return monster


@router.get(
    "/monstersandskill/{monster_id}",
    response_model=MonsterDetailSkill,
    tags=["dqm1 monsters"],
)
async def read_monster_skill(
    *, session: Session = Depends(get_session), monster_id: int
):
    monster = session.get(MonsterDetail, monster_id)
    if not monster:
        raise HTTPException(status_code=404, detail="Monster not found")
    return monster


@router.get(
    "/family/{family_id}",
    response_model=MonsterFamilyReadWithMonsterDetail,
    tags=["dqm1 monsters"],
)
async def read_family(*, session: Session = Depends(get_session), family_id: int):
    family = session.get(MonsterFamily, family_id)
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    return family


@router.get("/skills", tags=["dqm1 skills"])
async def read_skills(
    *,
    session: Session = Depends(get_session),
    category: Optional[SkillCategory] = None,
    skill_family: Optional[SkillFamily] = None,
):
    skills = select(Skill)
    if category:
        skills = skills.where(Skill.category_type == category)
    if skill_family:
        skills = skills.where(Skill.family_type == skill_family)
    skills_result = session.exec(skills).all()
    return skills_result


@router.get("/skills/{skill_id}", response_model=SkillUpgradeRead, tags=["dqm1 skills"])
async def read_skill(*, session: Session = Depends(get_session), skill_id: int):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.get(
    "/skillcombine/{skill_id}",
    response_model=List[SkillCombineRead],
    tags=["dqm1 skills"],
)
async def get_skill_combo(*, session: Session = Depends(get_session), skill_id: int):
    query = select(SkillCombine).where(SkillCombine.combo_skill_id == skill_id)
    skill = session.exec(query).all()
    return skill


@router.get("/items", tags=["dqm1 items"])
async def read_items(
    *,
    session: Session = Depends(get_session),
    category: Optional[ItemCategory] = None,
    selllocation: Optional[ItemSellLocation] = None,
):
    items = select(Item)
    if category:
        items = items.where(Item.item_category == category)
    if selllocation:
        items = items.where(Item.sell_location == selllocation)
    items_result = session.exec(items).all()
    return items_result


@router.get("/items/{item_id}", tags=["dqm1 items"])
async def read_item(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get(
    "/breeding/{monster_id}",
    response_model=List[MonsterBreedingLinkReadWithInfo],
    tags=["dqm1 monsters"],
)
async def get_breeding_combos(
    *, session: Session = Depends(get_session), monster_id: int
):
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
