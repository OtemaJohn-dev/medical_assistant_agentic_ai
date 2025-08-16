from langchain_groq import ChatGroq
from dotenv import dotenv_values
import streamlit as st

config = dotenv_values(".env")

if "llm" not in st.session_state:
    llm = ChatGroq(
        model=config["GROQ_API_MODEL"],
        api_key=config["GROQ_API_KEY"],
        temperature=0.1,
        max_tokens=131072,
    )
    st.session_state.llm = llm
else:
    llm = st.session_state.llm