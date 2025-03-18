from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

DATABASE_URI = "postgres://postgres:password@localhost/taskmanagement"

engine = create_engine()

class Base(DeclarativeBase):
    pass

class Tasks(Base):
    pass