# Code Review & Refactoring Agent

An AI-powered code review and refactoring service built with **LangGraph**, **FastAPI**, and **OpenAI**. It accepts source code, produces a structured review, and can suggest a refactored version.

## Features

- LangGraph workflow with review and optional refactoring nodes
- FastAPI REST API with interactive Swagger UI
- Findings organized by severity, location, impact, and recommendations
- Configurable model through environment variables
- Pytest API tests and GitHub Actions CI workflow
- Does not execute submitted source code

## Architecture

```text
Client
  |
  v
FastAPI POST /review
  |
  v
LangGraph StateGraph
  |
  v
Review node (LLM)
  |
  +---- include_refactor=false ---> Response
  |
  v
Refactor node (LLM)
  |
  v
Response: review + refactored_code
```

## Requirements

- Python 3.10+
- An OpenAI API key

## Installation

```bash
git clone https://github.com/dasranita/code-review-refactoring-agent.git
cd code-review-refactoring-agent

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Create your local environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set `OPENAI_API_KEY`. Never commit `.env` or paste your API key into source code.

## Run the API

```bash
uvicorn app.main:app --reload
```

- API base: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json
- Health check: http://127.0.0.1:8000/health

## Example request

```bash
curl -X POST "http://127.0.0.1:8000/review" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def divide(a, b):\\n    return a / b",
    "language": "python",
    "goals": "Check correctness, edge cases, and readability.",
    "include_refactor": true
  }'
```

Example response shape:

```json
{
  "review": "Summary: ... Findings: ... Recommendations: ...",
  "refactored_code": "```python\\ndef divide(a, b):\\n    ...\\n```"
}
```

## Run tests

```bash
pytest -q
```

Tests cover the health endpoint, request validation, and the review endpoint's configuration behavior. The LLM-backed path requires a valid API key.

## API

### `GET /health`

Returns service status.

### `POST /review`

Request body:

| Field | Type | Default | Description |
|---|---|---|---|
| `code` | string | required | Source code to review |
| `language` | string | `python` | Programming language |
| `goals` | string | general review goals | Review focus |
| `include_refactor` | boolean | `true` | Whether to run the refactoring node |

Response contains `review` and optional `refactored_code`.

## Project structure

```text
code-review-refactoring-agent/
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── main.py
│   └── schemas.py
├── tests/
│   └── test_api.py
├── .github/workflows/tests.yml
├── .env.example
├── .gitignore
├── openapi.json
├── requirements.txt
└── README.md
```

## Security notes

- Treat model output as suggestions; review changes before applying them.
- This service does not execute submitted code.
- Do not send secrets, credentials, or private source code unless your organization's policies allow it.
- Add authentication, rate limiting, request-size limits, and audit logging before public production deployment.
- Configure provider-side data handling according to your requirements.

## GitHub publication

Create a **public** repository named `code-review-refactoring-agent` under `dasranita`, then push this project:

```bash
git init
git add .
git commit -m "Build LangGraph code review and refactoring agent"
git branch -M main
git remote add origin https://github.com/dasranita/code-review-refactoring-agent.git
git push -u origin main
```

## Assessment submission checklist

- [ ] Public GitHub repository URL added to the assessment
- [ ] README installation and test instructions verified
- [ ] OpenAPI specification included
- [ ] `.env` configured locally (not committed)
- [ ] `pytest -q` passes
- [ ] Record a short Loom/YouTube demo showing `/docs` and a sample `/review` request
