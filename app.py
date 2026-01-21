import streamlit as st
import pandas as pd
import PyPDF2
from docx import Document

from auth import create_users_table, register_user, login_user
from chatbot import get_response

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI Chatbot", layout="centered")

# ---------- DARK + RADIANT CSS ----------
st.markdown("""
<style>

/* ---------- GLOBAL ---------- */
.stApp {
    background: radial-gradient(circle at top, #0f2027, #000000);
    color: #eaeaea;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ---------- TITLE ---------- */
h1 {
    color: #00f5ff;
    font-weight: 800;
    text-align: center;
    letter-spacing: 1px;
}

/* ---------- LABELS ---------- */
label {
    color: #bbbbbb !important;
    font-weight: 600;
}

/* ---------- INPUTS ---------- */
input {
    background-color: #0b0f14 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #00f5ff !important;
    padding: 12px !important;
    font-weight: 600 !important;
}

/* ---------- SELECTBOX ---------- */
div[data-baseweb="select"] > div {
    background-color: #0b0f14;
    border-radius: 10px;
    border: 1px solid #00f5ff;
    color: white;
}

/* ---------- BUTTONS ---------- */
button {
    background: linear-gradient(135deg, #00f5ff, #7c00ff) !important;
    color: #000 !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-size: 14px !important;
    font-weight: 800 !important;
    border: none !important;
    transition: all 0.25s ease;
}

button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #00f5ff;
}

/* ---------- CHAT BOX ---------- */
.chat-box {
    background: #0b0f14;
    border: 1px solid #1f2937;
    padding: 16px;
    border-radius: 14px;
    margin-top: 14px;
    line-height: 1.6;
    font-weight: 600;
}

/* ---------- ALERTS ---------- */
div[data-testid="stAlert"] {
    border-radius: 10px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ---------- DB ----------
create_users_table()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "file_text" not in st.session_state:
    st.session_state.file_text = ""

st.title("🤖 AI Chatbot")

# ---------- FILE READERS ----------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return " ".join([page.extract_text() or "" for page in reader.pages])

def read_excel(file):
    df = pd.read_excel(file)
    return df.to_string()

def read_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def read_txt(file):
    return file.read().decode("utf-8")

def extract_text(file):
    if file.type == "application/pdf":
        return read_pdf(file)
    elif file.type in [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel"
    ]:
        return read_excel(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return read_docx(file)
    elif file.type == "text/plain":
        return read_txt(file)
    return ""

# ---------- LOGIN / REGISTER ----------
if not st.session_state.logged_in:
    menu = st.selectbox("Menu", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Register":
        if st.button("Register"):
            if register_user(username, password):
                st.success("Registered Successfully!")
            else:
                st.error("User already exists")

    if menu == "Login":
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid Credentials")

# ---------- CHATBOT ----------
else:
    st.markdown(f"""
    **Welcome back, {st.session_state.username}!**  
    <span style="color:#8b9bb4;">Upload a file and ask anything.</span>
    """, unsafe_allow_html=True)

    # ---------- FILE UPLOAD ----------
    uploaded_file = st.file_uploader(
        "📎 Upload a file (PDF, Excel, Word, TXT)",
        type=["pdf", "xlsx", "xls", "docx", "txt"]
    )

    if uploaded_file:
        st.session_state.file_text = extract_text(uploaded_file)
        st.success("File loaded successfully!")

    user_input = st.text_input("💬 Your message")

    if st.button("Send"):
        if user_input:
            reply = get_response(
                user_input,
                st.session_state.file_text
            )

            st.markdown(f"""
            <div class="chat-box">
            <span style="color:#00f5ff;">You:</span> {user_input}<br><br>
            <span style="color:#7c00ff;">Bot:</span> {reply}
            </div>
            """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.file_text = ""
        st.rerun()
