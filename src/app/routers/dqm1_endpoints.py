from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.app.database import get_session
from src.app.models import (
    MonsterDetail,
    MonsterDetailWithFamily,
    MonsterDetailSkill,
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
