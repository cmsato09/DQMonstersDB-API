import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

from app.main import app, get_session
from app.models import MonsterDetail

TEST_DATABASE_URL = "sqlite:///testing.db"


def test_read_root():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the DQMonsters API. Go to the Swagger UI interface"}

def test_create_monster(client: TestClient, session: Session):

    session.add(MonsterDetail(new_name='Slime', old_name='Slime', description='The most abundant of this popular specie', family_id=1))
    session.commit()

    response = client.get('/dqm1/monsters/1')
    data_entry = response.json()
    
    object_comparison = {
        "new_name" : "Slime",
        "old_name" : "Slime",
        "description" : "The most abundant of this popular specie",
        "family_id" : 1,
    }
    
    assert response.status_code == 200
    assert data_entry["new_name"] == object_comparison["new_name"]
    assert data_entry["old_name"] == object_comparison["old_name"]
    assert data_entry["description"] == object_comparison["description"]
    assert data_entry["family_id"] == object_comparison["family_id"]
    