from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import or_
from db import SessionLocal
from models import KnowledgeEntry
import logging

# Setup logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI()

# Serve static files (for JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML templates (for web interface)
templates = Jinja2Templates(directory="templates")

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("Missing OPENAI_API_KEY environment variable")

# Database dependency to be injected into endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for chat request
class ChatRequest(BaseModel):
    prompt: str

# Pydantic model for knowledge entry input
class KnowledgeInput(BaseModel):
    topic: str
    title: str
    content: str
    tags: str
    source: str = None

# Route to add new knowledge entries to the database
@app.post("/add_knowledge")
def add_knowledge(entry: KnowledgeInput, db: Session = Depends(get_db)):
    new_entry = KnowledgeEntry(**entry.model_dump())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"message": "Knowledge added!", "id": new_entry.id}

# Home page route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Main chat endpoint with full knowledge base scanning
@app.post("/chat")
async def chat_with_llm(request: ChatRequest, db: Session = Depends(get_db)):
    query = request.prompt

    # Load all knowledge entries from DB
    results = db.query(KnowledgeEntry).all()

    if results:
        # Combine all entries into a single context for GPT
        context = "\n\n".join([f"{entry.title}:\n{entry.content}" for entry in results])
        prompt = (
            f"The user asked: \"{query}\".\n"
            f"Here is everything stored in the internal knowledge base:\n\n{context}\n\n"
            "Choose the most relevant entry and use ONLY its content to answer. "
            "Be concise and instructional. Do not make up steps or add anything extra."
        )
        logger.info("📚 GPT prompt using full knowledge base:\n%s", prompt)
    else:
        prompt = query
        logger.info("❌ Knowledge base is empty. Sending raw user query to GPT.")

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Use the following internal knowledge to answer the question. Only use the provided information. "
                        "Do not invent steps or add introductions, summaries, or closing comments. Be concise and instructional. "
                        "Use numbered steps or bullet points where needed."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=600,
            temperature=0.4
        )

        assistant_message = response.choices[0].message.content
        return {
            "response": assistant_message,
            "source": "internal" if results else "openai"
        }

    except Exception as e:
        logger.error("❌ Error during OpenAI API call: %s", str(e))
        return {"error": str(e)}
