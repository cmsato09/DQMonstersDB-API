from typing import List, Optional

from .monster import MonsterBreedingLinkBase, MonsterDetailBase
from .monster_family import MonsterFamilyBase
from .skill import Skill, SkillBase, SkillCombineBase


class MonsterFamilyRead(MonsterFamilyBase):
    id: int


class MonsterFamilyReadWithMonsterDetail(MonsterFamilyRead):
    monsters: List["MonsterDetailRead"] = []


class MonsterDetailRead(MonsterDetailBase):
    id: int


class MonsterDetailWithFamily(MonsterDetailRead):
    family: Optional[MonsterFamilyRead] = None


class MonsterBreedingLinkRead(MonsterBreedingLinkBase):
    id: int


class MonsterBreedingLinkReadWithInfo(MonsterBreedingLinkRead):
    child: Optional[MonsterDetailRead]
    pedigree: Optional[MonsterDetailRead]
    parent2: Optional[MonsterDetailRead]
    pedigree_family: Optional[MonsterFamilyRead]
    family2: Optional[MonsterFamilyRead]


class SkillRead(SkillBase):
    id: int


class SkillReadWithMonster(SkillRead):
    monsters: Optional[MonsterDetailRead]


class SkillUpgradeRead(SkillRead):
    upgrade_to: Optional[Skill]
    upgrade_from: Optional[Skill]


class MonsterDetailSkill(MonsterDetailWithFamily):
    skills: List[SkillRead] = []


class SkillCombineRead(SkillCombineBase):
    id: int
    needed_skill: Optional[SkillRead]
