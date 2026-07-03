# 🤝 Personalized Networking Assistant

**Networking Assistant** is a high-tech, AI-powered solution designed for event attendees, conference speakers, and networking professionals who want instant, contextual conversation starters and topic intelligence.

This repository combines a robust FastAPI backend, AI-driven theme extraction, GPT-2 based starter generation, fact-checking support, session history, feedback telemetry, and a sleek Streamlit frontend.

## 🚀 What this project does

*   Extracts meaningful event themes from raw event descriptions using `transformers` zero-shot classification.
*   Generates polished conversation starters for networking events using GPT-2.
*   Validates topic relevance through Wikipedia-backed fact-checking.
*   Provides a responsive Streamlit frontend for rapid interaction.
*   Maintains recent session history and collects feedback for continuous improvement.

## 🧠 Architecture Overview

This application is built as a modular backend + frontend system:

1.  **FastAPI backend** serving AI endpoints and telemetry.
2.  **Streamlit frontend** for user interactions and visualization.
3.  **Transformer pipelines** for event theme extraction and text generation.
4.  **Wikipedia REST API** for fact-checking and topic verification.
5.  **JSON persistence** for history and feedback storage.

## 📦 Core Components

### Backend

*   `app/main.py` — FastAPI app config and startup entry.
*   `app/routers/conversation.py` — API routes for analysis, generation, fact checking, history, and feedback.
*   `app/services/event_analyzer.py` — zero-shot classification with `typeform/distilbert-base-uncased-mnli`.
*   `app/services/topic_generator.py` — GPT-2 generation with prompt engineering and cleaning logic.
*   `app/services/fact_checker.py` — Wikipedia-based query verification and caching.
*   `app/services/history_logger.py` / `app/services/feedback_logger.py` — lightweight JSON-backed telemetry.
*   `app/models/schemas.py` — Pydantic request/response validation.

### Frontend

*   `frontend/app.py` — Streamlit UI with event input, topic display, fact verification, and interaction history.

## ⚙️ Technology Stack

*   Python 3.12+
*   FastAPI
*   Streamlit
*   Transformers
*   Hugging Face model hubs
*   Requests
*   Uvicorn

## 📁 File Structure

```

networking-assistant/
├── app/
│   ├── config.py
│   ├── main.py
│   ├── models/
│   │   └── schemas.py
│   ├── routers/
│   │   └── conversation.py
│   └── services/
│       ├── event_analyzer.py
│       ├── fact_checker.py
│       ├── feedback_logger.py
│       ├── history_logger.py
│       ├── storage.py
│       └── topic_generator.py
├── frontend/
│   └── app.py
├── history.json
├── feedback.json
├── requirements.txt
└── README.md
  
```

## 🛠️ Setup Requirements

Install project dependencies in a Python virtual environment:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Important:** This repository uses large transformer models, so ensure you have sufficient disk space and memory.

## 🚀 Run the Application

1.  Start the backend API:
2.  Open a new terminal and start the frontend:
3.  Navigate to `http://localhost:8501` in your browser to use the interface.

## 🔌 REST API Endpoints

| Endpoint | Method | Payload | Description |
| --- | --- | --- | --- |
| `/analyze-event` | POST | `{ "description": "..." }` | Extracts top event themes from raw text. |
| `/generate-conversation` | POST | `{ "description": "...", "interests": ["AI", "finance"] }` | Generates conversation starters based on event themes and user interests. |
| `/fact-check` | POST | `{ "query": "blockchain" }` | Returns a short Wikipedia summary for a topic. |
| `/history` | GET | none | Returns recent session history. |
| `/feedback` | POST | `{ "suggestion": "...", "action": "like" }` | Logs user feedback for a generated starter. |
| `/feedback-log` | GET | none | Returns the latest feedback activity. |

## 🎯 Key Features

*   Theme extraction using zero-shot classification.
*   Customized conversation starter generation tuned for networking events.
*   Automatic validation of extracted themes via Wikipedia lookup.
*   Feedback capture to monitor quality and user sentiment.
*   Lightweight JSON persistence for history and session logs.
*   Reproducible generation with a fixed GPT-2 seed.

## ⚠️ Limitations & Known Constraints

1.  The GPT-2 based conversation generator may occasionally produce generic or slightly tangential suggestions.
2.  Fact-checking depends on Wikipedia availability and may fail under network outages.
3.  Model loading is heavy: the zero-shot classifier and GPT-2 model each require significant RAM and disk space.
4.  There is no production-grade database; history and feedback are stored in local JSON files.
5.  There is no authentication or rate limiting implemented in this prototype.
6.  The app is designed for demo/educational use, not secure enterprise deployment.

## 🧪 Testing

The project includes test coverage for core backend services and router behavior.

```
pytest
```

If you want to focus on one file:

```
pytest tests/test_event_analyzer.py
```

## 🛡️ Best Practices

*   Use a dedicated virtual environment for this project.
*   Keep `venv/` ignored in Git.
*   Do not commit large model cache or temporary files.
*   Use the built-in `.gitignore` for safe version control.

## 📌 Notes for Contributors

To add a new feature or improve quality, consider:

*   Upgrading the text generator to a modern conversational model.
*   Replacing JSON persistence with a database.
*   Adding authentication and secure API access.
*   Improving the frontend with additional controls, filtering, and analytics.

## 💡 Enhancement Opportunities

*   Integrate a scalable vector database for richer context-aware generation.
*   Introduce conversation state tracking and user profile personalization.
*   Swap GPT-2 for a newer encoder-decoder or instruction-tuned model.
*   Add caching for API responses to reduce repeated fact-check traffic.
*   Build a production deployment pipeline with Docker and CI/CD.

## 📍 How to Extend

Suggested development path:

1.  Refactor `app/services` into smaller service classes.
2.  Move model names and API URLs into environment variables.
3.  Implement validation or sanitization for all user inputs.
4.  Expand the Streamlit UI with multi-step workflows.

## 👥 Team Members

*   Majeti NagaSai Rishi
*   Kotha Meghana
*   Riya
*   Buddavarapu Taraka Venkata Manikanta