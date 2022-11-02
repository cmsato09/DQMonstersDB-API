from database import create_db_and_tables, engine
from sqlmodel import Session
import csv
from model import Item, MonsterFamily, MonsterDetail, Skill, MonsterSkillLink,\
    MonsterBreedingLink, SkillCombine


def create_item_csv():
    # used dictionary unpacking
    # https://stackoverflow.com/questions/31750441/generalised-insert-into-sqlalchemy-using-dictionary
    session = Session(engine)
    with open('csv_files/DQM1_items.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for item_entry in reader:
            session.add(Item(**item_entry))
    session.commit()


def create_monster_family_csv():
    session = Session(engine)
    with open('csv_files/DQM1_monster_family.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for family_entry in reader:
            session.add(MonsterFamily(**family_entry))

    session.commit()


def create_skill_csv():
    session = Session(engine)
    with open('csv_files/DQM1_skills.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for skill_entry in reader:
            session.add(Skill(**skill_entry))

    session.commit()


def create_skillcombo_csv():
    session = Session(engine)
    with open('csv_files/DQM1_skill_combo.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for skillcombo_entry in reader:
            session.add(SkillCombine(**skillcombo_entry))

    session.commit()


def create_monster_detail(skills):
    monster_1 = MonsterDetail(
        new_name='Drake Slime', old_name='DrakSlime',
        description='Moves and jumps with its tail and wings', family_id=1,
        skills=skills[:3]
    )
    monster_2 = MonsterDetail(
        new_name='Healslime', old_name='Healer',
        description='Uses its powerful tentacles to move about', family_id=1,
        skills=skills[1:]
    )
    monster_3 = MonsterDetail(
        new_name='Cyber slime', old_name='SlimeBorg',
        description='Oil flows through its body instead of blood', family_id=1,
        skills=[skills[3], skills[1], skills[0]]
    )

    test_monsters = [monster_1, monster_2, monster_3]

    with Session(engine) as session:
        for monster in test_monsters:
            session.add(monster)
        session.commit()

    return [monster_1, monster_2, monster_3]


def create_breed_combo():
    session = Session(engine)
    with open('csv_files/DQM1_breeding_combo.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for monstercombo_entry in reader:
            session.add(MonsterBreedingLink(**monstercombo_entry))

    session.commit()


def main():
    create_db_and_tables()
    create_item_csv()
    create_monster_family_csv()
    create_skill_csv()
    create_skillcombo_csv()
    # monsters = create_monster_detail(skills)
    create_breed_combo()
    # create_monster_detail(skills)


if __name__ == "__main__":
    main()
