from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.app.database import get_session
from src.app.model_enums import (
    SkillCategory,
    SkillFamily,
)
from src.app.models import (
    MonsterDetail,
    MonsterDetailWithFamily,
    MonsterDetailSkill,
    MonsterFamily,
    MonsterFamilyReadWithMonsterDetail,
    Skill,
)

router = APIRouter(
    prefix="/dqm1",
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


@router.get("/dqm1/skills", tags=["dqm1 skills"])
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
