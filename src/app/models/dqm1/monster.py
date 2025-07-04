from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .skill import Skill
    from .monster_family import MonsterFamily, MonsterFamilyRead


class MonsterSkillLink(SQLModel, table=True):
    """
    many-to-many association table linking a monster to three different skills.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    monster_id: Optional[int] = Field(
        default=None,
        foreign_key="monsterdetail.id",
    )
    skill_id: Optional[int] = Field(
        default=None,
        foreign_key="skill.id",
    )


class MonsterDetailBase(SQLModel):
    """
    Monster details from in-game bestiary. Shows name, family, and description.
    """

    new_name: str
    old_name: str
    description: str

    # one-to-many relation where a family is linked to many monsters
    family_id: int = Field(foreign_key="monsterfamily.id")


class MonsterDetail(MonsterDetailBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    family: List["MonsterFamily"] = Relationship(back_populates="monsters")
    skills: List["Skill"] = Relationship(
        back_populates="monsters", link_model=MonsterSkillLink
    )


class MonsterDetailRead(MonsterDetailBase):
    id: int


class MonsterDetailWithFamily(MonsterDetailRead):
    family: Optional[MonsterFamilyRead]


class MonsterBreedingLinkBase(SQLModel):
    child_id: Optional[int] = Field(default=None, foreign_key="monsterdetail.id")
    pedigree_id: Optional[int] = Field(default=None, foreign_key="monsterdetail.id")
    parent2_id: Optional[int] = Field(default=None, foreign_key="monsterdetail.id")
    pedigree_family_id: Optional[int] = Field(
        default=None, foreign_key="monsterfamily.id"
    )
    family2_id: Optional[int] = Field(default=None, foreign_key="monsterfamily.id")


class MonsterBreedingLink(MonsterBreedingLinkBase, table=True):
    """
    many-to-many association table between MonsterDetail and MonsterFamily
    that represents breeding combinations.

    child_id, pedigree, and parent_2 represent individual monster ids.
    pedigree_family and family_2 represent family type.

    In order to make new monster, two parents are required.

    4 different combinations possible:
    pedigree + parent_2  -- specific monster + specific monster
    pedigree + family_2 -- specific monster + any monster from the family type
    pedigree_family + parent_2 -- specific family type + specific monster
    pedigree_family + family_2 -- family + different family type
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    child: "MonsterDetail" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "MonsterBreedingLink.child_id==MonsterDetail.id",
            "lazy": "joined",
        }
    )
    pedigree: "MonsterDetail" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "MonsterBreedingLink.pedigree_id==MonsterDetail.id",
            "lazy": "joined",
        }
    )
    parent2: "MonsterDetail" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "MonsterBreedingLink.parent2_id==MonsterDetail.id",
            "lazy": "joined",
        }
    )
    pedigree_family: "MonsterFamily" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "MonsterBreedingLink.pedigree_family_id"
            "==MonsterFamily.id",
            "lazy": "joined",
        }
    )
    family2: "MonsterFamily" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "MonsterBreedingLink.family2_id==MonsterFamily.id",
            "lazy": "joined",
        }
    )


class MonsterBreedingLinkRead(MonsterBreedingLinkBase):
    id: int


class MonsterBreedingLinkReadWithInfo(MonsterBreedingLinkRead):
    child: Optional[MonsterDetailRead]
    pedigree: Optional[MonsterDetailRead]
    parent2: Optional[MonsterDetailRead]
    pedigree_family: Optional[MonsterFamilyRead]
    family2: Optional[MonsterFamilyRead]
