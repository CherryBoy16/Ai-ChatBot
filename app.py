import streamlit as st
from auth import create_users_table, register_user, login_user
from chatbot import get_response

st.set_page_config(page_title="AI Chatbot", layout="centered")

# ---------- CSS GRADIENT ----------
st.markdown("""
<style>

/* ---------- GLOBAL ---------- */
.stApp {
    background-color: #fafafa;
    color: #111111;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                 Roboto, Oxygen, Ubuntu, Cantarell, "Helvetica Neue",
                 Arial, sans-serif;
}

/* ---------- TITLE ---------- */
h1 {
    color: #111111;
    font-weight: 600;
    text-align: center;
    letter-spacing: 0.5px;
    margin-bottom: 1.5rem;
}

/* ---------- INPUTS ---------- */
input {
    border-radius: 8px !important;
    padding: 10px !important;
    font-size: 15px !important;
    border: 1px solid #d0d0d0 !important;
    background-color: #ffffff !important;
}

/* ---------- SELECTBOX ---------- */
div[data-baseweb="select"] > div {
    border-radius: 8px;
    border: 1px solid #d0d0d0;
    background-color: #ffffff;
}

/* ---------- BUTTONS ---------- */
button {
    background-color: #111111 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    padding: 8px 22px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    border: none !important;
    transition: all 0.2s ease-in-out;
}

button:hover {
    background-color: #333333 !important;
    transform: translateY(-1px);
}

/* ---------- CHAT BOX ---------- */
.chat-box {
    background-color: #ffffff;
    padding: 14px;
    border-radius: 10px;
    margin-top: 12px;
    border: 1px solid #e6e6e6;
    line-height: 1.5;
}

/* ---------- SUCCESS / ERROR ---------- */
div[data-testid="stAlert"] {
    border-radius: 8px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


create_users_table()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("🤖 AI Chatbot")

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
    st.markdown(
        f"""**Hi {st.session_state.username}! 👋**  
        <span style='color:#555;'>Welcome back.</span>
        """,
        unsafe_allow_html=True
    )


    user_input = st.text_input("Your message")

    if st.button("Send"):
        if user_input:
            reply = get_response(user_input)
            st.markdown(f"""
            <div class="chat-box">
            <b>You:</b> {user_input}<br><br>
            <b>Bot:</b> {reply}
            </div>
            """, unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
