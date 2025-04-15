#list models
import google.generativeai as genai

# Configure Gemini API key
api_key = '**********'
genai.configure(api_key=api_key)

# List available models
try:
    models = list(genai.list_models())  # Convert the generator to a list
    print("Available Models:", models)
except Exception as e:
    print(f"Error listing models: {e}")
