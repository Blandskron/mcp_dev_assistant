from sse_starlette.sse import EventSourceResponse
from fastapi import Request
from .llm import get_code_from_prompt
import asyncio

async def stream_response(prompt: str):
    yield "data: Generando código...\n\n"
    await asyncio.sleep(1)
    code = get_code_from_prompt(prompt)
    for line in code.splitlines():
        yield f"data: {line}\n\n"
        await asyncio.sleep(0.1)

async def sse_handler(request: Request):
    prompt = request.query_params.get("prompt", "")
    return EventSourceResponse(stream_response(prompt))
