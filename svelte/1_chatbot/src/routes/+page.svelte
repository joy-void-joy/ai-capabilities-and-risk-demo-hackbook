<!--
  This is a bit ugly, we are using the ollama package directly in the frontend instead of the backend (e.g. by using [form actions](https://kit.svelte.dev/docs/form-actions))
  However, this allows us to directly modify the messages without having to set up websockets or server-side-events
-->

<script lang="ts">
  import { PUBLIC_OLLAMA_HOST } from "$env/static/public"
  import { ChatOllama } from "@langchain/ollama"

  /* We are using Ollama however, you can also use openAI or Anthropic:
  import { ChatOpenAI } from "@langchain/openai"
  import { ChatAnthropic } from "@langchain/anthropic"
  */

  type Message = { type: "user" | "assistant"; content: string }

  const llm = new ChatOllama({
    model: "llama3.1",
    temperature: 0,
    maxRetries: 2,
  })

  let currentMessage = ""
  let messages: Message[] = []

  async function answerMessage() {
    // We modify messages that way to update the UI
    messages = [...messages, { type: "user", content: currentMessage }]
    currentMessage = ""

    const response = await llm.invoke(messages)
    messages = [
      ...messages,
      { type: "assistant", content: response.content as string },
    ]
  }
</script>

<h1>Chatbot</h1>
<div id="messages">
  {#each messages as message}
    <h2>{message.type}</h2>
    <p>{message.content}</p>
  {/each}
</div>

<form on:submit|preventDefault={answerMessage}>
  <input type="text" bind:value={currentMessage} placeholder="Type a message" />
  <button>Submit</button>
</form>

<style>
  form {
    display: flex;
  }

  input {
    width: 90vw;
    padding: 3px;
    border-radius: 5px;
    outline: none;
    height: 50px;
  }

  button {
    background: none;
    border: none;
    pointer-events: auto;
    display: inline;
    color: navy;
  }

  #messages {
    position: relative;
    margin: 0px;
    flex: 1 94%;
    flex-wrap: wrap;
    align-items: flex-start;
    align-content: flex-start;
    overflow: auto;
  }
</style>
