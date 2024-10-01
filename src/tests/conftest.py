import csv

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app, get_session
from app.models import (
    Item,
    MonsterBreedingLink,
    MonsterDetail,
    MonsterFamily,
    MonsterSkillLink,
    Skill,
    SkillCombine,
)


@pytest.fixture(name="session")
def session_fixture():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session

    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="session_module", scope="module")
def session_module():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        yield session

    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="client_module", scope="module")
def client_module(session_module: Session):
    def get_session_override():
        yield session_module

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="load_all_csvdata", scope="module")
def load_csv_data(session_module: Session):
    csv_files = {
        ("src/csv_files/DQM1_items.csv", Item),
        ("src/csv_files/DQM1_monster_family.csv", MonsterFamily),
        ("src/csv_files/DQM1_skills.csv", Skill),
        ("src/csv_files/DQM1_skill_combo.csv", SkillCombine),
        ("src/csv_files/DQM1_monsterdetails.csv", MonsterDetail),
        ("src/csv_files/DQM1_breeding_combo.csv", MonsterBreedingLink),
        ("src/csv_files/DQM1_monster_skill_link.csv", MonsterSkillLink),
    }

    for csvfile, Model in csv_files:
        try:
            with open(csvfile, encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # replace empty string with None
                    row = {k: (None if v == "" else v) for k, v in row.items()}
                    session_module.add(Model(**row))
            session_module.commit()
        except Exception as e:
            print(f"Error loading {csvfile} : {e}")
