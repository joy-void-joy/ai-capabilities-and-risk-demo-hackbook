# FastAPI backend server
# Handles call
# See https://docs.retellai.com/retell-llm/create-llm and https://docs.retellai.com/retell-llm/llm-states for more details

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from contextlib import asynccontextmanager

import pydantic

from .llm import retell, AgentResponse, create_agent


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


@app.get("/")
async def root():
    return RedirectResponse("/index.html")


app.mount("/", StaticFiles(directory="./static"), name="static")
