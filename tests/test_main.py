import pytest
from fastapi.testclient import TestClient
from app.main import app, get_session
# from app.database 

TEST_DATABASE_URL = "sqlite:///testing.db"


def test_read_main():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the DQMonsters API. Go to the Swagger UI interface"}

# def test_create_monster():
#     pass