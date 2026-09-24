import streamlit as st
import os
from crew_agent import run_tutor_agent

st.set_page_config(
    page_title="AI Study Tutor",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 820px;
    }
    h1 {
        color: #1E3A8A;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .stChatMessage {
        padding: 1rem 1.2rem;
        border-radius: 1rem;
        margin-bottom: 0.6rem;
        border: 1px solid #E5E7EB;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background-color: #EFF6FF;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
        background-color: #F9FAFB;
    }
    .stChatInput textarea {
        border-radius: 1rem !important;
        border: 1px solid #D1D5DB !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 AI Study Tutor")
st.caption("Your personal study companion — powered by Groq + CrewAI")


# --- Load API key ---
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    st.error("⚠️ GROQ_API_KEY not found. Add it in Streamlit secrets.")
    st.stop()


# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm your study tutor. Ask me to explain a topic, "
                "generate a quiz, or find resources."
            ),
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --- Chat input ---
if prompt := st.chat_input("Ask a question or request a study task..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("The tutor is thinking..."):
            try:
                response = run_tutor_agent(prompt)
            except Exception as e:
                response = f"Sorry, I hit an error: {e}"
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
