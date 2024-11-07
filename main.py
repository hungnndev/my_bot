# from openai import OpenAI
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
import random
import time

st.title("HR Chatbot")
OPENAI_API_KEY='<key from https://platform.openai.com>'

chat = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model='gpt-3.5-turbo'
)

messages = []
source_knowledge = ''

with open('hr_policy.txt', 'r') as file:
    source_knowledge = file.read().replace('\n', '')

# Streamed response emulator
def response_generator(query):


    augmented_prompt = f"""Using the contexts below, answer the query.

    Contexts:
    {source_knowledge}

    Query: {query}"""

    prompt = HumanMessage(
        content=augmented_prompt
    )
    messages.append(prompt)
    res = chat(messages)
    messages.append(res)

    response = res.content
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        text = ''
        for m in st.session_state.messages:
            if m == st.session_state.messages[-1] and m['role'] == 'user':
                text = m['content']
        res = response_generator(text)
        response = st.write_stream(res)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
