from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class MonsterSkillLink(SQLModel, table=True):
    monster_id: Optional[int] = Field(
        foreign_key='monsterdetail.id', primary_key=True
    )
    skill_id: Optional[int] = Field(
        default=None, foreign_key='skill.id', primary_key=True
    )


# class MonsterBreedingLink(SQLModel, table=True):
#     child_id: Optional[int] = Field(
#         foreign_key='monsterdetail.id', primary_key=True
#     )
#     pedigree: Optional[int] = Field(
#         foreign_key='monsterdetail.id', primary_key=True
#     )
#     parent_2: Optional[int] = Field(
#         foreign_key='monsterdetail.id', primary_key=True
#     )
#     pedigree_family: Optional[int] = Field(
#         foreign_key='monsterfamily.id', primary_key=True
#     )
#     family_2: Optional[int] = Field(
#         foreign_key='monsterfamily.id', primary_key=True
#     )


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

    # monster_child: List['MonsterDetail'] = Relationship(
    #     link_model=MonsterBreedingLink
    # )
    # monster_pedigree: List['MonsterDetail'] = Relationship(
    #     link_model=MonsterBreedingLink
    # )
    # monster_parent2: List['MonsterDetail'] = Relationship(
    #     link_model=MonsterBreedingLink
    # )


class MonsterFamily(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    family_eng: str

    # pedigree_family: List['pedigree_family'] = Relationship(
    #     link_model=MonsterBreedingLink
    # )
    # family_2: List['family_2'] = Relationship(
    #     link_model=MonsterBreedingLink
    # )


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

