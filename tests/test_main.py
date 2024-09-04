import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

from app.main import app, get_session
from app.models import MonsterDetail
# from app.database 

TEST_DATABASE_URL = "sqlite:///testing.db"


def test_read_main():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the DQMonsters API. Go to the Swagger UI interface"}

def test_create_monster():
    test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:

        def get_session_override():
            return session
        
        app.dependency_overrides[get_session] = get_session_override
        
        client = TestClient(app)

        object_comparison = {
            "new_name" : "Slime",
            "old_name" : "Slime",
            "description" : "The most abundant of this popular specie",
            "family_id" : 1,
        }

        session.add(MonsterDetail(new_name='Slime', old_name='Slime', description='The most abundant of this popular specie', family_id=1))
        session.commit()

        response = client.get('/dqm1/monsters/1')
        data_entry = response.json()
        
        
        assert response.status_code == 200
        assert data_entry["new_name"] == object_comparison["new_name"]
        assert data_entry["old_name"] == object_comparison["old_name"]
        assert data_entry["description"] == object_comparison["description"]
        assert data_entry["family_id"] == object_comparison["family_id"]
    
    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(test_engine)