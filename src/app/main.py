from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from src.app.database import get_session
from src.app.model_enums import (
    ItemCategory,
    ItemSellLocation,
)
from src.app.models import (
    Item,
    MonsterBreedingLink,
    MonsterBreedingLinkReadWithInfo,
)
from src.app.routers import dqm1_endpoints

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
    openapi_tags=tags_metadata,
)
app.mount("/static", StaticFiles(directory="src/static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://dqmonsters-db.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(dqm1_endpoints.router)


@app.get("/")
def root():
    return {
        "message": ("Welcome to the DQMonsters API. " "Go to the Swagger UI interface")
    }


@app.get("/dqm1/items", tags=["dqm1 items"])
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


@app.get("/dqm1/items/{item_id}", tags=["dqm1 items"])
async def read_item(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get(
    "/dqm1/breeding/{monster_id}",
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
