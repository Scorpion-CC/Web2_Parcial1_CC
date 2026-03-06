from sqlmodel import SQLModel, create_engine
from src.database.models.maestro_model import Maestro
from src.database.models.carrera_model import Carrera
from src.database.models.materia_carrera_model import Materia_Carrera
from src.database.models.materia_model import Materia

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_db_and_tables():
  SQLModel.metadata.create_all(engine)