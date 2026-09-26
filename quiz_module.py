import json
import re

from ai_client import (
    GeminiError,
    generate_text,
)

from config import get_settings


def clean_json_block(
    raw: str,
) -> str:

    text = raw.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    return text.strip()


def validate_quiz(data):

    if not isinstance(data, list):
        raise ValueError(
            "Quiz response must be a list."
        )

    if len(data) != 3:
        raise ValueError(
            "Quiz response must contain "
            "exactly 3 questions."
        )

    normalized = []

    for item in data:

        if not isinstance(item, dict):
            raise ValueError(
                "Each quiz question must "
                "be an object."
            )

        question = str(
            item.get(
                "question",
                "",
            )
        ).strip()

        options = item.get(
            "options"
        )

        correct_answer = str(
            item.get(
                "correct_answer",
                "",
            )
        ).strip()

        explanation = str(
            item.get(
                "explanation",
                "",
            )
        ).strip()

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        if not isinstance(
            options,
            list,
        ):
            raise ValueError(
                "Options must be a list."
            )

        if len(options) != 4:
            raise ValueError(
                "Each question must contain "
                "exactly four options."
            )

        options = [
            str(option).strip()
            for option in options
        ]

        if any(
            not option
            for option in options
        ):
            raise ValueError(
                "Options cannot be empty."
            )

        if correct_answer not in options:
            raise ValueError(
                "correct_answer must exactly "
                "match one option."
            )

        if not explanation:
            explanation = (
                "Review the supplied material "
                "to verify the answer."
            )

        normalized.append(
            {
                "question": question,
                "options": options,
                "correct_answer": correct_answer,
                "explanation": explanation,
            }
        )

    return normalized


async def generate_quiz(
    text: str,
    level: str,
):

    settings = get_settings()

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly THREE multiple-choice
questions from the supplied educational
content.

Learner level:
{level}

Educational content:
{text}

Return ONLY a valid JSON array.

Each object must contain exactly:

{{
    "question": "string",
    "options": [
        "string",
        "string",
        "string",
        "string"
    ],
    "correct_answer": "string",
    "explanation": "string"
}}

Rules:

- Exactly 3 questions.
- Exactly 4 options per question.
- correct_answer must exactly match
  one of the options.
- Questions must be based on the
  supplied content.
- Distractors should be plausible.
- Do not use Markdown.
"""

    try:

        raw = generate_text(prompt)

        cleaned = clean_json_block(raw)

        data = json.loads(cleaned)

        validated = validate_quiz(data)

        return {
            "questions": validated,
            "source": (
                f"Gemini "
                f"({settings.gemini_model})"
            ),
        }

    except (
        GeminiError,
        json.JSONDecodeError,
        ValueError,
        TypeError,
    ) as exc:

        if settings.demo_mode:

            demo_questions = [
                {
                    "question": (
                        "What is the main purpose "
                        "of the supplied passage?"
                    ),
                    "options": [
                        "To present educational information",
                        "To provide a restaurant menu",
                        "To describe a sports match",
                        "To advertise a vehicle",
                    ],
                    "correct_answer": (
                        "To present educational information"
                    ),
                    "explanation": (
                        "The passage is being used "
                        "as educational material."
                    ),
                },
                {
                    "question": (
                        "Which approach is useful "
                        "when studying new material?"
                    ),
                    "options": [
                        "Break it into smaller ideas",
                        "Ignore the definitions",
                        "Avoid examples",
                        "Memorize without understanding",
                    ],
                    "correct_answer": (
                        "Break it into smaller ideas"
                    ),
                    "explanation": (
                        "Breaking information into "
                        "smaller ideas can support "
                        "understanding."
                    ),
                },
                {
                    "question": (
                        "What can a learner do when "
                        "a concept is unclear?"
                    ),
                    "options": [
                        "Ask for a simpler explanation",
                        "Stop studying immediately",
                        "Guess and never verify",
                        "Delete the study material",
                    ],
                    "correct_answer": (
                        "Ask for a simpler explanation"
                    ),
                    "explanation": (
                        "Asking for clarification "
                        "helps address gaps in understanding."
                    ),
                },
            ]

            return {
                "questions": demo_questions,
                "source": "Demo mode",
            }

        raise RuntimeError(
            f"Quiz generation failed: {exc}"
        ) from exc