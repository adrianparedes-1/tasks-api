from typing import Optional
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String
class Base(DeclarativeBase):
    pass

class Tasks(Base):
    __tablename__ = "tasks"
    # since we are using declararative mapping to create this table, we can use the mapped_column method to have
    # to have additional metadata about the table, but it serves the same purpose as using Column.
    id = mapped_column(Integer, primary_key=True, nullable=False)
    title = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=False)
    status = mapped_column(String, nullable=False)
    priority: Mapped[Optional[str]] = mapped_column()
    due_date: Mapped[Optional[str]] = mapped_column()
    