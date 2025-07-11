from fastapi import FastAPI
from backend.fetch_papers import fetch_latest_ai_papers
from backend.summarize import summarize_text
from backend.notion_client import add_note_to_notion

app = FastAPI()

@app.get("/health")
def health_check():
    """Health check endpoint for the API."""
    return {"status": "ok"}

@app.get("/run_pipeline")
def run_pipeline():
    print("Pipeline triggered!")
    papers = fetch_latest_ai_papers()
    print(f"Fetched papers: {papers}")
    
    successful_additions = 0
    for paper in papers:
        summary = summarize_text(paper['summary'])
        print(f"Summary: {summary}")
        success = add_note_to_notion(paper['title'], summary, paper['link'])
        if success:
            successful_additions += 1
    
    return {"status": "completed", "papers_added": successful_additions}