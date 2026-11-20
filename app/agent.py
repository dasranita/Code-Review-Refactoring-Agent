from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from app.config import get_settings

class AgentState(TypedDict, total=False):
    code: str
    language: str
    goals: str
    include_refactor: bool
    review: str
    refactored_code: str

def _model():
    settings = get_settings()
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file.")
    return ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=0)

def review_node(state: AgentState) -> AgentState:
    prompt = f"""You are a careful senior software engineer performing a code review.
Language: {state['language']}
Review goals: {state['goals']}
Review the code below. Identify concrete issues, explain impact, and suggest fixes.
Organize the answer into: Summary, Findings (severity + location + explanation), and Recommendations.
Do not claim to have executed the code.

CODE:
```{state['language']}
{state['code']}
```"""
    answer = _model().invoke(prompt)
    return {"review": str(answer.content)}

def refactor_node(state: AgentState) -> AgentState:
    prompt = f"""Refactor the following {state['language']} code to address the review.
Preserve intended behavior, avoid unnecessary dependencies, and return ONLY the complete
refactored source code in a fenced code block. If a safe refactor is not possible, explain why.

REVIEW:
{state['review']}

CODE:
```{state['language']}
{state['code']}
```"""
    answer = _model().invoke(prompt)
    return {"refactored_code": str(answer.content)}

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("review", review_node)
    graph.add_node("refactor", refactor_node)
    graph.set_entry_point("review")
    graph.add_conditional_edges(
        "review",
        lambda state: "refactor" if state.get("include_refactor") else END,
        {"refactor": "refactor", END: END},
    )
    graph.add_edge("refactor", END)
    return graph.compile()

agent_graph = build_graph()
