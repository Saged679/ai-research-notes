import streamlit as st
import requests
import time
import os

# Get the API URL from environment variable or use default
API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Research Notes", page_icon="📄")

st.title("AI Research Notes to Notion")

st.write("""
This app fetches the latest AI research papers, summarizes them using Gemini API, 
and automatically adds the summaries to your Notion database.
""")

# Display the API URL (helpful for debugging)
st.caption(f"API endpoint: {API_URL}")

# Function to check API availability
def is_api_available():
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

if st.button("Run Pipeline"):
    # Try to connect to the API with retries
    max_retries = 5
    for attempt in range(max_retries):
        if is_api_available():
            break
        if attempt < max_retries - 1:
            st.warning(f"API not ready, retrying ({attempt+1}/{max_retries})...")
            time.sleep(2)
        else:
            st.error("Could not connect to the backend API. Please check if the service is running.")
            st.stop()
    
    with st.spinner("Fetching and summarizing papers..."):
        try:
            response = requests.get(f"{API_URL}/run_pipeline")
            if response.status_code == 200:
                st.success(f"✅ {response.json()['papers_added']} papers added to Notion!")
            else:
                st.error(f"❌ Error: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Exception: {str(e)}")