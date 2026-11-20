from fastapi import FastAPI, HTTPException

from app.agent import agent_graph
from app.schemas import ReviewRequest, ReviewResponse


app = FastAPI(
    title="Code Review & Refactoring Agent",
    description="An AI-powered code review and refactoring API built with LangGraph.",
    version="1.0.0",
)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


@app.post("/review", response_model=ReviewResponse, tags=["agent"])
def review_code(request: ReviewRequest):
    try:
        result = agent_graph.invoke(
            {
                "code": request.code,
                "language": request.language,
                "goals": request.goals,
                "include_refactor": request.include_refactor,
            }
        )
        return ReviewResponse(
            review=result["review"],
            refactored_code=result.get("refactored_code"),
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Agent execution failed: {exc}") from exc
