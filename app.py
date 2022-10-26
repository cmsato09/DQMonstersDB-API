from database import create_db_and_tables, engine
from sqlmodel import Session
from model import Item, MonsterFamily, MonsterDetail, Skill, MonsterSkillLink


def create_items():
    item_1 = Item(
        item_name='Herb',item_category='Recovery',
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
        item_description='Cures poison of one ally', price=10, sell_price=8,
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
    session = Session(engine)

    session.add(item_1)
    session.add(item_2)
    session.add(item_3)
    session.add(item_4)
    session.add(item_5)

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

    with Session(engine) as session:
        session.add(family_1)
        session.add(family_2)
        session.add(family_3)
        session.add(family_4)
        session.add(family_5)
        session.add(family_6)
        session.add(family_7)
        session.add(family_8)
        session.add(family_9)
        session.add(family_10)

        session.commit()


def create_monster_detail():
    monster_1 = MonsterDetail(
        new_name='Drake Slime', old_name='DrakSlime',
        description='Moves and jumps with its tail and wings', family_id=1,
        skills=[1, 2, 3]
    )
    monster_2 = MonsterDetail(
        new_name='Healslime', old_name='Healer',
        description='Uses its powerful tentacles to move about', family_id=1,
        skills=[2, 3, 4]
    )
    monster_3 = MonsterDetail(
        new_name='Cyber slime', old_name='SlimeBorg',
        description='Oil flows through its body instead of blood', family_id=1,
        skills=[4, 2, 1]
    )

    with Session(engine) as session:
        session.add(monster_1)
        session.add(monster_2)
        session.add(monster_3)

        session.commit()


def create_skill():
    skill_1 = Skill(
        category_type='Attack', family_type='Frizz', new_name='Frizz',
        old_name='Blaze', description='Inflict damage with small fireball ',
        mp_cost=2, required_level=2, required_mp=7, required_intelligence=20
    )
    skill_2 = Skill(
        category_type='Attack', family_type='Zap', new_name='Zap',
        old_name='Bolt', description='Strikes all enemies with lightning',
        mp_cost=5, required_level=7,required_mp=20, required_intelligence=35
    )
    skill_3 = Skill(
        category_type='Attack', family_type='Zap', new_name='Lightning',
        old_name='Lightning',
        description='Calls on lightning attack to all enemies', mp_cost=3,
        required_level=11, required_hp=65, required_attack=90,
        required_speed=52
    )
    skill_4 = Skill(
        category_type='Recovery', family_type='Heal', new_name='Heal',
        old_name='Heal', description='Heals 30-40 Hp for one ally', mp_cost=2,
        required_level=2, required_mp=7, required_intelligence=6
    )

    with Session(engine) as session:
        session.add(skill_1)
        session.add(skill_2)
        session.add(skill_3)
        session.add(skill_4)

        session.commit()


def main():
    create_db_and_tables()
    create_items()
    create_monster_family()
    create_skill()
    create_monster_detail()


if __name__== "__main__":
    main()
