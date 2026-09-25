import os
from typing import TypedDict, List
from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from  rag_pipeline import create_vector_store, retrieve_documents
# ------------------------------------
# Create Vector Database
# ------------------------------------
create_vector_store()

# ------------------------------------
# Mock LLM Setting
# ------------------------------------
MOCK_LLM = os.getenv("MOCK_LLM", "1") == "1"

# ------------------------------------
# Pydantic Models
# ------------------------------------
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

# ------------------------------------
# LangGraph State
# ------------------------------------
class SupportState(TypedDict):
    query: str
    intent: str
    context: str
    sources: List[str]
    answer: str
    confidence: float

# ------------------------------------
# Node 1 : Intent Classification
# ------------------------------------
policy_keywords = [
    "delivery",
    "return",
    "refund",
    "membership",
    "tracking",
    "cancel",
    "gift card",
    "support hours"
]

def classify_intent(state: SupportState):
    query = state["query"].lower()
    intent = "general_question"
    for word in policy_keywords:
        if word in query:
            intent = "policy_question"
            break
    state["intent"] = intent
    return state

# ------------------------------------
# Node 2 : Retrieve and Answer
# ------------------------------------
def retrieve_and_answer(state: SupportState):
    results = retrieve_documents(state["query"], top_k=3)
    documents = results["documents"][0]
    ids = results["ids"][0]
    #use only the most relevant document for the answer
    top_document = documents[0]
    top_source = ids[0]
     
    state["context"] = top_document
    state["sources"] = [top_source]

    if MOCK_LLM:
        snippet = top_document[:200]
        state["answer"] = "Based on the retrieved context: " + snippet
        state["confidence"] = 1.0
    return state

# ------------------------------------
# Node 3 : Direct Answer
# ------------------------------------
def direct_answer(state: SupportState):
    state["context"] = ""
    state["sources"] = []
    if MOCK_LLM:
        state["answer"] = "I can only answer questions about Zepto policies right now."
        state["confidence"] = 1.0
    return state

# ------------------------------------
# Routing Function
# ------------------------------------
def router(state: SupportState):
    if state["intent"] == "policy_question":
        return "retrieve"
    return "direct"

# ------------------------------------
# Build LangGraph
# ------------------------------------
builder = StateGraph(SupportState)

builder.add_node("classify", classify_intent)
builder.add_node("retrieve", retrieve_and_answer)
builder.add_node("direct", direct_answer)

builder.set_entry_point("classify")
builder.add_conditional_edges(
    "classify",
    router,
    {
        "retrieve": "retrieve",
        "direct": "direct"
    }
)
builder.add_edge("retrieve", END)
builder.add_edge("direct", END)

graph = builder.compile()

# ------------------------------------
# FastAPI App
# ------------------------------------
app = FastAPI(title="Zepto AI Support Assistant")

 
@app.get("/")
def home():
    return {"message": "Zepto AI Support Assistant is running."}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    state = SupportState(
        query=request.query,
        intent="",
        context="",
        sources=[],
        answer="",
        confidence=0.0
    )
    result = graph.invoke(state)

    return QueryResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )

# ------------------------------------
# Run FastAPI Server
# ------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True)