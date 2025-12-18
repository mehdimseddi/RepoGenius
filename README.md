# RepoGenius ✨

AI-powered test and README generation for your GitHub repositories. Turn any public repo into a well-documented and tested project in seconds.

## Screenshots

<p align="center">
  <strong>Main Interface</strong><br>
  <img src="/images/main.png" alt="Main Application UI">
</p>
<p align="center">
  <strong>Generated README.md</strong><br>
  <img src="/images/readme.png" alt="Generated README">
</p>
<p align="center">
  <strong>Generated Test Suite</strong><br>
  <img src="/images/tests.png" alt="Generated Tests">
</p>

---

## About The Project

RepoGenius is a Streamlit web application that leverages the power of Google's Gemini models to automatically analyze a public GitHub repository and generate essential project files. It's designed to help developers quickly bootstrap documentation and testing for their projects.

### Key Features

*   **Automated README Generation:** Creates a professional `README.md` file based on the repository's name, description, language, and key files.
*   **Automated Test Generation:** Generates a comprehensive unit test suite for the primary code file in the repository.
*   **Multi-Language Support:** Intelligently handles various programming languages, including Python, Java, C++, C, JavaScript, and more.
*   **Jupyter Notebook Parsing:** Automatically extracts and analyzes code from `.ipynb` files.
*   **Configurable AI Model:** Allows users to choose from different Gemini models (e.g., `gemini-pro`, `gemini-1.5-flash`) to balance cost, speed, and quality.
*   **Secure API Key Handling:** API keys are entered directly into the UI and are not stored or logged.

### Built With

*   [Streamlit](https://streamlit.io/)
*   [Python](https://www.python.org/)
*   [Google Gemini API](https://ai.google.dev/)
*   [PyGithub](https://pygithub.readthedocs.io/)

---

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Python 3.8+
*   `pip` package manager

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your_username/RepoGenius.git
    cd RepoGenius
    ```
2.  **Create and activate a virtual environment:**
    ```sh
    # For Windows
    python -m venv .venv
    .venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1.  Launch the Streamlit app:
    ```sh
    streamlit run app.py
    ```
2.  The application will open in your web browser.

---

## Usage

1.  Open the application in your browser.
2.  Enter your **Gemini API Key** in the sidebar.
3.  (Optional) Provide a **GitHub Token** to increase the API rate limit, which is useful for larger repositories.
4.  Paste the URL of a public GitHub repository into the main input field.
5.  Select your desired AI model from the dropdown.
6.  Click the **"✨ Generate Content"** button.
7.  View, copy, or download the generated `README.md` and test files from the tabs.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

*(Note: A `LICENSE` file would need to be added separately.)*


