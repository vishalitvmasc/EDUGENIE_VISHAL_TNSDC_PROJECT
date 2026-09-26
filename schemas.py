from typing import List

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


class BaseTextRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=20000,
    )

    level: str = Field(
        default="beginner",
        max_length=30,
    )

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Text cannot be empty."
            )

        return value

    @field_validator("level")
    @classmethod
    def clean_level(cls, value: str) -> str:

        value = value.strip().lower()

        allowed = {
            "beginner",
            "intermediate",
            "advanced",
        }

        if value not in allowed:
            return "beginner"

        return value


class ExplainRequest(BaseTextRequest):
    pass


class QARequest(BaseTextRequest):
    pass


class QuizRequest(BaseTextRequest):
    pass


class SummaryRequest(BaseTextRequest):
    pass


class LearningPathRequest(BaseTextRequest):

    weeks: int = Field(
        default=6,
        ge=1,
        le=52,
    )


class ExplainResponse(BaseModel):

    result: str

    source: str


class QAResponse(BaseModel):

    answer: str

    source: str


class QuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4,
    )

    correct_answer: str

    explanation: str


class QuizResponse(BaseModel):

    questions: List[QuizQuestion]

    source: str


class SummaryResponse(BaseModel):

    summary: str

    source: str


class LearningPathResponse(BaseModel):

    recommendations: str

    source: str


class HealthResponse(BaseModel):

    status: str