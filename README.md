# EduGenie

EduGenie is an AI-powered educational assistant built with:

- FastAPI
- Google Gemini
- HTML
- CSS
- JavaScript
- Optional LaMini-Flan-T5 local model

## Features

EduGenie supports:

1. Question & Answer
2. Concept Explanation
3. Quiz Generation
4. Text Summarization
5. Personalized Learning Paths

---

# Project Structure

```text
EduGenie/
│
├── main.py
├── config.py
├── ai_client.py
├── schemas.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── app.js
│
└── tests/
    └── test_api.py