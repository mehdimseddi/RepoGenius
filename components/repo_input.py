import streamlit as st

def repo_input_section():
    repo_url = st.text_input(
        "Enter a public GitHub repository URL to get started",
        placeholder="https://github.com/owner/repo"
    )
    return repo_url