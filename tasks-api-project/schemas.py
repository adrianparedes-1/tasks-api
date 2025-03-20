from datetime import date
from typing import Optional
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    description: str
    status: str
    priority: Optional[str] = None
    due_date: Optional[date] = None