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


def create_breeds(families, monsters):
    with Session(engine) as session:
        for family, monster in zip(
            families,
            reversed(monsters)
        ):
            breed_1 = MonsterBreedingLink(
                child=monster,
                pedigree=monster)
            breed_2 = MonsterBreedingLink(
                child=monster,
                pedigree=monster,
                parent2=monster,
                pedigree_family=family)
            breed_3 = MonsterBreedingLink(
                child=monster,
                pedigree=monster,
                parent2=monster,
                pedigree_family=family,
                family2=family)
            session.add(breed_1)
            session.add(breed_2)
            session.add(breed_3)
            session.commit()


def main():
    create_db_and_tables()
    create_item_csv()
    create_monster_family_csv()
    create_skill_csv()
    # monsters = create_monster_detail(skills)
    # create_breeds(families, monsters)
    # create_skill_combo(skills)
    # create_monster_detail(skills)


if __name__ == "__main__":
    main()
