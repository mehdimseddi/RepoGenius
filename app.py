import streamlit as st
from components.header import header_section
from components.repo_input import repo_input_section
from components.results_display import results_section
from utils.validators import validate_github_url
from services.github_service import fetch_repo_data_cached
from services.ai_service import generate_ai_content

# Page config
st.set_page_config(
    page_title="RepoGenius",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded" # Show sidebar by default
)

# --- API Key Configuration ---
st.sidebar.title("⚙️ API Configuration")
st.sidebar.markdown("Enter your API keys below. Your keys are not stored or shared.")

gemini_key = st.sidebar.text_input(
    "Gemini API Key", 
    type="password", 
    help="Required. Get yours from Google AI Studio."
)

st.sidebar.markdown("---")

use_github_token = st.sidebar.checkbox(
    "Use GitHub Token (Optional)", 
    value=False, 
    help="Provide a GitHub token to increase API rate limits, allowing analysis of more files."
)
github_token = None
if use_github_token:
    github_token = st.sidebar.text_input(
        "GitHub Personal Access Token", 
        type="password", 
        help="Generate a token with `public_repo` access."
    )

# Custom styling
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Header
header_section()

# Main content
if "results" not in st.session_state:
    st.session_state.results = None

repo_url = repo_input_section()

model_choice = st.selectbox(
    "Select AI Model",
    ("gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-2.5-pro", "gemini-3-flash-preview", "gemini-3-pro-preview"),
    index=0,
    help="Choose the AI model for generation. More powerful models may yield better results."
)

if st.button("✨ Generate Content", type="primary", use_container_width=True):
    if not validate_github_url(repo_url):
        st.error("❌ Please enter a valid GitHub repository URL.")
    elif not gemini_key:
        st.error("❌ Please enter your Gemini API Key in the sidebar to continue.")
    else:
        with st.spinner("Analyzing repository and generating content..."):
            repo_data = fetch_repo_data_cached(repo_url, github_token=github_token)
            if repo_data:
                results = generate_ai_content(
                    repo_data, 
                    model_name=model_choice, 
                    gemini_api_key=gemini_key
                )
                if results:
                    st.session_state.results = results
                    st.rerun()

# Results display
if st.session_state.results:
    results_section(st.session_state.results)
