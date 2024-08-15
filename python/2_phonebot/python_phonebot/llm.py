# Head over to https://python.langchain.com/v0.2/docs/integrations/chat/ollama/
# For more information about langchain and Ollama
from collections.abc import Generator
from retell.types import AgentResponse

from contextlib import contextmanager
from retell import Retell
from .env import env

retell = Retell(api_key=env.str("RETELL_API_KEY"))

begin_sentence = "Hey there!"
agent_prompt = """You are a friendly conversational agent in call with the user. Be short in your answers, and behave as though you were physically talking over the phone with them."""


@contextmanager
def create_agent() -> Generator[AgentResponse, None]:
    # Create an LLM
    # You can personalize this with Multiple States, such as in https://docs.retellai.com/retell-llm/llm-states
    llm = retell.llm.create(
        begin_message=begin_sentence,
        general_prompt=agent_prompt,
        model="claude-3.5-sonnet",
    )

    agent = retell.agent.create(
        agent_name="test",
        voice_id="openai-Alloy",
        llm_websocket_url=llm.llm_websocket_url,
    )

    yield agent

    retell.llm.delete(llm.llm_id)
    retell.agent.delete(agent.agent_id)
