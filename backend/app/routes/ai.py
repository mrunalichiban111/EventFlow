#app/routes/ai.py

from fastapi import APIRouter

from app.schemas.ai import EventGenerationRequest
from app.services.gemini_service import generate_event_content

router = APIRouter()

@router.post("/ai/generate-event")
def generate_event(
    request: EventGenerationRequest
):

    content = generate_event_content(
        request.title
    )

    return {
        "generated_content": content
    }