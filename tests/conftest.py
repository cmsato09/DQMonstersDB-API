import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app, get_session

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

# @pytest.fixture(name="client")
# def client_fixture(session: Session):
#     def get_test_session():
#         yield session

#     app.dependency_overrides[get_session] = get_test_session
#     client = TestClient(app)
#     yield client
#     app.dependency_overrides.clear()