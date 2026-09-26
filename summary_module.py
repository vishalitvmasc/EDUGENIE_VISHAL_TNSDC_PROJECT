from ai_client import (
    GeminiError,
    generate_text,
)

from config import get_settings


async def summarize_text(
    text: str,
    level: str,
):

    settings = get_settings()

    prompt = f"""
You are EduGenie, an educational
summarization assistant.

Summarize the following passage for a
{level} learner.

PASSAGE:
{text}

Requirements:

- Preserve the central meaning.
- Preserve important facts.
- Remove unnecessary repetition.
- Use clear and simple language.
- Keep the summary concise.
- Use bullet points when appropriate.
- Do not add facts that are not present
  in the original passage.
- Do not mention these instructions.
"""

    try:

        summary = generate_text(prompt)

        return {
            "summary": summary,
            "source": (
                f"Gemini "
                f"({settings.gemini_model})"
            ),
        }

    except GeminiError:

        if settings.demo_mode:

            sentences = [
                sentence.strip()
                for sentence
                in text.replace(
                    "\n",
                    " ",
                ).split(".")
                if sentence.strip()
            ]

            demo = ". ".join(
                sentences[:3]
            )

            if demo and not demo.endswith("."):
                demo += "."

            return {
                "summary": (
                    f"Demo summary:\n\n{demo}"
                ),
                "source": "Demo mode",
            }

        raise