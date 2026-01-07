from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from utils.parallel import run_parallel
from utils.report import generate_report
import auth

st.set_page_config(
    page_title="LLM Comparison Tool",
    page_icon="🚀",
    layout="wide"
)

# -------- AUTH GATE --------
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    auth.login()
    st.stop()

# -------- LOGGED-IN UI --------
st.write(f"Welcome {st.session_state.user}")

if st.button("Logout"):
    st.session_state.authenticated = False
    st.session_state.user = None
    st.rerun()

st.title("🚀 LLM Comparison Tool")
st.caption("🔒 Demo authentication only — users reset on refresh")

st.markdown(
    """
Compare **ChatGPT**, **Gemini**, and **LLaMA**
using a **single unified prompt**.
"""
)

prompt = st.text_area(
    "Enter your prompt",
    height=150,
    placeholder="Explain Python decorators with an example"
)

if st.button("Compare Models"):
    if not prompt.strip():
        st.warning("Please enter a prompt")
    else:
        with st.spinner("Running models in parallel..."):
            responses = run_parallel(prompt)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("ChatGPT")
            st.write(responses.get("ChatGPT", ""))

            st.subheader("Gemini")
            st.write(responses.get("Gemini", ""))

        with col2:
            st.subheader("LLaMA")
            st.write(responses.get("LLaMA", ""))

        report_path = generate_report(prompt, responses)

        with open(report_path, "rb") as f:
            st.download_button(
                label="📥 Download comparison report (CSV)",
                data=f,
                file_name="llm_comparison_report.csv",
                mime="text/csv"
            )

        st.success("✅ Comparison completed successfully!")
