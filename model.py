from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class MonsterSkillLink(SQLModel, table=True):
    """
    many-to-many association table linking a monster to three different skills.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    monster_id: Optional[int] = Field(
        default=None, foreign_key='monsterdetail.id',
    )
    skill_id: Optional[int] = Field(
        default=None, foreign_key='skill.id',
    )


class MonsterDetailBase(SQLModel):
    new_name: str
    old_name: str
    description: str

    # one-to-many relation where a family is linked to many monsters
    family_id: int = Field(foreign_key='monsterfamily.id')


class MonsterDetail(MonsterDetailBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    family: List['MonsterFamily'] = Relationship(back_populates='monsters')
    skills: List['Skill'] = Relationship(
        back_populates='monsters', link_model=MonsterSkillLink
    )


class MonsterDetailRead(MonsterDetailBase):
    id: int


class MonsterFamilyBase(SQLModel):
    family_eng: str


class MonsterFamily(MonsterFamilyBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monsters: List[MonsterDetail] = Relationship(back_populates='family')


class MonsterFamilyRead(MonsterFamilyBase):
    id: int


class MonsterDetailWithFamily(MonsterDetailRead):
    family: Optional[MonsterFamilyRead]


class MonsterFamilyReadWithMonsterDetail(MonsterFamilyRead):
    monsters: List[MonsterDetailRead] = []


class MonsterBreedingLinkBase(SQLModel):
    """TODO: move stuff from MonsterBreedingLink here"""
    child_id: Optional[int] = Field(
        default=None, foreign_key='monsterdetail.id'
    )
    pedigree_id: Optional[int] = Field(
        default=None, foreign_key='monsterdetail.id'
    )
    parent2_id: Optional[int] = Field(
        default=None, foreign_key='monsterdetail.id'
    )
    pedigree_family_id: Optional[int] = Field(
        default=None, foreign_key='monsterfamily.id'
    )
    family2_id: Optional[int] = Field(
        default=None, foreign_key='monsterfamily.id'
    )


class MonsterBreedingLink(MonsterBreedingLinkBase, table=True):
    """
    This helped:
    https://github.com/tiangolo/sqlmodel/issues/10#issuecomment-1002835506
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    child: 'MonsterDetail' = Relationship(
        sa_relationship_kwargs={
            'primaryjoin': 'MonsterBreedingLink.child_id==MonsterDetail.id',
            'lazy': 'joined'
        }
    )
    pedigree: 'MonsterDetail' = Relationship(
        sa_relationship_kwargs={
            'primaryjoin': 'MonsterBreedingLink.pedigree_id==MonsterDetail.id',
            'lazy': 'joined'
        }
    )
    parent2: 'MonsterDetail' = Relationship(
        sa_relationship_kwargs={
            'primaryjoin': 'MonsterBreedingLink.parent2_id==MonsterDetail.id',
            'lazy': 'joined'
        }
    )
    pedigree_family: 'MonsterFamily' = Relationship(
        sa_relationship_kwargs={
            'primaryjoin': 'MonsterBreedingLink.pedigree_family_id'
                           '==MonsterFamily.id',
            'lazy': 'joined'
        }
    )
    family2: 'MonsterFamily' = Relationship(
        sa_relationship_kwargs={
            'primaryjoin': 'MonsterBreedingLink.family2_id==MonsterFamily.id',
            'lazy': 'joined'
        }
    )


class MonsterBreedingLinkRead(MonsterBreedingLinkBase):
    id: int


class MonsterBreedingLinkReadWithParentsAndFamilies(MonsterBreedingLinkRead):
    pedigree: Optional[MonsterDetailRead]
    parent2: Optional[MonsterDetailRead]
    pedigree_family: Optional[MonsterFamilyRead]
    family2: Optional[MonsterFamilyRead]


class SkillBase(SQLModel):
    category_type: str
    family_type: str
    new_name: Optional[str] = Field(default=None)
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


class Skill(SkillBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    upgrade_to_id: Optional[int] = Field(
        foreign_key='skill.id',  # lowercase refers to database table name
        default=None,
    )
    upgrade_to: Optional['Skill'] = Relationship(
        sa_relationship_kwargs={
            'primaryjoin': 'Skill.upgrade_to_id==Skill.id',
            'lazy': 'joined',
            'remote_side': 'Skill.id'  # uppercase refers to this Skill class
        }
    )

    upgrade_from_id: Optional[int] = Field(
        foreign_key='skill.id', default=None,
    )
    upgrade_from: Optional['Skill'] = Relationship(
        sa_relationship_kwargs={
            'primaryjoin': 'Skill.upgrade_from_id==Skill.id',
            'lazy': 'joined',
            'remote_side': 'Skill.id'
        }
    )

    monsters: List[MonsterDetail] = Relationship(
        back_populates='skills', link_model=MonsterSkillLink
    )


class SkillRead(SkillBase):
    id: int


class SkillUpgradeRead(SkillRead):
    upgrade_to: Optional[Skill]
    upgrade_from: Optional[Skill]


class SkillReadWithMonster(SkillRead):
    monsters: Optional[MonsterDetailRead]


class MonsterDetailSkill(MonsterDetailRead):
    family: Optional[MonsterFamilyRead]
    skills: List[SkillRead] = []


class SkillCombineBase(SQLModel):
    combo_skill_id: Optional[int] = Field(
        default=None, foreign_key='skill.id'
    )
    needed_skill_id: Optional[int] = Field(
        default=None, foreign_key='skill.id'
    )


class SkillCombine(SkillCombineBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    combo_skill: Skill = Relationship(
        sa_relationship_kwargs={
            'primaryjoin': 'SkillCombine.combo_skill_id==Skill.id',
            'lazy': 'joined'
        }
    )

    needed_skill: Skill = Relationship(
        sa_relationship_kwargs={
            'primaryjoin': 'SkillCombine.needed_skill_id==Skill.id',
            'lazy': 'joined'
        }
    )


class SkillCombineRead(SkillCombineBase):
    id: int
    needed_skill: Optional[SkillRead]


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_name: str
    item_category: str
    item_description: str
    price: Optional[int] = Field(default=None)
    sell_price: Optional[int] = Field(default=None)
    sell_location: str
