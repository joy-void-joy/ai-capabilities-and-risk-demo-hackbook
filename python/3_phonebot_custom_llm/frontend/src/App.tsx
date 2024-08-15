import { RetellWebClient } from "retell-client-js-sdk"

const retellWebClient = new RetellWebClient()

type CallResponse = {
  access_token: string
}

const call: CallResponse = await (
  await fetch("/api/call", {
    method: "POST",
  })
).json()

async function startCall() {
  await retellWebClient.startCall({
    accessToken: call.access_token,
  })
}

export function App() {
  return <button onClick={() => startCall()}>Call</button>
}
