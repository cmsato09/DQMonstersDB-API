from typing import Optional

from sqlmodel import Field, SQLModel


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
