# app/schemas/registration.py

from pydantic import BaseModel

class RegistrationCreate(BaseModel):
    event_id: int