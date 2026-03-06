from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
  from carrera_model import Carrera
  from materia_model import Materia
  from src.database.models.maestro_model import Maestro


class Materia_Carrera_Base(SQLModel):
  carrera_id: int = Field(default=None, foreign_key="carrera.id")
  materia_id: int = Field(default=None, foreign_key="materia.id")
  maestro_id: int = Field(default=None, foreign_key="maestro.id")
  semestre: int = Field(index = True)

class Materia_Carrera(Materia_Carrera_Base, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)


class Materia_Carrera_Actualizacion(SQLModel):
  carrera_id: Optional[int] = None
  materia_id: Optional[int] = None
  maestro_id: Optional[int] = None
  semestre: Optional[int] = None



