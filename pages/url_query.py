import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings

st.set_page_config(layout="wide")

def process_input(urls, question):
    model_local = Ollama(model="llama2-uncensored")

    urls_list = urls.split("\n")
    docs = [WebBaseLoader(url).load() for url in urls_list]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"]
    )
    doc_splits = text_splitter.split_documents(docs_list)

    vectorstore = Chroma.from_documents(
        documents=doc_splits, collection_name="rag-chroma", embedding=OllamaEmbeddings()
    )
    retriever = vectorstore.as_retriever()

    after_rag_template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    """
    after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
    after_rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | after_rag_prompt
        | model_local
        | StrOutputParser()
    )
    return after_rag_chain.invoke(question)


st.title("Query URLs with Ollama")

urls = st.text_input("Enter URLs separated by new lines")
question = st.text_input("Question")

query = st.button("Query Documents")

with st.container(height=500, border=True):
    if "url_messages" not in st.session_state:
        st.session_state.url_messages = []

    for message in st.session_state.url_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if query:
        user_message = st.chat_message("user")
        user_message.write(f"{question}")
        st.session_state.url_messages.append({"role": "user", "content": question})

        with st.spinner("Processing..."):
            
            answer = process_input(urls, question)
            bot_message = st.chat_message("assistant")
            st.session_state.url_messages.append(
                {"role": "assistant", "content": answer}
            )
            bot_message.write(f"{answer}")