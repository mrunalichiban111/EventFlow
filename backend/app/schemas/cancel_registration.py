# app/schemas/cancel_registration.py

from pydantic import BaseModel

class CancelRegistration(BaseModel):
    registration_id: int