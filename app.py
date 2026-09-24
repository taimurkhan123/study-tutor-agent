
import streamlit as st
import os
from io import BytesIO
from datetime import datetime
from pypdf import PdfReader
from crew_agent import run_tutor_agent

# ============================================================
#  PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="AI Study Tutor",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ============================================================
#  MODERN CSS
# ============================================================
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 6rem;
        max-width: 860px;
    }
    h1 {
        color: #1E3A8A;
        font-weight: 700;
        letter-spacing: -0.6px;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #6B7280;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    /* Chat bubbles */
    .stChatMessage {
        padding: 1rem 1.2rem;
        border-radius: 1rem;
        margin-bottom: 0.6rem;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background-color: #EFF6FF;
        border-color: #DBEAFE;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
        background-color: #F9FAFB;
    }
    .stChatInput textarea {
        border-radius: 1rem !important;
        border: 1px solid #D1D5DB !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E5E7EB;
    }
    section[data-testid="stSidebar"] h2 {
        font-size: 1.05rem;
        color: #111827;
        margin-bottom: 0.3rem;
    }
    /* Buttons */
    .stButton button {
        border-radius: 0.6rem;
        font-weight: 500;
        border: 1px solid #E5E7EB;
        transition: all 0.15s ease;
    }
    .stButton button:hover {
        border-color: #93C5FD;
        background-color: #EFF6FF;
    }
    /* PDF pill */
    .pdf-pill {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        background-color: #DCFCE7;
        color: #166534;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    /* Message count badge */
    .msg-count {
        font-size: 0.78rem;
        color: #6B7280;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
#  API KEY
# ============================================================
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
else:
    st.error("⚠️ GROQ_API_KEY not found in Streamlit secrets.")
    st.stop()

# ============================================================
#  SESSION STATE
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I'm your study tutor. 🧠\n\n"
                "You can:\n"
                "- Ask me to explain any topic\n"
                "- Request a quiz on anything\n"
                "- Upload a PDF in the sidebar and ask questions about it\n\n"
                "I'll remember our conversation."
            ),
        }
    ]

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None
if "chat_id" not in st.session_state:
    st.session_state.chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# ============================================================
#  SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🧠 Study Tutor")
    st.caption("Groq · GPT-OSS-120B · CrewAI")
    st.divider()

    # ---------- Chat controls ----------
    st.markdown("### 💬 Chat")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ New", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "New chat started. What would you like to study?",
                }
            ]
            st.session_state.chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.rerun()

    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Chat cleared. Ask me anything!",
                }
            ]
            st.rerun()

    st.markdown(
        f"<span class='msg-count'>{len(st.session_state.messages)} messages · "
        f"ID {st.session_state.chat_id[-6:]}</span>",
        unsafe_allow_html=True,
    )

    st.divider()

    # ---------- PDF section ----------
    st.markdown("### 📄 Study Material")
    uploaded = st.file_uploader(
        "Upload a PDF",
        type=["pdf"],
        label_visibility="collapsed",
    )

    if uploaded is not None and uploaded.name != st.session_state.pdf_name:
        try:
            reader = PdfReader(BytesIO(uploaded.read()))
            text = "".join(page.extract_text() or "" for page in reader.pages)
            if not text.strip():
                st.warning("No readable text found in this PDF.")
            else:
                st.session_state.pdf_text = text[:12000]
                st.session_state.pdf_name = uploaded.name
                st.rerun()
        except Exception as e:
            st.error(f"Could not read PDF: {e}")

    if st.session_state.pdf_name:
        st.markdown(
            f"<span class='pdf-pill'>📄 {st.session_state.pdf_name}</span>",
            unsafe_allow_html=True,
        )
        st.caption(f"{len(st.session_state.pdf_text):,} characters loaded")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔍 Preview", use_container_width=True):
                st.session_state.show_preview = not st.session_state.get(
                    "show_preview", False
                )
        with col_b:
            if st.button("❌ Remove", use_container_width=True):
                st.session_state.pdf_text = None
                st.session_state.pdf_name = None
                st.rerun()

        if st.session_state.get("show_preview", False):
            with st.expander("PDF preview", expanded=True):
                st.text(st.session_state.pdf_text[:1500] + "...")

    st.divider()
    st.caption("Built with CrewAI · Powered by Groq")

# ============================================================
#  MAIN AREA
# ============================================================
st.title("🧠 AI Study Tutor")
st.markdown(
    "<div class='subtitle'>Your personal study companion — with memory and PDF understanding.</div>",
    unsafe_allow_html=True,
)

# --- Status strip ---
status_cols = st.columns(2)
with status_cols[0]:
    if st.session_state.pdf_name:
        st.success(f"📄 PDF active: {st.session_state.pdf_name}", icon="✅")
    else:
        st.info("📄 No PDF uploaded — upload one in the sidebar", icon="ℹ️")
with status_cols[1]:
    st.info(f"💬 Memory on · {len(st.session_state.messages)} messages", icon="🧠")

st.write("")

# --- Render chat ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Input ---
placeholder = (
    "Ask about the PDF or anything else..."
    if st.session_state.pdf_name
    else "Ask a question or request a study task..."
)

if prompt := st.chat_input(placeholder):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                history = st.session_state.messages[:-1]
                response = run_tutor_agent(
                    user_request=prompt,
                    chat_history=history,
                    pdf_text=st.session_state.pdf_text,
                )
            except Exception as e:
                response = f"⚠️ Error: {e}"
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# ============================================================
#  FOOTER
# ============================================================
st.markdown(
    "<div style='text-align:center; color:#9CA3AF; font-size:0.78rem; "
    "margin-top:2rem;'>Powered by Groq GPT-OSS-120B · Built with CrewAI</div>",
    unsafe_allow_html=True,
)
