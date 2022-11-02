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


def _insert_data(csv_file, Model):
    with Session(engine) as session:
        with open(csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                session.add(Model(**row))
        session.commit()


def create_monster_family_csv():
    _insert_data('csv_files/DQM1_monster_family.csv', MonsterFamily)


def create_skill_csv():
    _insert_data('csv_files/DQM1_skills.csv', Skill)


def create_skillcombo_csv():
    session = Session(engine)
    with open('csv_files/DQM1_skill_combo.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for skillcombo_entry in reader:
            session.add(SkillCombine(**skillcombo_entry))

    session.commit()


def create_monster_detail_csv():
    session = Session(engine)
    with open('csv_files/DQM1_monsterdetails.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for monsterdetail_entry in reader:
            session.add(MonsterDetail(**monsterdetail_entry))

    session.commit()


def create_breed_combo():
    session = Session(engine)
    with open('csv_files/DQM1_breeding_combo.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for monstercombo_entry in reader:
            session.add(MonsterBreedingLink(**monstercombo_entry))

    session.commit()


def create_monster_skill_link():
    session = Session(engine)
    with open('csv_files/practice_monster_skill_link.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for monsterskill_entry in reader:
            session.add(MonsterSkillLink(**monsterskill_entry))

    session.commit()


def main():
    create_db_and_tables()
    create_item_csv()
    create_monster_family_csv()
    create_skill_csv()
    create_skillcombo_csv()
    create_monster_detail_csv()
    create_breed_combo()
    create_monster_skill_link()


if __name__ == "__main__":
    main()
