from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
  from .maestro_model import Maestro

class CarreraBase(SQLModel):
  name: str = Field(index=True)
  acronimo: str = Field(index=True)
  id_coordinador: int | None = Field(default=None, foreign_key="maestro.id")

class Carrera(CarreraBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)

class CarreraActualizacion(SQLModel):
  name:  Optional[str] = None
  acronimo: Optional[str] = None
  id_coordinador:  Optional[int] = None