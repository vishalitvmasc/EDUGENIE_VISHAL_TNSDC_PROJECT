from ai_client import (
    GeminiError,
    generate_text,
)

from config import get_settings


async def get_learning_recommendations(
    topic: str,
    level: str,
    weeks: int,
):

    settings = get_settings()

    prompt = f"""
You are EduGenie, a personalized
learning-path designer.

Topic:
{topic}

Current learner level:
{level}

Duration:
{weeks} weeks

Create a structured learning path.

Include:

1. Overall learning goal.

2. Week-by-week topics.

3. What the learner should practice.

4. Recommended resource TYPES such as:
   - official documentation
   - textbooks
   - tutorials
   - practice problems
   - videos
   - projects

Do not invent exact URLs.

5. A checkpoint or self-test for
   each major phase.

Move logically from fundamentals
toward more advanced concepts.

Keep the plan practical and readable.
"""

    try:

        recommendations = generate_text(
            prompt
        )

        return {
            "recommendations": recommendations,
            "source": (
                f"Gemini "
                f"({settings.gemini_model})"
            ),
        }

    except GeminiError:

        if settings.demo_mode:

            return {
                "recommendations": (
                    f"Demo learning path for "
                    f"{topic} ({weeks} weeks).\n\n"

                    "Weeks 1-2 — Foundations\n"
                    "Learn terminology and core concepts.\n\n"

                    "Weeks 3-4 — Practice\n"
                    "Complete guided exercises and "
                    "small practical tasks.\n\n"

                    "Weeks 5-6 — Application\n"
                    "Build a practical project and "
                    "review weak areas.\n\n"

                    "Configure GEMINI_API_KEY for "
                    "a personalized AI-generated plan."
                ),
                "source": "Demo mode",
            }

        raise