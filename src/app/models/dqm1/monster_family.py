from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .monster import MonsterDetail


class MonsterFamilyBase(SQLModel):
    """
    There are 10 monster families in the game.
    """

    family_eng: str


class MonsterFamily(MonsterFamilyBase, table=True):
    """
    one-to-many relation between family and monsters.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    monsters: List["MonsterDetail"] = Relationship(back_populates="family")
