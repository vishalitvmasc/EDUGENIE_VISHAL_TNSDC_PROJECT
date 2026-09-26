from functools import lru_cache

from google import genai
from google.genai import types

from config import get_settings


class GeminiError(RuntimeError):
    """
    Raised when Gemini cannot be used.
    """


@lru_cache
def get_client():
    settings = get_settings()

    if not settings.gemini_api_key:
        raise GeminiError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your .env file and restart the server."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_text(
    prompt: str,
    *,
    json_schema=None,
) -> str:

    settings = get_settings()

    client = get_client()

    config_kwargs = {
        "temperature": 0.3,
        "max_output_tokens": 2048,
    }

    if json_schema is not None:
        config_kwargs["response_mime_type"] = "application/json"
        config_kwargs["response_schema"] = json_schema

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            **config_kwargs
        ),
    )

    text = getattr(response, "text", None)

    if not text:
        raise GeminiError(
            "Gemini returned an empty response."
        )

    return text.strip()