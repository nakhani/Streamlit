# app.py
import streamlit as st
from sqlmodel import Session as DBSession
from db.engine import get_engine
from settings import DB_URL, EDEN_PROVIDER, EDEN_MODEL, EDENAI_API_KEY
from auth.service import AuthService
from auth.widgets import AuthWidget
from ai.eden_client import EdenClient
from chat.service import ChatService

st.set_page_config(page_title="Najmeh Chatbot", page_icon="✨", layout="centered")

# Initialize services
engine = get_engine(DB_URL)
db = DBSession(engine)
auth = AuthService(db)
eden = EdenClient(api_key=EDENAI_API_KEY, provider=EDEN_PROVIDER, model=EDEN_MODEL)
chat = ChatService(db, eden)
auth_widget = AuthWidget(auth)

# Session check
sess = auth_widget.current_session()

if not sess:
    st.title("Welcome")
    auth_widget.login_view()
    st.markdown("---")
    auth_widget.register_view()
else:
    st.title("Chat")
    auth_widget.logout_button()

    # Input field
    user_input = st.text_input("Type your message…")

    # Chat response
    conv = None
    if user_input.strip():
        reply, conv = chat.full_turn(sess.user_id, user_input)
        st.markdown(f"**You:** {user_input}")
        st.markdown(f"**Bot:** {reply.content}")
        st.markdown(f"**Date:** {conv.created_at.strftime('%Y-%m-%d')}")

    # Conversation history by date
    if st.checkbox("Show conversation history"):
        convs = chat.convs.list_by_user(sess.user_id)
        if convs:
            selected = st.selectbox(
                "Select conversation date",
                convs,
                format_func=lambda c: c.created_at.strftime('%Y-%m-%d')
            )
            msgs = chat.msgs.list_by_conversation(selected.id)
            st.markdown("---")
            st.subheader(f"Conversation History — {selected.created_at.strftime('%Y-%m-%d')}")
            for m in msgs:
                st.markdown(f"**{m.role.capitalize()}:** {m.content}")
