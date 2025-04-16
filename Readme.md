Sure! Here's a complete `README.md` file for your project:

---
# Code Review Assistant with AI

A Streamlit-powered web app that integrates with GitHub and Gemini AI to optimize the code review process for Python files in pull requests. It helps reviewers by detecting formatting issues, bugs, and unnecessary code, while also showing precise diffs for each file.

## 🚀 Features

- 🔒 Authenticate with your GitHub token
- 🌿 Select any branch and view open PRs
- 📂 Browse and view modified Python files
- 🧠 Get AI-powered suggestions using Gemini:
  - Formatting issues
  - Bugs and logical errors
  - Unused imports and variables
- 📌 View code diffs for selected files

## 📦 Requirements

- Python 3.8+
- Streamlit
- PyGithub
- requests
- google-generativeai

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🛠️ Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/code-review-assistant.git
cd code-review-assistant
```

2. Create a `.streamlit/secrets.toml` file and add your Gemini API key:

```toml
GEMINI_API_KEY = "your-gemini-api-key"
```

3. Run the app:

```bash
streamlit run app.py
```

## 📸 Preview

![screenshot](https://path-to-your-screenshot.png)

## 🤖 Powered by

- [Google Gemini API](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [GitHub API](https://docs.github.com/en/rest)
