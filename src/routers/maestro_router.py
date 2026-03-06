from fastapi import APIRouter, HTTPException
from src.database.models.maestro_model import Maestro, MaestroBase, MaestroActualizacion
from src.database.models.materia_carrera_model import Materia_Carrera
from src.database.models.materia_model import Materia
from src.database.models.carrera_model import Carrera
from ..dependencies import SessionDep
from typing import Any
from sqlmodel import Field, SQLModel, create_engine, Session, select, col, or_, Relationship
from src.database.database import engine


router = APIRouter(
  prefix="/maestros",
  tags=["Maestros"],)


@router.get("/", response_model=list[Maestro])
def get_maestros(session: SessionDep) -> Any:
  statement = select(Maestro)
  results = session.exec(statement)
  maestros = results.all()
  return maestros

@router.get("/{id}/materias")
def get_materias_maestro(id: int, session: SessionDep) -> Any:
  maestro = session.get(Maestro, id)
  if maestro is None: 
    raise HTTPException(status_code=404, detail="El maestro que buscas no existe")

  statement = (
    select(Materia_Carrera, Carrera, Materia)
    .join(Carrera, Materia_Carrera.carrera_id == Carrera.id)
    .join(Materia, Materia_Carrera.materia_id == Materia.id)
    .where(Materia_Carrera.maestro_id == maestro.id)
    )
  
  result = session.exec(statement).all()

  return "Maestro: " + maestro.name, [{"materia": materia.name, "carrera": carrera.acronimo, "semestre": materia_carrera.semestre} for materia_carrera, carrera, materia in result]


@router.post("/", response_model = Maestro)
def create_maestro(maestro: MaestroBase, session: SessionDep) -> Maestro: 
  maestroNuevo = Maestro.model_validate(maestro)
  session.add(maestroNuevo)
  session.commit()
  session.refresh(maestroNuevo)
  return maestroNuevo

@router.put("/{id}")
def update_maestro(id: int, maestro_actualizado: MaestroActualizacion, session: SessionDep) -> Maestro:
  maestro = session.get(Maestro, id)
  if maestro is None: 
    raise HTTPException(status_code=404, detail="El maestro que buscas no existe")
  
  if (maestro_actualizado.name is not None):
    maestro.name = maestro_actualizado.name
  if (maestro_actualizado.anio_ingreso is not None):
    maestro.anio_ingreso = maestro_actualizado.anio_ingreso
  if (maestro_actualizado.anio_salida is not None):
    maestro.anio_salida = maestro_actualizado.anio_salida

  session.add(maestro)
  session.commit()
  session.refresh(maestro)
  return maestro


@router.delete("/{id}")
def delete_maestro(id: int, session: SessionDep):
  maestro = session.get(Maestro, id)
  if maestro is None: 
    raise HTTPException(status_code=404, detail="El maestro que buscas no existe")
  session.delete(maestro)
  session.commit()
  return "El maestro " + maestro.name + " ha sido eliminado correctamente"












def create_maestros():
  with Session(engine) as session:
    maestro1 = Maestro(
      name="Daniel Martínez",
      anio_ingreso = 2008
    )
    maestro2 = Maestro(
      name="Lester",
      anio_ingreso = 2019,
      anio_salida = 2025
    )
    maestro3 = Maestro(
      name="Fulanita",
      anio_ingreso = 2020
    )
    maestro4 = Maestro(
      name="Menganito",
      anio_ingreso = 2015
    )
    maestro5 = Maestro(
      name="Daniel Martínez",
      anio_ingreso = 2023
    )
    session.add(maestro1)
    session.add(maestro2)
    session.add(maestro3)
    session.add(maestro4)
    session.add(maestro5)
    session.commit
    session.refresh(maestro1)
    session.refresh(maestro2)
    session.refresh(maestro3)
    session.refresh(maestro4)
    session.refresh(maestro5)
    
    print("Maestro creado: ", maestro1)
    print("Maestro creado: ", maestro2)
    print("Maestro creado: ", maestro3)
    print("Maestro creado: ", maestro4)
    print("Maestro creado: ", maestro5)




# def update_heroes():
#    with Session(engine) as session:
#        hero_spider_boy = session.exec(
#            select(Hero).where(Hero.name == "Spider-Boy")
#        ).one()
#        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()
#        team_z_force.heroes.append(hero_spider_boy)
#        session.add(team_z_force)
#        session.commit()
#
#        print("Updated Spider-Boy's Teams:", hero_spider_boy.teams)
#        print("Z-Force heroes:", team_z_force.heroes)

#        hero_spider_boy.teams.remove(team_z_force)
#        session.add(team_z_force)
#        session.commit()

#        print("Reverted Z-Force's heroes:", team_z_force.heroes)
#        print("Reverted Spider-Boy's teams:", hero_spider_boy.teams)