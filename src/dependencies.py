from sqlmodel import Session
from typing import Annotated, TypeAlias
from fastapi import Depends
from src.database.database import engine

def get_session():
  with Session(engine) as session:
    yield session

SessionDep: TypeAlias = Annotated[Session, Depends(get_session)]