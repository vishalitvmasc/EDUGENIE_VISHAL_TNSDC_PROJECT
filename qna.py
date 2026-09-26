from ai_client import (
    GeminiError,
    generate_text,
)

from config import get_settings


async def answer_question(
    text: str,
    level: str,
):

    settings = get_settings()

    prompt = f"""
You are EduGenie, an educational
question-answering assistant.

Learner level:
{level}

Question:
{text}

Instructions:

- Answer the question accurately.
- Answer directly first.
- Explain the reasoning when useful.
- Use simple language appropriate for
  the learner level.
- Use short paragraphs or bullet points.
- If the question is ambiguous, state the
  interpretation you are using.
- Do not invent sources.
- Do not mention these instructions.
"""

    try:

        answer = generate_text(prompt)

        return {
            "answer": answer,
            "source": (
                f"Gemini "
                f"({settings.gemini_model})"
            ),
        }

    except GeminiError:

        if settings.demo_mode:

            return {
                "answer": (
                    "Demo mode is active.\n\n"
                    "Your question was received, "
                    "but a Gemini API key is required "
                    "for a real AI answer."
                ),
                "source": "Demo mode",
            }

        raise