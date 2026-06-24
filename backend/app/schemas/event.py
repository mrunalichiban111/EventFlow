# app/schemas/event.py

from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    description: str
    capacity: int
    event_date: datetime