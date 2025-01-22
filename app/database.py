from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.engine import URL
from fastapi import Depends
from typing import Annotated

from .config import settings


url = URL.create(
    "postgresql",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database=settings.database_name,
)

engine = create_engine(url, echo=False)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)




