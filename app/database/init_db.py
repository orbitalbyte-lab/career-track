from app.database.connection import Base, engine
from app.database.models.application import ApplicationDB
from app.database.models.company import CompanyDB

def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)