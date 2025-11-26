from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base model with common attributes
class NoticeBase(BaseModel):
    title: str
    content: Optional[str] = None

# Model for creating a new notice (used in POST request body)
class NoticeCreate(NoticeBase):
    pass

# Model for updating a notice (used in PUT request body)
class NoticeUpdate(NoticeBase):
    pass

# Model for reading a notice (used in responses), includes all DB columns
class Notice(NoticeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True # Changed from orm_mode = True for Pydantic v2
