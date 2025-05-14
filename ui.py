import streamlit as st
from llm_service import llm_service

def load_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def render_chat():
    st.title("Tellurium Chatbot")
    load_css()
    init_session()
    container = st.container()

    # display history
    with container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # input loop
    if prompt := st.chat_input("Type your message…"):
        st.session_state.messages.append({"role":"user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                reply = llm_service.send_message(prompt)
                st.markdown(reply)

        st.session_state.messages.append({"role":"assistant", "content": reply})
