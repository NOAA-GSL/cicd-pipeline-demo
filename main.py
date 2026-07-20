import os
from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Hello World API", description="A simple FastAPI application demonstrating CI/CD with GitHub Actions")

# In-memory storage for comments (for demonstration purposes)
comments: List[dict] = []

class Comment(BaseModel):
    author: str
    text: str

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Serve the index.html file from the static directory"""
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration"""
    return {"status": "healthy"}

@app.get("/comments", response_model=List[Comment])
async def get_comments():
    """Get all comments"""
    return comments

@app.post("/comments", response_model=Comment)
async def create_comment(comment: Comment):
    """Create a new comment"""
    comments.append(comment.dict())
    return comment
