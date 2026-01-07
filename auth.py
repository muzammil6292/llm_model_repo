import streamlit as st
import hashlib


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _init_state():
    if "users" not in st.session_state:
        st.session_state.users = {}  # demo-only, in-memory

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "user" not in st.session_state:
        st.session_state.user = None


def login():
    _init_state()

    if st.session_state.authenticated:
        return

    st.markdown("## 🔐 Authentication (Demo Only)")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    # ---------- LOGIN ----------
    with tab_login:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", use_container_width=True):
            users = st.session_state.users
            hashed = _hash(password)

            if username in users and users[username] == hashed:
                st.session_state.authenticated = True
                st.session_state.user = username
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    # ---------- REGISTER ----------
    with tab_register:
        new_user = st.text_input("Choose Username", key="reg_user")
        new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")

        if st.button("Register", use_container_width=True):
            users = st.session_state.users

            if not new_user.strip():
                st.error("Username cannot be empty")
            elif new_user in users:
                st.error("Username already exists")
            elif len(new_pass) < 4:
                st.error("Password must be at least 4 characters")
            elif new_pass != confirm:
                st.error("Passwords do not match")
            else:
                users[new_user] = _hash(new_pass)
                st.success("🎉 Registered successfully. Please login.")

    st.info("ℹ️ Demo authentication — users reset on refresh or restart")
    st.stop()
