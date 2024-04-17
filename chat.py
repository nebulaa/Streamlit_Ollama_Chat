import streamlit as st
from langchain_community.llms import Ollama

llm = Ollama(model="llama2-uncensored")

st.title("Query with Ollama")

with st.chat_message("assistant"):
    st.write("Enter your question in the chatbox.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Enter your question here.")

if prompt:
    user_message = st.chat_message("user")
    user_message.write(f"{prompt}")
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Processing..."):
        answer = llm.invoke(prompt)
        bot_message = st.chat_message("assistant")
        st.session_state.messages.append({"role": "assistant", "content": answer})
        bot_message.write(f"{answer}")
        