from fastapi import APIRouter, HTTPException
from src.database.models.materia_model import Materia, MateriaBase, MateriaActualizacion
from ..dependencies import SessionDep
from typing import Any
from sqlmodel import Field, SQLModel, create_engine, Session, select, col, or_, Relationship
from src.database.database import engine

router = APIRouter(
  prefix="/materias",
  tags=["Materias"],)

@router.get("/", response_model=list[Materia])
def get_materias(session: SessionDep) -> Any:
  statement = select(Materia)
  results = session.exec(statement)
  materias = results.all()
  return materias

@router.post("/")
def create_materia(materia: MateriaBase, session: SessionDep) -> Materia: 
  materiaNueva = Materia.model_validate(materia)
  session.add(materiaNueva)
  session.commit()
  session.refresh(materiaNueva)
  return materiaNueva

@router.put("/{id}")
def update_materia(id: int, materia_actualizada: MateriaActualizacion, session: SessionDep) -> Materia:
  materia = session.get(Materia, id)
  if materia is None: 
    raise HTTPException(status_code=404, detail="La materia que buscas no existe")
  
  if(materia_actualizada.name is not None):
    materia.name = materia_actualizada.name

  if(materia_actualizada.clave is not None):
    materia.clave = materia_actualizada.clave

  session.add(materia)
  session.commit()
  session.refresh(materia)
  return materia

@router.delete("/{id}")
def delete_materia(id: int, session: SessionDep):
  materia = session.get(Materia, id)
  if materia is None: 
    raise HTTPException(status_code=404, detail="La materia que quieres eliminar no existe")
  session.delete(materia)
  session.commit()
  return "La materia " + materia.name + " ha sido eliminada correctamente"