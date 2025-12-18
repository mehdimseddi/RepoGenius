import os
import streamlit as st
from google import genai
from google.genai import types
import traceback

def get_testing_framework(language: str) -> str:
    """Returns the name of a popular testing framework for a given language."""
    frameworks = {
        "Python": "pytest",
        "JavaScript": "Jest",
        "TypeScript": "Jest with ts-jest",
        "Java": "JUnit 5",
        "C++": "Google Test (gtest)",
        "C": "cmocka",
        "Go": "the built-in testing package",
        "Ruby": "RSpec",
        "PHP": "PHPUnit",
        "C#": "xUnit"
    }
    return frameworks.get(language, f"an appropriate and popular testing framework for {language}")

def generate_ai_content(repo_data: dict, model_name: str = "gemini-pro", gemini_api_key: str | None = None) -> dict:
    """Generate content using Google Gemini API"""
    if not gemini_api_key:
        st.error("A Gemini API key is required to generate content.")
        return None

    try:
        client = genai.Client(api_key=gemini_api_key)
    except Exception as e:
        st.error(f"Failed to initialize Gemini client: {e}")
        return None

    if not repo_data.get('files'):
        st.warning("Could not find any relevant files in the repository to generate content from.")
        return None
        
    try:
        # Configuration for generation
        config = types.GenerateContentConfig(
            temperature=0.2, # Lower temperature for more predictable code
            top_p=0.9,
            top_k=35,
            max_output_tokens=4096, # Increased token limit for tests
            candidate_count=1
        )
        
        # --- README Generation ---
        readme_prompt = f"Create a professional README.md for a {repo_data['language']} repository named '{repo_data['name']}'. Description: {repo_data['description']}. Key files: {''.join([f'- {f['name']}' for f in repo_data['files']])}"
        
        # --- Test Generation ---
        first_file = repo_data['files'][0]
        file_name = first_file['name']
        file_content = first_file['content']
        language = first_file.get('language') or repo_data.get('language')

        is_notebook = file_name.endswith('.ipynb')

        prompt_intro = "You are an expert test engineer. Your task is to generate comprehensive and runnable unit tests for the following code."
        if is_notebook:
            prompt_context = f"The code was extracted from a Jupyter Notebook named '{file_name}'. Treat it as a standard Python script."
            language = 'Python' # Override language for notebooks
        else:
            if file_name.endswith(('.h', '.hpp')):
                prompt_context = f"The code is from a header file named '{file_name}' written in {language}. Generate tests for the logic defined in this header, assuming it's implemented in a corresponding source file."
            else:
                prompt_context = f"The code is from a file named '{file_name}' written in {language}."

        testing_framework = get_testing_framework(language)

        prompt_instruction = f"""
Generate a complete test file with all necessary imports and setup.
Use the {testing_framework}.
If the code involves external dependencies like APIs, file I/O, or environment variables, create mock objects to ensure the tests are isolated and runnable without the actual dependencies.
Your output must be only the test code itself, ready to be saved to a file. Do not write any explanations, introductions, summaries, or markdown formatting like ```python.
"""

        test_prompt = f"""
{prompt_intro}
{prompt_context}
{prompt_instruction}

Here is the code to test:
```{language.lower() if language else 'code'}
{file_content[:3500]}
```
"""
        
        # --- API Calls ---
        readme_response = client.models.generate_content(
            model=model_name,
            contents=readme_prompt,
            config=config
        )
        
        test_response = client.models.generate_content(
            model=model_name,
            contents=test_prompt,
            config=config
        )
        
        # Clean up the test output
        raw_tests = test_response.text
        if raw_tests.strip().startswith("```"):
            # Find the first newline and take everything after it
            first_newline = raw_tests.find('\n')
            if first_newline != -1:
                raw_tests = raw_tests[first_newline+1:]

        if raw_tests.strip().endswith("```"):
            # Find the last occurrence of ``` and take everything before it
            last_marker = raw_tests.rfind('```')
            if last_marker != -1:
                raw_tests = raw_tests[:last_marker]

        return {
            "readme": readme_response.text,
            "tests": raw_tests.strip(),
            "repo_name": repo_data["name"],
            "file_name": file_name
        }
    
    except Exception as e:
        st.error(f"An error occurred during AI content generation: {str(e)}")
        with st.expander("Technical Details"):
            st.code(traceback.format_exc())
        return None
