import streamlit as st
import time
from chatbot_utilities.helpers import get_rag_agent
from dotenv import load_dotenv
import os
from langchain.schema import HumanMessage, AIMessage

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY_PERSONAL"]

retrieval_agent = get_rag_agent(
    model="gpt-4o-mini",
    index_name="langchain-chabot",
    embeddings="text-embedding-3-small",
)
st.header("Langchain Docs Chatbot")

st.chat_message("assistant").markdown("Hello, How can I help you?")

if "user_query" not in st.session_state:
    st.session_state.user_query = []

if "bot_response" not in st.session_state:
    st.session_state.bot_response = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for user_query, generated_response in zip(
    st.session_state.user_query, st.session_state.bot_response
):
    st.chat_message("user").markdown(user_query)
    st.chat_message("assistant").markdown(generated_response)

input_question = st.chat_input("Enter your query")

if input_question:
    answer = None
    with st.spinner("Wait for it..."):
        st.chat_message("user").markdown(input_question)
        st.session_state.user_query.append(input_question)
        answer = retrieval_agent.invoke(
            {"input": input_question, "chat_history": st.session_state.chat_history}
        )["answer"]
        st.chat_message("assistant").markdown(answer)
        st.session_state.bot_response.append(answer)
        st.session_state.chat_history.append(HumanMessage(content=input_question))
        st.session_state.chat_history.append(AIMessage(content=answer))
