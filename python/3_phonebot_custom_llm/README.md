This template is very similar to 2_phonebot, but allows you to customize the way you call the LLM model fully if you need more customization.
Consult ../2_phonebot/README.md for an introduction.
Changes to files compared to 2_phonebot include:

- Modifying docker-compose to run a local Ollama model, and a localtunnel service to expose a public URL that retell can access
- Changes to python_phonebot/llm.py to call a custom Ollama model
- Changes to python_phonebot/server.py to handle the call by interacting with llm.py

# Running this template

Like for 2_phonebot, you will need to populate .env.local with RETELL_API_KEY by heading to https://beta.retellai.com/dashboard/apiKeys and getting one there.
Also ensure that the name in LLM_WS_PUBLIC_SUBDOMAIN is unique, for instance by using an UUID generator.

## Using docker-compose

Run this template with `docker-compose up --build`. Then head to `localhost:4444` and you can start hacking away! Changes you make to files locally will reflect in the app directly, you will need to refresh your browser for changes you make to the frontend.

## Locally

- Llama model
  - Using [ollama](https://ollama.com/download), do `ollama serve` and leave it running
  - In another terminal, run `ollama pull llama3.1` to download the model
- Localtunnel
  - Install [localtunnel](http://localtunnel.me/)
  - In a terminal, run `lt --port 4444 -s 52bf3247d35d4e1cab6ea00eccf52a82` and leave it running
- Frontend
  - Head to the frontend folder: `cd frontend`
  - Install [bun](https://bun.sh/)
  - `bun install`
  - Run `bun dev`
- Backend
  - install [poetry](https://python-poetry.org/)
  - Do: `poetry install`
  - Run this template by doing: `fastapi dev --port 4444 python_phonebot/server.py`
