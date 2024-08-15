# Head over to https://python.langchain.com/v0.2/docs/integrations/chat/ollama/
# For more information about langchain and Ollama

from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from environs import Env

# We export all environment variables from .envs in the os.environs variable
env = Env()
env.read_env(".env.local")
env.read_env()

llm = ChatOllama(
    model="llama3.1",
    temperature=0,
)

# You might want to use GPT or Claude instead, in which case you would follow:
# https://python.langchain.com/v0.2/docs/integrations/chat/openai/ or https://python.langchain.com/v0.2/docs/integrations/chat/anthropic/
#
# llm = ChatAnthropic(
# model="claude-3-5-sonnet-20240620",
# temperature=0,
# )
#
# Or
#
# llm = ChatOpenAI(
# model="gpt-4o",
# )
#
# Be sure to set ANTHROPIC_API_KEY or OPENAI_API_KEY in .env.local and indicate to the user that they need to do so in the README
