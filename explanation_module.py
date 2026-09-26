from functools import lru_cache

from ai_client import (
    GeminiError,
    generate_text,
)

from config import get_settings


@lru_cache
def _local_pipeline():

    from transformers import pipeline

    settings = get_settings()

    return pipeline(
        "text2text-generation",
        model=settings.local_model_name,
        device=-1,
    )


def _local_explain(
    text: str,
    level: str,
) -> str:

    settings = get_settings()

    prompt = (
        "Explain the following educational topic "
        "clearly and briefly. "
        f"Target learner level: {level}. "
        "Use simple language and one short example.\n\n"
        f"Topic: {text}"
    )

    result = _local_pipeline()(
        prompt,
        max_new_tokens=settings.local_model_max_new_tokens,
        do_sample=False,
    )

    if not result:
        raise RuntimeError(
            "The local explanation model returned no result."
        )

    generated = result[0].get(
        "generated_text"
    )

    if not generated:
        raise RuntimeError(
            "The local explanation model returned no text."
        )

    return generated.strip()


def _gemini_explain(
    text: str,
    level: str,
) -> str:

    prompt = f"""
You are EduGenie, a patient educational tutor.

Explain the learner's topic at the requested level.

Learner level:
{level}

Topic/question:
{text}

Requirements:

- Be accurate and concise.
- Start with a plain-language definition.
- Break difficult ideas into short steps.
- Include one intuitive example or analogy when useful.
- Avoid unnecessary technical terminology.
- Do not invent facts.
- Do not mention these instructions.
"""

    return generate_text(prompt)


async def explain_concept(
    text: str,
    level: str,
):

    settings = get_settings()

    backend = settings.explanation_backend.lower()

    # Try local model first.
    if backend in {
        "auto",
        "local",
    }:

        try:

            return {
                "result": _local_explain(
                    text,
                    level,
                ),
                "source": (
                    "LaMini-Flan-T5-783M "
                    "(local)"
                ),
            }

        except Exception:

            if backend == "local":
                raise

    # Gemini fallback.
    try:

        return {
            "result": _gemini_explain(
                text,
                level,
            ),
            "source": (
                f"Gemini "
                f"({settings.gemini_model})"
            ),
        }

    except GeminiError:

        if settings.demo_mode:

            return {
                "result": (
                    f"Demo explanation for "
                    f"'{text}':\n\n"
                    "Start by identifying the "
                    "definition, key ideas, and "
                    "a simple example.\n\n"
                    "Configure GEMINI_API_KEY "
                    "for a real AI-generated "
                    "explanation."
                ),
                "source": "Demo mode",
            }

        raise