from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import (
    ExplainRequest,
    QARequest,
    QuizRequest,
    SummaryRequest,
    LearningPathRequest,
    ExplainResponse,
    QAResponse,
    QuizResponse,
    SummaryResponse,
    LearningPathResponse,
    HealthResponse,
)

from explanation_module import explain_concept
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description=(
        "AI-powered educational assistant for Q&A, explanations, "
        "quiz generation, summarization, and personalized learning paths."
    ),
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


# HTML templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request":request},
    )


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok")


@app.post("/explain", response_model=ExplainResponse)
async def explain(request: ExplainRequest):
    return await explain_concept(
        request.text,
        request.level,
    )


@app.post("/qa", response_model=QAResponse)
async def qa(request: QARequest):
    return await answer_question(
        request.text,
        request.level,
    )


@app.post("/quiz", response_model=QuizResponse)
async def quiz(request: QuizRequest):
    return await generate_quiz(
        request.text,
        request.level,
    )


@app.post("/summarize", response_model=SummaryResponse)
async def summarize(request: SummaryRequest):
    return await summarize_text(
        request.text,
        request.level,
    )


@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse,
)
async def learning_path(request: LearningPathRequest):
    return await get_learning_recommendations(
        request.text,
        request.level,
        request.weeks,
    )