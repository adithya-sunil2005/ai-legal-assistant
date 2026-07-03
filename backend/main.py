from dotenv import load_dotenv
import os
load_dotenv()

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pdfplumber
import io

from backend.agents.document_agent import extract_text_from_pdf
from backend.agents.legal_terms_agent import flag_risky_clauses
from backend.agents.solution_agent import get_solutions
from backend.agents.chat_agent import answer_question

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Store document text temporarily
document_store = {}

# Route 1: Upload PDF and analyze
@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    contents = await file.read()
    
    text = extract_text_from_pdf(contents)
    
    document_store["text"] = text
    
    risky_clauses = flag_risky_clauses(text)
    solutions = get_solutions(risky_clauses)
    
    return {
        "text": text[:500],
        "risky_clauses": risky_clauses,
        "solutions": solutions
    }

# Route 2: Chat Q&A
class Question(BaseModel):
    question: str

@app.post("/chat")
async def chat(q: Question):
    doc_text = document_store.get("text", "")
    result = answer_question(q.question, doc_text)
    return result