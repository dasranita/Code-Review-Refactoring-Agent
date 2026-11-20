from pydantic import BaseModel, Field

class ReviewRequest(BaseModel):
    code: str = Field(..., min_length=1, description="Source code to review")
    language: str = Field(default="python", min_length=1)
    goals: str = Field(default="Find bugs, security issues, and maintainability problems.")
    include_refactor: bool = True

class ReviewResponse(BaseModel):
    review: str
    refactored_code: str | None = None
