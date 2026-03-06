from fastapi import APIRouter, HTTPException
from src.database.models.materia_carrera_model import Materia_Carrera, Materia_Carrera_Base, Materia_Carrera_Actualizacion
from src.database.models.carrera_model import Carrera
from src.database.models.maestro_model import Maestro
from src.database.models.materia_model import Materia
from ..dependencies import SessionDep
from typing import Any
from sqlmodel import Field, SQLModel, create_engine, Session, select, col, or_, Relationship
from src.database.database import engine

router = APIRouter(
  prefix="/carreras/materias",
  tags=["Carrera-Materias"],)

@router.get("/", response_model=list[Materia_Carrera])
def get_materias_de_carrera(session: SessionDep) -> Any:
  statement = select(Materia_Carrera)
  results = session.exec(statement)
  carrera = results.all()
  return carrera

@router.post("/")
def create_materia_de_carrera(materia_carrera: Materia_Carrera_Base, session: SessionDep) -> Materia_Carrera: 

  maestro = session.get(Maestro, materia_carrera.maestro_id)
  if maestro is None: 
    raise HTTPException(status_code=404, detail="El maestro seleccionado no existe")

  materia = session.get(Materia, materia_carrera.materia_id)
  if materia is None: 
    raise HTTPException(status_code=404, detail="La materia seleccionada no existe")

  carrera = session.get(Carrera, materia_carrera.carrera_id)
  if carrera is None: 
    raise HTTPException(status_code=404, detail="La carrera seleccionada no existe")
  

  statement = select(Materia_Carrera).where(col(Materia_Carrera.maestro_id) == materia_carrera.maestro_id, Materia_Carrera.carrera_id == materia_carrera.carrera_id, Materia_Carrera.materia_id == materia_carrera.materia_id)
  result = session.exec(statement).first()
  if result is not None:
    raise HTTPException(status_code=400, detail="Esta materia ya es impartida por el maestro dentro de la carrera (duplicado)")
  
  nuevaMateriaCarrera = Materia_Carrera.model_validate(materia_carrera)
  session.add(nuevaMateriaCarrera)
  session.commit()
  session.refresh(nuevaMateriaCarrera)
  return nuevaMateriaCarrera


@router.put("/{id}")
def update_materia_de_carrera(id: int, materia_carrera_actualizada: Materia_Carrera_Actualizacion, session: SessionDep) -> Materia_Carrera:
  materiaDeCarrera = session.get(Materia_Carrera, id)
  if materiaDeCarrera is None: 
    raise HTTPException(status_code=404, detail="La id utilizada no retornó ningún dato")
  if (materia_carrera_actualizada.carrera_id is not None):
    materiaDeCarrera.carrera_id = materia_carrera_actualizada.carrera_id

  if (materia_carrera_actualizada.materia_id is not None):
    materiaDeCarrera.materia_id = materia_carrera_actualizada.materia_id

  if (materia_carrera_actualizada.maestro_id is not None):
    materiaDeCarrera.maestro_id = materia_carrera_actualizada.maestro_id

  if (materia_carrera_actualizada.semestre is not None and materia_carrera_actualizada.semestre >= 0):
    materiaDeCarrera.semestre = materia_carrera_actualizada.semestre

  statement = select(Materia_Carrera).where(col(Materia_Carrera.maestro_id) == materiaDeCarrera.maestro_id, Materia_Carrera.carrera_id == materiaDeCarrera.carrera_id, Materia_Carrera.materia_id == materiaDeCarrera.materia_id)
  result = session.exec(statement).first()
  if result is not None:
    raise HTTPException(status_code=400, detail="Ya existe un registro con los mismos datos (datos duplicados)")

  session.add(materiaDeCarrera)
  session.commit()

  session.refresh(materiaDeCarrera)
  return materiaDeCarrera



@router.delete("/{id}")
def delete_materia_de_carrera(id: int, session: SessionDep):
  materia_carrera = session.get(Materia_Carrera, id)
  if materia_carrera is None: 
    raise HTTPException(status_code=404, detail="La materia de la carrera que quieres eliminar no existe")
  session.delete(materia_carrera)
  session.commit()
  return "La materia ha sido eliminada de la carrera correctamente"