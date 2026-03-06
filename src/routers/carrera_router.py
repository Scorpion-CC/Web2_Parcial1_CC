from fastapi import APIRouter, HTTPException
from src.database.models.carrera_model import Carrera, CarreraBase, CarreraActualizacion
from src.database.models.maestro_model import Maestro
from ..dependencies import SessionDep
from typing import Any
from sqlmodel import Field, SQLModel, create_engine, Session, select, col, or_, Relationship
from src.database.database import engine

router = APIRouter(
  prefix="/carreras",
  tags=["Carreras"],)

@router.get("/", response_model=list[Carrera])
def get_carrera(session: SessionDep) -> Any:
  statement = select(Carrera)
  results = session.exec(statement)
  carrera = results.all()
  return carrera

@router.post("/")
def create_carrera(carrera: CarreraBase, session: SessionDep) -> Carrera: 
  coordinador = session.get(Maestro, carrera.id_coordinador)
  if coordinador is None: 
    raise HTTPException(status_code=404, detail="El maestro seleccionado no existe")
  
  statement = select(Carrera).where(col(Carrera.id_coordinador) == carrera.id_coordinador)
  result = session.exec(statement).first()
  if result is not None:
    raise HTTPException(status_code=400, detail="El maestro seleccionado ya coordina una carrera")

  carreraNueva = Carrera.model_validate(carrera)
  session.add(carreraNueva)
  session.commit()
  session.refresh(carreraNueva)
  return carreraNueva

@router.put("/{id}")
def update_carrera(id: int, carrera_actualizada: CarreraActualizacion, session: SessionDep) -> Carrera:
  carrera = session.get(Carrera, id)
  if carrera is None: 
    raise HTTPException(status_code=404, detail="La carrera que buscas no existe")
  
  statement = select(Carrera).where(col(Carrera.id_coordinador) == carrera.id_coordinador)
  result = session.exec(statement).first()
  if result is not None:
    raise HTTPException(status_code=400, detail="El maestro seleccionado ya coordina una carrera")

  if (carrera_actualizada.name is not None):
    carrera.name = carrera_actualizada.name
  
  if (carrera_actualizada.acronimo is not None):
    carrera.acronimo = carrera_actualizada.acronimo
  
  if (carrera_actualizada.id_coordinador is not None):  
    carrera.id_coordinador = carrera_actualizada.id_coordinador
  
  session.add(carrera)
  session.commit()
  session.refresh(carrera)
  return carrera

@router.delete("/{id}")
def delete_carrera(id: int, session: SessionDep):
  carrera = session.get(Carrera, id)
  if carrera is None: 
    raise HTTPException(status_code=404, detail="La carrera que quieres eliminar no existe")
  session.delete(carrera)
  session.commit()
  return "La materia " + carrera.name + " ha sido eliminada correctamente"