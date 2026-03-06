from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

class MaestroBase(SQLModel):
  name: str = Field(index=True)
  anio_ingreso: int
  anio_salida: Optional[int] = Field(default = None)

class Maestro(MaestroBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)

class MaestroActualizacion(SQLModel):
  name: Optional[str] = None
  anio_ingreso: Optional[int] = None
  anio_salida: Optional[int] = None