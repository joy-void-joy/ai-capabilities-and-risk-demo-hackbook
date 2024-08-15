# Head over to https://python.langchain.com/v0.2/docs/integrations/chat/ollama/
# For more information about langchain and Ollama
from retell.types import AgentResponse
from typing import Literal
from collections.abc import AsyncGenerator, Generator

# As before, feel free to use other chat providers:
# from langchain_anthropic import ChatAnthropic
# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from retell import Retell

from contextlib import contextmanager

import pydantic

from .env import env

retell = Retell(api_key=env.str("RETELL_API_KEY"))

begin_sentence = "Hey there!"
agent_prompt = """You are a friendly conversational agent in call with the user. Be short in your answers, and behave as though you were physically talking over the phone with them."""


@contextmanager
def create_agent() -> Generator[AgentResponse, None]:
    agent = retell.agent.create(
        agent_name="test",
        voice_id="openai-Alloy",
        llm_websocket_url=f"http://{env.str('LLM_WS_PUBLIC_SUBDOMAIN')}.{env.str('LLM_WS_PUBLIC_HOSTNAME')}/llm-websocket",
    )

    yield agent

    retell.agent.delete(agent_id=agent.agent_id)


class AnswerConfig(pydantic.BaseModel):
    class Config(pydantic.BaseModel):
        auto_reconnect: bool = True
        call_details: bool = True

    response_id: int
    response_type: Literal["config"] = "config"
    config: Config = Config()


class Utterance(pydantic.BaseModel):
    role: Literal["agent", "user", "system"]
    content: str


class Prompt(pydantic.BaseModel):
    class Message(pydantic.BaseModel):
        role: Literal["assistant", "user", "system"]
        content: str

    messages: list[Message]


class AskLlm(pydantic.BaseModel):
    interaction_type: Literal["reminder_required", "response_required"]
    response_id: int
    transcript: list[Utterance]


class AnswerLlm(pydantic.BaseModel):
    response_id: int
    content: str
    content_complete: bool
    end_call: bool


class LlmClient:
    def __init__(self):
        self.client = ChatOllama(model="llama3.1", temperature=0)

    def prompt(self, request: AskLlm) -> Prompt:
        """Create the prompt to send to Ollama, includes all previous messages in the call along with system instructions"""
        return Prompt(
            messages=[
                Prompt.Message(
                    role="system",
                    content=agent_prompt,
                )
            ]
            + [
                Prompt.Message(
                    role="assistant" if utterance.role == "agent" else "user",
                    content=utterance.content,
                )
                for utterance in request.transcript
            ] + ([
                {
                    "role": "user",
                    "content": "(Now the user has not responded in a while, you would say:)",
                }
            ] if request.interaction_type == "reminder_required" else []),
        )

    def draft_begin_message(self) -> AnswerLlm:
        """First message to send at the beginning of the call"""
        return AnswerLlm(
            response_id=0,
            content=begin_sentence,
            content_complete=True,
            end_call=False,
        )

    async def draft_response(self, request: AskLlm) -> AsyncGenerator[AnswerLlm, None]:
        """
        Answer the user after they have said something
        We just send the prompt to Ollama and stream the response back
        """
        prompt = self.prompt(request)
        stream = self.client.astream(
            prompt.model_dump()["messages"],
        )

        async for chunk in stream:
            yield AnswerLlm(
                response_id=request.response_id,
                content=chunk.content,  # type: ignore
                content_complete=False,
                end_call=False,
            )

        # Send final response with "content_complete" set to True to signal completion
        yield AnswerLlm(
            response_id=request.response_id,
            content="",
            content_complete=True,
            end_call=False,
        )
