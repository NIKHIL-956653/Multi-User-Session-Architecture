import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.session_manager import create_session, get_chat_history, get_existing_session
from app.llm_engine import chat_with_history

st.set_page_config(
    page_title="Multi-User AI Chat",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-User AI Chat Assistant")
st.caption("Each user gets their own private chat history stored in MongoDB")

# Login
if "session_id" not in st.session_state:
    st.subheader("👤 Login")
    username = st.text_input("Enter your name to start chatting:")
    if st.button("Start Chat 🚀"):
        if username:
            # Check if user already exists
            existing_session = get_existing_session(username)
            if existing_session:
                st.session_state.session_id = existing_session
                st.info("Welcome back! Loading your previous chat...")
            else:
                session_id = create_session(username)
                st.session_state.session_id = session_id
            st.session_state.username = username
            st.rerun()
        else:
            st.warning("Please enter your name!")

else:
    # Sidebar
    with st.sidebar:
        st.success(f"👤 {st.session_state.username}")
        st.caption(f"Session: {st.session_state.session_id[:8]}...")
        st.divider()
        st.info("Your chat history is saved in MongoDB. Come back anytime!")
        if st.button("🚪 Logout"):
            del st.session_state.session_id
            del st.session_state.username
            st.rerun()

    # Chat history
    history = get_chat_history(st.session_state.session_id)
    
    if not history:
        st.info("No messages yet — ask me anything!")
    
    for msg in history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["message"])
        else:
            st.chat_message("assistant").write(msg["message"])

    # Input
    user_input = st.chat_input("Ask anything...")
    if user_input:
        st.chat_message("user").write(user_input)
        with st.spinner("Thinking..."):
            response = chat_with_history(
                st.session_state.session_id,
                user_input
            )
        st.chat_message("assistant").write(response)
        st.rerun()