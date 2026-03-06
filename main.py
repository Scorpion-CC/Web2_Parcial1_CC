from fastapi import FastAPI, Depends
from fastapi.concurrency import asynccontextmanager
from src.database.database import create_db_and_tables, engine
from src.routers import maestro_router
from src.routers import materia_router
from src.routers import carrera_router
from src.routers import materia_carrera_router
from src.dependencies import get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
  create_db_and_tables()
  yield

app = FastAPI(lifespan=lifespan, dependencies =[Depends(get_session)])

app.include_router(maestro_router.router)
app.include_router(materia_router.router)
app.include_router(carrera_router.router)
app.include_router(materia_carrera_router.router)
