from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

class MateriaBase(SQLModel):
  name: str = Field(index=True) 
  clave: int | None = Field(index = True)

class Materia(MateriaBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)

class MateriaActualizacion(SQLModel):
  name: Optional[str] = None
  clave: Optional[int] = None