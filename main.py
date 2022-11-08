from typing import Optional, Union, List

from fastapi import Depends, FastAPI, HTTPException
from model import Item, MonsterDetail, MonsterBreedingLink, Skill, \
    MonsterFamily, MonsterDetailRead, MonsterDetailWithFamily, \
    MonsterFamilyReadWithMonsterDetail
from database import engine
from sqlmodel import Session, select

app = FastAPI()


def get_session():  # place in database.py?
    with Session(engine) as session:
        yield session


@app.get("/")
def root():
    return {"message": "Hello World!!"}

# for some reason, can't add "response_model=List[MonsterDetailRead]" to
# decorator without getting an internal server error
@app.get("/dqm1/monsters")
def read_monsters(*, session: Session = Depends(get_session),
                  family: Union[int, None] = None):
    monsters = select(MonsterDetail, MonsterFamily).join(MonsterFamily)
    if family:
        monsters = monsters.where(MonsterDetail.family_id == family)
    monsters = session.exec(monsters).all()
    return monsters


@app.get("/dqm1/monsters/{monster_id}", response_model=MonsterDetailWithFamily)
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
def read_skills(*, session: Session = Depends(get_session)):
    skills = session.exec(select(Skill)).all()
    return skills


@app.get("/dqm1/skills/{skill_id}")
def read_skill(*, session: Session = Depends(get_session), skill_id: int):
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
def read_skill(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
