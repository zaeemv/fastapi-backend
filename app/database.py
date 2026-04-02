import os
from sqlmodel import Session, create_engine, SQLModel
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def close_db() -> None:
    engine.dispose()

def get_session():
    with Session(engine) as session:
        yield session