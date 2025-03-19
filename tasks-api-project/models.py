from datetime import date
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, create_engine, String

DATABASE_URI = "postgres://postgres:password@localhost/taskmanagement"

# engine is a global object that establishes the connection to our db
engine = create_engine(DATABASE_URI, echo=False) 

class Base(DeclarativeBase):
    pass

class Tasks(Base):
    __tablename__ = "tasks"
    # since we are using declararative mapping to create this table, we can use the mapped_column method to have
    # to have additional metadata about the table, but it serves the same purpose as using Column.
    id = mapped_column(Integer, primary_key=True, nullable=False)
    title = mapped_column(String(30), nullable=False)
    description = mapped_column(String, nullable=False)
    status = mapped_column(String(10), nullable=False)
    priority: Optional[str] = mapped_column()
    due_date: Optional[date] = mapped_column()