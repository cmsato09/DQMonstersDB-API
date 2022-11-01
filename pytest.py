import unittest

from database import create_db_and_tables, engine
from sqlmodel import Session

from model import Item, MonsterFamily, MonsterDetail, Skill, MonsterSkillLink,\
    MonsterBreedingLink, SkillCombine


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


def create_items():
    item_1 = Item(
        item_name='Herb', item_category='Recovery',
        item_description='Restores around 30 HP', price=10, sell_price=6,
        sell_location='Bazaar shop 1'
    )
    item_2 = Item(
        item_name='Lovewater', item_category='Recovery',
        item_description='Restores around 70 HP', price=80, sell_price=60,
        sell_location='Bazaar shop 1'
    )
    item_3 = Item(
        item_name='Antidote', item_category='recovery',
        item_description='Cures poison of one ally', price=10,
        sell_price=8,
        sell_location='Bazaar shop 1'
    )
    item_4 = Item(
        item_name='Repellent', item_category='dungeon use',
        item_description='Reduces monster encounters', price=200,
        sell_price=150, sell_location='Bazaar shop 1'
    )
    item_5 = Item(
        item_name='BeefJerky', item_category='meat',
        item_description="Give to monster to tame during battle or reduce "
                         "your own monster's WLD (wildness) by 5",
        price=200, sell_price=150, sell_location='Bazaar shop 1'
    )
    test_items = [item_1, item_2, item_3, item_4, item_5]
    session = Session(engine)

    for item in test_items:
        session.add(item)

    session.commit()


def create_monster_family():
    family_1 = MonsterFamily(family_eng='SLIME')
    family_2 = MonsterFamily(family_eng='DRAGON')
    family_3 = MonsterFamily(family_eng='BEAST')
    family_4 = MonsterFamily(family_eng='BIRD')
    family_5 = MonsterFamily(family_eng='PLANT')
    family_6 = MonsterFamily(family_eng='BUG')
    family_7 = MonsterFamily(family_eng='DEVIL')
    family_8 = MonsterFamily(family_eng='UNDEAD')
    family_9 = MonsterFamily(family_eng='MATERIAL')
    family_10 = MonsterFamily(family_eng='???')

    test_families = [family_1, family_2, family_3, family_4, family_5,
                     family_6, family_7, family_8, family_9, family_10]
    with Session(engine) as session:
        for family in test_families:
            session.add(family)

        session.commit()

    return [family_1, family_2, family_3, family_4, family_5,
            family_6, family_7, family_8, family_9, family_10]


def create_skill():
    skill_1 = Skill(
        category_type='Attack', family_type='Frizz', new_name='Frizz',
        old_name='Blaze', description='Inflict damage with small fireball ',
        mp_cost=2, required_level=2, required_mp=7, required_intelligence=20
    )
    skill_2 = Skill(
        category_type='Attack', family_type='Frizz', new_name='Frizzle',
        old_name='Blazemore', description='Inflict damage with giant fireball',
        mp_cost=4, required_level=14, required_mp=46, required_intelligence=64,
        upgrade=1  # added foreign key ID and value adds to table w/out problem
    )
    skill_3 = Skill(
        category_type='Attack', family_type='Frizz', new_name='Kafrizzle',
        old_name='Blazemost',
        description='Inflict damage with pillars of fire', mp_cost=10,
        required_level=29, required_mp=112, required_intelligence=146,
        upgrade=2
        # added foreign key ID and value adds to table w/out problem
    )
    skill_4 = Skill(
        category_type='Attack', family_type='Zap', new_name='Zap',
        old_name='Bolt', description='Strikes all enemies with lightning',
        mp_cost=5, required_level=7, required_mp=20, required_intelligence=35
    )
    skill_5 = Skill(
        category_type='Attack', family_type='Zap', new_name='Lightning',
        old_name='Lightning',
        description='Calls on lightning attack to all enemies', mp_cost=3,
        required_level=11, required_hp=65, required_attack=90,
        required_speed=52
    )
    skill_6 = Skill(
        category_type='Recovery', family_type='Heal', new_name='Heal',
        old_name='Heal', description='Heals 30-40 Hp for one ally', mp_cost=2,
        required_level=2, required_mp=7, required_intelligence=6
    )

    test_skills = [skill_1, skill_2, skill_3, skill_4, skill_5, skill_6]

    with Session(engine) as session:
        for skill in test_skills:
            session.add(skill)
        # session.refresh(skill_4)
        session.commit()

    return test_skills


def create_skill_combo(skills):
    # set up to show that in order to learn skills[3], monster needs to know
    # skill[4] and skill[5]

    combo_1 = SkillCombine(combo_skill=skills[3], needed_skill=skills[4])
    combo_2 = SkillCombine(combo_skill=skills[3], needed_skill=skills[5])

    combos = [combo_1, combo_2]

    with Session(engine) as session:
        for combo in combos:
            session.add(combo)
        session.commit()


if __name__ == '__main__':
    unittest.main()
