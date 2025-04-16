import streamlit as st
from github import Github
import requests
import google.generativeai as genai

# Initialize Gemini
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "your-gemini-api-key")
genai.configure(api_key=GEMINI_API_KEY)

# Fetch file content from GitHub

def fetch_file_content(file_url):
    response = requests.get(file_url)
    response.raise_for_status()
    return response.text

# Fetch all branches
def fetch_branches(repo_name, github_token):
    try:
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        branches = repo.get_branches()
        return [branch.name for branch in branches]
    except Exception as e:
        st.error(f"🚫 Failed to fetch branches: {e}")
        return []

# Get file diffs in a PR
def get_file_diff(repo_name, pr_number, file_path, github_token):
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3.diff"
    }
    url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    files = response.json()
    for file in files:
        if file["filename"] == file_path:
            return file.get("patch", "No diff available.")
    return "Diff not found for this file."

# Fetch open pull requests
def fetch_pull_requests(repo_name, github_token, base_branch=None):
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    pull_requests = repo.get_pulls(state="open")
    pr_data = []

    for pr in pull_requests:
        if base_branch and pr.base.ref != base_branch:
            continue

        pr_info = {
            "number": pr.number,
            "title": pr.title,
            "created_at": pr.created_at,
            "branch": pr.head.ref,
            "files": []
        }

        files = pr.get_files()
        for file in files:
            if file.filename.endswith('.py'):
                pr_info["files"].append({
                    "filename": file.filename,
                    "status": file.status
                })

        pr_data.append(pr_info)

    return pr_data

# Streamlit UI
st.title("Code Review Assistant with AI")
st.sidebar.header("Repository Configuration")

repo_name = st.sidebar.text_input("GitHub Repo (e.g., 'user/repo')", "MohakSaini/Mail_Automation")
github_token = st.sidebar.text_input("GitHub Token", type="password")

if not github_token:
    st.warning("Please enter your GitHub token in the sidebar to proceed.")
    st.stop()

if repo_name and github_token:
    try:
        branches = fetch_branches(repo_name, github_token)
        selected_branch = st.sidebar.selectbox("Select a branch", branches)
        st.sidebar.markdown(f"**Selected Branch:** `{selected_branch}`")

        pr_data = fetch_pull_requests(repo_name, github_token, base_branch=selected_branch)

        if pr_data:
            st.subheader(f"Open Pull Requests in {repo_name}")

            pr_options = [f"#{pr['number']} - {pr['title']} (→ {pr['branch']})" for pr in pr_data]
            selected_option = st.selectbox("Select a PR to view", pr_options)
            selected_index = pr_options.index(selected_option)
            selected_pr = pr_data[selected_index]

            st.subheader(f"PR #{selected_pr['number']} - {selected_pr['title']}")
            st.write(f"Created at: {selected_pr['created_at']}")

            if selected_pr['files']:
                file_names = [f["filename"] for f in selected_pr["files"]]
                selected_file = st.selectbox("Select a file to view", file_names)

                branch = selected_pr.get("branch", "main")
                file_url = f"https://raw.githubusercontent.com/{repo_name}/{branch}/{selected_file}"

                try:
                    content = fetch_file_content(file_url)
                except Exception as e:
                    st.error(f"Error fetching file content: {e}")
                    content = ""
            else:
                st.warning("No Python files modified in this PR.")
                content = ""

            if content:
                if st.button("💡 Get AI Suggestions"):
                    with st.spinner("Analyzing with Gemini..."):
                        try:
                            model = genai.GenerativeModel("gemini-2.0-flash")
                            prompt = f"""
You are a code reviewer.

Analyze the following Python code and provide only the following three sections in your response:

1. Formatting Issues (e.g., indentation, naming, spacing)
2. Errors or Bugs (logical or runtime issues)
3. Unnecessary Variables or Imports (anything unused or redundant)

Do not include any other commentary. Keep it concise and structured.

```python
{content}
```"""
                            response = model.generate_content(prompt)
                            suggestion = response.text
                            st.markdown("### 🧠 AI Suggestions")
                            st.info(suggestion)
                        except Exception as e:
                            st.error(f"AI analysis failed: {e}")

                if st.button("📌 Show Changes Only"):
                    try:
                        diff = get_file_diff(repo_name, selected_pr["number"], selected_file, github_token)
                        st.markdown("### 🧾 Code Diff")
                        st.code(diff, language="diff")
                    except Exception as e:
                        st.error(f"Error fetching diff: {e}")
        else:
            st.info("No open PRs found in the repository.")
    except Exception as e:
        st.error(f"❌ Error fetching PRs: {e}")
