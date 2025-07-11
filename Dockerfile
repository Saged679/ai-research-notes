# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Environment variables
ENV GEMINI_API_KEY=""
ENV NOTION_API_KEY=""
ENV NOTION_DATABASE_ID=""
ENV API_URL="http://localhost:8000"

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Add a health endpoint to FastAPI
RUN echo 'from fastapi import FastAPI\napp = FastAPI()\n@app.get("/health")\ndef health_check():\n    return {"status": "ok"}' > backend/health_endpoint.py

# Command to run both services
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run backend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]