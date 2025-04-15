import streamlit as st
import google.generativeai as genai

# Setup
st.set_page_config(page_title="Code Optimizer with Gemini", layout="centered")
st.title("🧠 Gemini Code Optimizer")
st.markdown("Upload a Python file, and get AI suggestions to optimize it.")

# Predefined credentials (username: "admin", password: "password123")
USERNAME = "admin"
PASSWORD = "password123"

# Login functionality
def authenticate_user(username, password):
    return username == USERNAME and password == PASSWORD

# Login form
st.sidebar.title("Login")
username_input = st.sidebar.text_input("Username")
password_input = st.sidebar.text_input("Password", type="password")

# Authentication check
if username_input and password_input:
    if authenticate_user(username_input, password_input):
        st.sidebar.success("Login successful!")
        
        # Provided API key
        api_key = "AIzaSyA2C5vWjRdgCJ8sKz9TxmbLp2THxhEyElM"  # Directly use your provided API key here

        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")  # Specify the correct model, you might need to adjust it depending on the available models

        # File uploader
        uploaded_file = st.file_uploader("📁 Upload your Python (.py) file", type=["py"])

        if uploaded_file:
            code = uploaded_file.read().decode("utf-8")

            st.subheader("📄 Code Preview")
            st.code(code, language="python")

            with st.spinner("Analyzing with Gemini..."):
                prompt = (
                    "You are an expert Python developer. Analyze the following code and suggest any optimizations, "
                    "including removal of unnecessary variables, unused imports, better structure, and simplifications:\n\n"
                    f"{code}"
                )
                try:
                    response = model.generate_content(prompt)
                    suggestions = response.text
                except Exception as e:
                    st.error(f"❌ Gemini API error: {e}")
                    st.stop()

            st.subheader("💡 Optimization Suggestions")
            st.markdown(suggestions)
    else:
        st.sidebar.error("Invalid credentials. Please try again.")
else:
    st.sidebar.warning("Please enter your username and password to log in.")
