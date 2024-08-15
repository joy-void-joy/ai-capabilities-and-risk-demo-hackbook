# FastAPI backend server
# Handles call and LLM websockets
# See https://docs.retellai.com/integrate-llm/overview and https://github.com/RetellAI/retell-custom-llm-python-demo to get started

from retell.types import AgentResponse

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

import asyncio
from contextlib import asynccontextmanager

import pydantic

from .llm import (
    retell,
    LlmClient,
    create_agent,
    AnswerConfig,
    AskLlm,
)


class Globals(pydantic.BaseModel):
    agent: AgentResponse | None = None


globals = Globals()


@asynccontextmanager
async def lifespan(app: FastAPI):
    with create_agent() as agent:
        globals.agent = agent
        yield


app = FastAPI(lifespan=lifespan)


@app.post("/api/call")
async def call():
    if not globals.agent:
        raise HTTPException(status_code=503, detail="Agent not ready")

    return retell.call.create_web_call(agent_id=globals.agent.agent_id)


@app.websocket("/llm-websocket/{call_id}")
async def websocket_handler(websocket: WebSocket, call_id: str):
    await websocket.accept()
    llm_client = LlmClient()

    # Send optional config to Retell server
    config = AnswerConfig(
        response_id=1,
    )
    await websocket.send_json(config.model_dump())

    # Send first message to signal ready of server
    first_event = llm_client.draft_begin_message()
    await websocket.send_json(first_event.model_dump())

    # response_id is used to keep track of the current response accross different events
    response_id = 0
    async def handle_message(request_json):
        nonlocal response_id

        # There are 5 types of interaction_type: call_details, pingpong, update_only, response_required, and reminder_required.
        # Not all of them need to be handled, only response_required and reminder_required.
        match request_json["interaction_type"]:
            case "call_details":
                return

            case "ping_pong":
                await websocket.send_json(
                    {
                        "response_type": "ping_pong",
                        "timestamp": request_json["timestamp"],
                    }
                )
                return

            case "update_only":
                return

            case "response_required" | "reminder_required":
                response_id = request_json["response_id"]
                request = AskLlm(
                    interaction_type=request_json["interaction_type"],
                    response_id=response_id,
                    transcript=request_json["transcript"],
                )

                async for event in llm_client.draft_response(request):
                    await websocket.send_json(event.model_dump())

                    if request.response_id < response_id:
                        break  # new response needed, abandon this one

    async for data in websocket.iter_json():
        asyncio.create_task(handle_message(data))


@app.get("/")
async def root():
    return RedirectResponse("/index.html")


app.mount("/", StaticFiles(directory="./static"), name="static")
