#app/schemas/ai.py

from pydantic import BaseModel

class EventGenerationRequest(BaseModel):
    title: str