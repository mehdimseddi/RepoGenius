import streamlit as st
from utils.formatters import format_code
import base64

def results_section(results: dict):
    st.subheader("Generated Content")

    tab1, tab2 = st.tabs([
        "README.md",
        "Test Suite"
    ])

    with tab1:
        st.markdown(results["readme"])
        readme_bytes = results["readme"].encode('utf-8')
        st.download_button(
            label="Download README.md",
            data=readme_bytes,
            file_name="README.md",
            mime="text/markdown",
            use_container_width=True
        )

    with tab2:
        st.markdown(f"#### Tests for `{results['file_name']}`")
        st.code(format_code(results["tests"]), language=detect_language(results["tests"]))
        test_bytes = results["tests"].encode('utf-8')
        st.download_button(
            label=f"Download Tests",
            data=test_bytes,
            file_name=f"test_{results['repo_name']}.py",
            mime="text/plain",
            use_container_width=True
        )

def detect_language(code: str) -> str:
    """Detect programming language from code snippet for syntax highlighting."""
    if not isinstance(code, str):
        return "python"  # Default

    # Order matters to distinguish C-like languages
    if "std::" in code or "#include <iostream>" in code:
        return "cpp"
    if "import org.junit" in code or ("public class" in code and "{" in code):
        return "java"
    if "#include <stdio.h>" in code or "#include <stdlib.h>" in code:
        return "c"
    if "import pytest" in code or ("def " in code and ":" in code):
        return "python"
    if "describe(" in code and "it(" in code or "console.log(" in code:
        return "javascript"
    if "package main" in code or ("func " in code and "{" in code):
        return "go"
    if "namespace " in code and "class " in code and "{" in code:
        return "csharp" # Streamlit uses 'csharp' for C#

    return "python"  # Fallback
