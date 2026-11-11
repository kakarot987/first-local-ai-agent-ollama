"""Optional FastAPI wrapper around the same Ollama client."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ollama_client import generate

app = FastAPI(title="Local Ollama Chatbot")


class AskRequest(BaseModel):
    prompt: str = Field(min_length=1)


@app.post("/ask")
def ask(payload: AskRequest) -> dict[str, str]:
    try:
        return {"response": generate(payload.prompt)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
