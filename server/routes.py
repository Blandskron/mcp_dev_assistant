from fastapi import APIRouter, Request
from .llm import get_code_from_prompt
from .sse import sse_handler

router = APIRouter()

@router.get("/code")
async def generate_code(prompt: str):
    if not prompt:
        return {"error": "Prompt vacío"}
    try:
        return {"code": get_code_from_prompt(prompt)}
    except Exception as e:
        return {"error": str(e)}

@router.get("/stream")
async def stream_code(request: Request):
    return await sse_handler(request)
