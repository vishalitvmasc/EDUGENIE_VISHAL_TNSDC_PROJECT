import os

# Make tests independent of a real Gemini API key.
os.environ["DEMO_MODE"] = "true"

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }


def test_qa_demo():

    response = client.post(
        "/qa",
        json={
            "text": "What is Python?",
            "level": "beginner",
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["source"]
        == "Demo mode"
    )


def test_quiz_demo():

    response = client.post(
        "/quiz",
        json={
            "text": "Photosynthesis",
            "level": "beginner",
        },
    )

    assert response.status_code == 200

    assert len(
        response.json()["questions"]
    ) == 3


def test_summary_demo():

    response = client.post(
        "/summarize",
        json={
            "text":
                "This is a short educational passage.",
            "level":
                "beginner",
        },
    )

    assert response.status_code == 200