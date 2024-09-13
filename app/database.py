from pathlib import Path

from sqlmodel import SQLModel, create_engine

app_dir = Path(__file__).resolve().parent
project_dir = app_dir.parent

sqlite_file_name = project_dir / "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
