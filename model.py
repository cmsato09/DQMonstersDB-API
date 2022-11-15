from enum import Enum
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class MonsterSkillLink(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monster_id: Optional[int] = Field(
        default=None, foreign_key='monsterdetail.id',
    )
    skill_id: Optional[int] = Field(
        default=None, foreign_key='skill.id',
    )


class MonsterBreedingLink(SQLModel, table=True):
    """
    This helped:
    https://github.com/tiangolo/sqlmodel/issues/10#issuecomment-1002835506
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    child_id: Optional[int] = Field(
        default=None, foreign_key="monsterdetail.id"
    )
    child: "MonsterDetail" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "MonsterBreedingLink.child_id==MonsterDetail.id",
            "lazy": "joined"
        }
    )

    pedigree_id: Optional[int] = Field(
        default=None, foreign_key="monsterdetail.id"
    )
    pedigree: "MonsterDetail" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "MonsterBreedingLink.pedigree_id==MonsterDetail.id",
            "lazy": "joined"
        }
    )

    parent2_id: Optional[int] = Field(
        default=None, foreign_key="monsterdetail.id"
    )
    parent2: "MonsterDetail" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "MonsterBreedingLink.parent2_id==MonsterDetail.id",
            "lazy": "joined"
        }
    )

    pedigree_family_id: Optional[int] = Field(
        default=None, foreign_key="monsterfamily.id"
    )
    pedigree_family: "MonsterFamily" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "MonsterBreedingLink.pedigree_family_id"
                           "==MonsterFamily.id",
            "lazy": "joined"
        }
    )

    family2_id: Optional[int] = Field(
        default=None, foreign_key="monsterfamily.id"
    )
    family2: "MonsterFamily" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "MonsterBreedingLink.family2_id==MonsterFamily.id",
            "lazy": "joined"
        }
    )


class MonsterDetailBase(SQLModel):
    new_name: str
    old_name: str
    description: str

    # one-to-many relation. monster in only one family category.
    # many monsters in a family category
    family_id: int = Field(foreign_key='monsterfamily.id')

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


class MonsterFamily(MonsterFamilyBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monsters: List[MonsterDetail] = Relationship(back_populates='family')


class MonsterFamilyRead(MonsterFamilyBase):
    id: int


class MonsterDetailWithFamily(MonsterDetailRead):
    family: Optional[MonsterFamilyRead]
    # skills: Optional['SkillRead']


class MonsterFamilyReadWithMonsterDetail(MonsterFamilyRead):
    monsters: List[MonsterDetailRead] = []


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
    upgrade_to_id: Optional[int] = Field(
        foreign_key='skill.id',  # refers to database table name
        default=None,
        nullable=True
    )
    """
    upgrade_from_id: Optional[int] = Field(
        foreign_key='skill.id',
        default=None,
        nullable=True
    )
    """


class Skill(SkillBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monsters: List[MonsterDetail] = Relationship(
        back_populates='skills', link_model=MonsterSkillLink
    )
    upgrade_to: Optional['Skill'] = Relationship(
        back_populates='stronger_skill',
        #sa_relationship_kwargs=dict(
        #    foreign_keys="[Skill.upgrade_to_id]",
        #    remote_side='Skill.id'  # refers to this Skill table class
        #)
        sa_relationship_kwargs={
            'primaryjoin': 'Skill.upgrade_to_id==Skill.id',
            "lazy": 'joined',
            'remote_side': 'Skill.id',
        }
    )
    """
    upgrade_from: Optional['Skill'] = Relationship(
        back_populates='weaker_skill',
        sa_relationship_kwargs=dict(
            # foreign_keys="[Skill.upgrade_from_id]",
            remote_side='Skill.id'  # refers to this Skill table class
        )
    )
    """
    # self-referential backpopulates to variables
    stronger_skill: List['Skill'] = Relationship(back_populates='upgrade_to')
    # weaker_skill: List['Skill'] = Relationship(back_populates='upgrade_from')


class SkillRead(SkillBase):
    id: int


class SkillReadWithUpgradeSkill(SkillRead):
    uprade_to: Optional[SkillRead]


class SkillReadWithMonster(SkillRead):
    monsters: Optional[MonsterDetailRead]


class MonsterDetailSkill(MonsterDetailRead):
    family: Optional[MonsterFamilyRead]
    skills: List[SkillRead] = []


class SkillCombine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    combo_skill_id: Optional[int] = Field(
        default=None, foreign_key='skill.id'
    )
    combo_skill: Skill = Relationship(
        sa_relationship_kwargs={
            'primaryjoin': 'SkillCombine.combo_skill_id==Skill.id',
            "lazy": 'joined'
        }
    )

    needed_skill_id: Optional[int] = Field(
        default=None, foreign_key='skill.id'
    )
    needed_skill: Skill = Relationship(
        sa_relationship_kwargs={
            'primaryjoin': 'SkillCombine.needed_skill_id==Skill.id',
            "lazy": 'joined'
        }
    )


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    item_name: str
    item_category: str
    item_description: str
    price: Optional[int] = Field(default=None)
    sell_price: Optional[int] = Field(default=None)
    sell_location: str

"""
Start of ENUMERATE Class for Swagger UI dropdown menu
https://fastapi.tiangolo.com/tutorial/path-params/#predefined-values
"""
class ItemCategory(str, Enum):
    """
    Create dropdown menu for read_items() in Swagger UI to filter by
    item_category. Works for predefined choices in item_category.
    For the Item class model
    """
    recovery = "recovery"
    meat = "meat"
    staff = "staff"
    seed = "seed"
    book = "book"
    dungeon_use = "dungeon use"


class ItemSellLocation(str, Enum):
    """
    Create dropdown menu for read_items() in Swagger UI to filter by
    sell_location. For Item class model
    """
    bazzar_shop_1 = "Bazaar shop 1"
    bazzar_shop_2 = "Bazaar shop 2"
    bazzar_shop_3 = "Bazaar shop 3"
    bazzar_shop_4 = "Bazaar shop 4"
    field_shop = "Field shop"
    found_in_field = "found in field"


class SkillCategory(str, Enum):
    """
    Create dropdown menu for read_skills() in Swagger UI to filter by
    category_type. Works for predefined choices in the Skill model class
    """
    attack = "Attack"
    support = "Support"
    recovery = "Recovery"


class SkillFamily(str, Enum):
    """
    Create dropdown menu for read_skills() in Swagger UI to filter by
    family_type. Works for predefined choices in the Skill model class
    """
    frizz = "Frizz"
    sizz = "Sizz"
    bang = "Bang"
    woosh = "Woosh"
    zap = "Zap"
    crack = "Crack"
    whack = "Whack"
    kamikazee = "Kamikazee"
    magic_burst = "Magic Burst"
    help = "Help"
    fire = "Fire"
    ice = "Ice"
    poison = "Poison"
    paralyze = "Paralyze"
    sleep = "Sleep"
    gigaslash = "Gigaslash"
    attack = "Attack"
    dazzle = "Dazzle"
    drain_magic = "Drain Magic"
    fuddle = "Fuddle"
    sap = "Sap"
    curse = "Curse"
    decelerate = "Decelerate"
    ban_dance = "Ban Dance"
    gobstop = "Gobstop"
    lose_turn = "Lose a turn"
    defense = "Defense"
    status_support = "Status support"
    summon = "Summon"
    heal = "Heal"
    status_recovery = "Status recovery"
    revive = "Revive"
    map = "Map"
