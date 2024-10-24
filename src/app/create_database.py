import csv
from pathlib import Path

from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from src.app.database import create_db_and_tables, engine
from src.app.models import (
    Item,
    MonsterBreedingLink,
    MonsterDetail,
    MonsterFamily,
    MonsterSkillLink,
    Skill,
    SkillCombine,
)

current_dir = Path(__file__).resolve().parent
csv_dir = current_dir.parent / "csv_files"


def _insert_data(csv_file, Model):
    """
    helper function that uses dictionary unpacking to add csv file data
    into database
    """
    with Session(engine) as session:
        with open(csv_file, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # replace empty string with None
                row = {k: (None if v == "" else v) for k, v in row.items()}
                if "id" in row:
                    existing_entry = session.exec(
                        select(Model).where(Model.id == row["id"])
                    ).first()

                    if existing_entry:
                        print(
                            f"Entry with id {row['id']} already exists. Skipping insertion."
                        )
                        continue
                try:
                    session.add(Model(**row))
                except IntegrityError as e:
                    session.rollback()
                    print(f"IntegrityError has occurred: {e.orig}")

        session.commit()


def create_item_csv():
    _insert_data(csv_dir / "DQM1_items.csv", Item)


def create_monster_family_csv():
    _insert_data(csv_dir / "DQM1_monster_family.csv", MonsterFamily)


def create_skill_csv():
    _insert_data(csv_dir / "DQM1_skills.csv", Skill)


def create_skillcombo_csv():
    _insert_data(csv_dir / "DQM1_skill_combo.csv", SkillCombine)


def create_monster_detail_csv():
    _insert_data(csv_dir / "DQM1_monsterdetails.csv", MonsterDetail)


def create_breed_combo():
    _insert_data(csv_dir / "DQM1_breeding_combo.csv", MonsterBreedingLink)


def create_monster_skill_link():
    _insert_data(csv_dir / "DQM1_monster_skill_link.csv", MonsterSkillLink)


def load_all_csv_data():
    create_db_and_tables()
    create_item_csv()
    create_monster_family_csv()
    create_skill_csv()
    create_skillcombo_csv()
    create_monster_detail_csv()
    create_breed_combo()
    create_monster_skill_link()


if __name__ == "__main__":
    load_all_csv_data()
