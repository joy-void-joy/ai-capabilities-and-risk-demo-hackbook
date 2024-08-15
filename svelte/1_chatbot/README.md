![2024-08-15-120804_1207x387_scrot](https://github.com/user-attachments/assets/b883cddc-2744-4599-9311-1653e83a4989)

Very simple template for chatting with a bot for you to use during the [AI capabilities and risks demo-jam hackathon](https://www.apartresearch.com/event/ai-capabilities-and-risks-demo-jam)

# Running this template

## Using docker-compose

Once you have docker-compose installed, using: `docker-compose up --build` will run the template. Then head to `localhost:4444` and you can start hacking away!
Changes you make to files locally will reflect in the app directly.
Be sure to put your own values of `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` in .env.local if you want to use openai or anthropic.

## Locally

You can also run this template locally:

- install [ollama](https://ollama.com/)
- run `ollama serve` on a different terminal
- On a different terminal still, run `ollama pull llama3.1`
- install [bun](https://bun.sh/)
- Do: `bun install`
- Finally you can run this template by doing: `bun dev`

# Understanding the code

The main part of the code lies in src/routes/+page.ts
Note that we call the ollama server from the frontend in order to simplify the calling procedure.

# Using this template for creating a submission

You can modify the code and use any services you want. Be sure to:

- Document any and all API used, and indicate how to get API keys to put them in .env.local
  - It will be easier to judge your submission if you use APIs that provide free-tiers, or use local models
- Include ways for reviewers to test your demo easily. This can include thorough-and-simple deployment instructions or modifying the docker-compose at your convenience.
- Follow the [submission template](https://www.apartresearch.com/event/ai-capabilities-and-risks-demo-jam#submission) to validate your submission
- Stick around after your submission to review other projects - you need to review your assigned projects for your submission to be valid
