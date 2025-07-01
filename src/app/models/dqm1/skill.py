from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel
from .monster import (
    MonsterDetail,
    MonsterSkillLink,
    MonsterDetailRead,
    MonsterDetailWithFamily,
)

if TYPE_CHECKING:
    from .monster import (
        MonsterDetail,
        MonsterSkillLink,
        MonsterDetailRead,
        MonsterDetailWithFamily,
    )


class SkillBase(SQLModel):
    """
    Shows description, MP cost, and required stats to learn skill.
    Each monster naturally learns 3 skills.
    """

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
        foreign_key="skill.id",  # lowercase refers to database table name
        default=None,
    )
    upgrade_to: Optional["Skill"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Skill.upgrade_to_id==Skill.id",
            "lazy": "joined",
            "remote_side": "Skill.id",  # uppercase refers to this Skill class
        }
    )

    upgrade_from_id: Optional[int] = Field(
        foreign_key="skill.id",
        default=None,
    )
    upgrade_from: Optional["Skill"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Skill.upgrade_from_id==Skill.id",
            "lazy": "joined",
            "remote_side": "Skill.id",
        }
    )

    monsters: List["MonsterDetail"] = Relationship(
        back_populates="skills", link_model=MonsterSkillLink
    )


class SkillRead(SkillBase):
    id: int


class SkillReadWithMonster(SkillRead):
    monsters: Optional[MonsterDetailRead]


class SkillUpgradeRead(SkillRead):
    upgrade_to: Optional[Skill]
    upgrade_from: Optional[Skill]


class MonsterDetailSkill(MonsterDetailWithFamily):
    skills: List[SkillRead] = []


class SkillCombineBase(SQLModel):
    combo_skill_id: Optional[int] = Field(default=None, foreign_key="skill.id")
    needed_skill_id: Optional[int] = Field(default=None, foreign_key="skill.id")


class SkillCombine(SkillCombineBase, table=True):
    """
    many-to-many association table showing certain needed skills combine to
    learn new combo skill.
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    combo_skill: Skill = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "SkillCombine.combo_skill_id==Skill.id",
            "lazy": "joined",
        }
    )

    needed_skill: Skill = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "SkillCombine.needed_skill_id==Skill.id",
            "lazy": "joined",
        }
    )


class SkillCombineRead(SkillCombineBase):
    id: int
    needed_skill: Optional[SkillRead]
