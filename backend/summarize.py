import google.generativeai as genai
from backend.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

def summarize_text(text):
    prompt = f"Summarize this AI research abstract in 3-5 simple bullet points:\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()
