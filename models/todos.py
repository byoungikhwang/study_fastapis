from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TodoBase(BaseModel):
    content: str
    status: Optional[str] = "Pending"
    deadline_time: Optional[datetime] = None

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    content: Optional[str] = None
    status: Optional[str] = None
    deadline_time: Optional[datetime] = None

class Todo(TodoBase):
    id: int
    create_time: datetime

    class Config:
        from_attributes = True
