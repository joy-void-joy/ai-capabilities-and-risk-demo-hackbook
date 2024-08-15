FROM oven/bun:1
WORKDIR /static
WORKDIR /app

COPY package.json ./
COPY bun.lockb ./
RUN bun install
USER bun
