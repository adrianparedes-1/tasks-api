from . import models
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URI = "postgresql://postgres:password@localhost/taskmanagement"

# engine is a global object that establishes the connection to our db
engine = create_engine(DATABASE_URI, echo=False) 

models.Tasks.metadata.create_all(engine) #create table on db

# session factory for session instance creation
SessionLocal = sessionmaker(engine)


def get_db():
    session = SessionLocal() #create a session instance
    try:
        yield session # yield session so it pauses the function and returns to close session regardless of outcome
    finally:
        session.flush()
        session.close()

