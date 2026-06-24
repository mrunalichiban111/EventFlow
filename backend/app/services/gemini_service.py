import os
from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_event_content(title: str):

    prompt = f"""
    Create a professional campus event.

    Event Title: {title}

    Return ONLY valid JSON in this format:

    {{
      "description": "...",
      "agenda": [
        "...",
        "..."
      ],
      "learning_outcomes": [
        "...",
        "..."
      ]
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text