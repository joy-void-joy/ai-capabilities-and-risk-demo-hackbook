Template for calling with a bot for you to use during the [AI capabilities and risks demo-jam hackathon](https://www.apartresearch.com/event/ai-capabilities-and-risks-demo-jam)

# Running this template

Populate .env.local with RETELL_API_KEY by heading to https://beta.retellai.com/dashboard/apiKeys and getting one there.

## Using docker-compose

Once you have docker-compose installed, using: `docker-compose up --build` will run the template. Then head to `localhost:4444` and you can start hacking away!
Changes you make to files locally will reflect in the app directly, you will need to refresh your browser for changes you make to the frontend.

## Locally

You can also run this template locally:

- Frontend
  - Head to the frontend folder: `cd frontend`
  - Install [bun](https://bun.sh/)
  - `bun install`
  - Run `bun dev`
- Backend
  - install [poetry](https://python-poetry.org/)
  - Do: `poetry install`
  - Run this template by doing: `fastapi dev --port 4444 python_phonebot/server.py`

# Understanding the code

The code is segmented in two parts:

- Frontend: The frontend is built in React and is a simple button to establish web-call
  - frontend/src/App.tsx: Main code for the application
- Backend
  - python_phonebot/server.py: Server code to handle the call
  - python_phonebot/llm.py: Code for the behaviour of the agent during the call

If you want to use a custom LLM besides what retell offer, you will need to provide a custom endpoint. A template for this is available at the `3_phonebot_custom_llm` folder.

# Using this template for creating a submission

You can modify the code and use any services or programming language you want. Be sure to:

- Document any and all API used, and indicate how to get API keys to put them in .env.local
  - It will be easier to judge your submission if you use APIs that provide free-tiers, or use local models
- Include ways for reviewers to test your demo easily. This can include thorough-and-simple deployment instructions or modifying the docker-compose at your convenience.
- Follow the [submission template](https://www.apartresearch.com/event/ai-capabilities-and-risks-demo-jam#submission) to validate your submission
- Stick around after your submission to review other projects - you need to review your assigned projects for your submission to be valid
