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
#     child_id: int = Field(
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
    required_hp: Optional[int] = None
    required_mp: Optional[int] = None
    required_attack: Optional[int] = None
    required_defense: Optional[int] = None
    required_speed: Optional[int] = None
    required_intelligence: Optional[int] = None

    upgrade: Optional[int] = Field(  # works for now
        foreign_key='skill.id', default=None,
    )

    monsters: List[MonsterDetail] = Relationship(
        back_populates='skills', link_model=MonsterSkillLink
    )


class SkillCombine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    combo_skill_id: Optional[int] = Field(default=None, foreign_key='skill.id')
    combo_skill: Skill = Relationship(
        sa_relationship_kwargs={'primaryjoin': 'SkillCombine.combo_skill_id==Skill.id', "lazy": 'joined'}
    )

    needed_skill_id: Optional[int] = Field(default=None, foreign_key='skill.id')
    needed_skill: Skill = Relationship(
        sa_relationship_kwargs={'primaryjoin': 'SkillCombine.needed_skill_id==Skill.id', "lazy": 'joined'}
    )


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_name: str
    item_category: str
    item_description: str
    price: int
    sell_price: int
    sell_location: str

