from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class MonsterSkillLink(SQLModel, table=True):
    monster_id: Optional[int] = Field(
        foreign_key='monsterdetail.id', primary_key=True
    )
    skill_id: Optional[int] = Field(
        default=None, foreign_key='skill.id', primary_key=True
    )


class MonsterBreedingLink(SQLModel, table=True):
    """
    This helped:
    https://github.com/tiangolo/sqlmodel/issues/10#issuecomment-1002835506
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    child_id: Optional[int] = Field(default=None, foreign_key="monsterdetail.id")
    child: "MonsterDetail" = Relationship(
        sa_relationship_kwargs={"primaryjoin": "MonsterBreedingLink.child_id==MonsterDetail.id", "lazy": "joined"}
    )
    pedigree_id: Optional[int] = Field(default=None, foreign_key="monsterdetail.id")
    pedigree: "MonsterDetail" = Relationship(
        sa_relationship_kwargs={"primaryjoin": "MonsterBreedingLink.pedigree_id==MonsterDetail.id", "lazy": "joined"}
    )
    parent2_id: Optional[int] = Field(default=None, foreign_key="monsterdetail.id")
    parent2: "MonsterDetail" = Relationship(
        sa_relationship_kwargs={"primaryjoin": "MonsterBreedingLink.parent2_id==MonsterDetail.id", "lazy": "joined"}
    )
    pedigree_family_id: Optional[int] = Field(default=None, foreign_key="monsterfamily.id")
    pedigree_family: "MonsterFamily" = Relationship(
        sa_relationship_kwargs={"primaryjoin": "MonsterBreedingLink.pedigree_family_id==MonsterFamily.id", "lazy": "joined"}
    )
    family2_id: Optional[int] = Field(default=None, foreign_key="monsterfamily.id")
    family2: "MonsterFamily" = Relationship(
        sa_relationship_kwargs={"primaryjoin": "MonsterBreedingLink.family2_id==MonsterFamily.id", "lazy": "joined"}
    )


class MonsterDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    new_name: str
    old_name: str
    description: str

    # one-to-many relation. monster in only one family category.
    # many monsters in a family category
    family_id: int = Field(foreign_key='monsterfamily.id')
    skills: List['Skill'] = Relationship(
        back_populates='monsters', link_model=MonsterSkillLink
    )

    """
    children: List['MonsterFamily'] = Relationship(
        back_populates="families",
        link_model=MonsterBreedingLink
    )
    pedigrees: List['MonsterFamily'] = Relationship(
        back_populates="pedigree_families",
        link_model=MonsterBreedingLink
    )
    monster_parents: List['MonsterFamily'] = Relationship(
        back_populates="secondary_families",
        link_model=MonsterBreedingLink
    )
    """


class MonsterFamily(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    family_eng: str

    """
    families: List[MonsterDetail] = Relationship(
        back_populates="children",
        link_model=MonsterBreedingLink
    )
    pedigree_families: List[MonsterDetail] = Relationship(
        back_populates="pedigrees",
        link_model=MonsterBreedingLink
    )
    secondary_families: List[MonsterDetail] = Relationship(
        back_populates="monster_parents",
        link_model=MonsterBreedingLink
    )
    """


class Skill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category_type: str
    family_type: str
    new_name: str
    old_name: str
    description: str
    mp_cost: int
    required_level: int
    required_hp: Optional[int]
    required_mp: Optional[int]
    required_attack: Optional[int]
    required_defense: Optional[int]
    required_speed: Optional[int]
    required_intelligence: Optional[int]

    # upgrade: Optional[int] = Field(
    #     foreign_key='skill.id', default=None,
    # )
    # combine: Easier to make intermediate table? only a couple of skills have
    # two or more combinations
    # TODO: can try this: https://github.com/tiangolo/sqlmodel/issues/89

    monsters: List[MonsterDetail] = Relationship(
        back_populates='skills', link_model=MonsterSkillLink
    )


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_name: str
    item_category: str
    item_description: str
    price: int
    sell_price: int
    sell_location: str

