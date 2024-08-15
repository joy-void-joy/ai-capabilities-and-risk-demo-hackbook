# Head over to https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
# For more information about how streamlit and this template works
#
# Adapted from https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps, MIT License

import streamlit as st
import pydantic

# We can directly import subfolders by naming them here
from lib.llm import llm

st.title("Chatbot")


class Message(pydantic.BaseModel):
    role: str
    content: str


def display_message(message: Message):
    with st.chat_message(message.role):
        st.markdown(message.content)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    display_message(message)

# React to user input
if prompt := st.chat_input("Enter your message"):
    # Add user message to chat history
    user_message = Message(role="user", content=prompt)
    st.session_state.messages.append(user_message)
    display_message(user_message)

    response = llm.invoke(
        [
            (
                "system",
                "You are a helpful assistant.",
            ),
        ]
        + [(message.role, message.content) for message in st.session_state.messages]
    )
    if isinstance(response.content, str):
        ai_message = Message(role="assistant", content=response.content)
        st.session_state.messages.append(ai_message)
        display_message(ai_message)
