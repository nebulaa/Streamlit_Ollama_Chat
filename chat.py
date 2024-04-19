import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

def process_answer(prompt):
    model_local = Ollama(model="llama2-uncensored")

    after_rag_chain = (
        model_local
        | StrOutputParser()
    )
    return after_rag_chain.invoke(prompt)

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
        bot_message = st.chat_message("assistant")
        answer = process_answer(prompt)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        bot_message.write(f"{answer}")
        