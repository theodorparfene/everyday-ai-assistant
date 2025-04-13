from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import base64
import openai
import os
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import httpx
from bs4 import BeautifulSoup

# Initialize FastAPI
app = FastAPI()

#Server static files (for JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

#HTML templates (for web interface)
templates = Jinja2Templates(directory="templates")

load_dotenv()

# Set your OpenAI API Key (Consider using environment variables)
openai.api_key = os.getenv("OPENAI_API_KEY")


if not openai.api_key:
    raise ValueError("Missing OPENAI_API_KEY environment variable")


# Function to scrape and extract text from a webpage
async def fetch_webpage_content(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text(separator=" ", strip=True)[:8000]  # Limit to 8000 chars
        else:
            raise Exception(f"Failed to fetch webpage: {response.status_code}")

# Define the request model
class ChatRequest(BaseModel):
    prompt: str

class LinkRequest(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define the response endpoint
# Text chat endpoint
@app.post("/chat")
async def chat_with_llm(request: ChatRequest):
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                    {"role": "system", "content": "Respond concisely, with a maximum of 200 words while keeping key information intact."},
                    {"role": "user", "content": request.prompt}
                    ],
            max_tokens=200,
            temperature=0.3
        )

        # Corrected way to extract response (might delete)
        assistant_message = response.choices[0].message.content
        
        return {"response": assistant_message}

    except Exception as e:
        return {"error": str(e)}


# Image-to-Text Endpoint
@app.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Read and encode the image to base64
        image_data = base64.b64encode(await file.read()).decode("utf-8")

        # Call the OpenAI API with the updated gpt-4o model and image_url type
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract any visible text from this image."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )

        # Correct extraction of the assistant's message
        extracted_text = response.choices[0].message.content
        return {"text": extracted_text}

    except Exception as e:
        return {"error": str(e)}


# Webpage analysis endpoint
@app.post("/analyze_link")
async def analyze_link(request: LinkRequest):
    try:
        webpage_text = await fetch_webpage_content(request.url)

        # Send the content to GPT-4o for analysis
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Your job is to analyze product descriptions and identify whether the supplement is vegan, gluten-free, and non-GMO. Respond with 'Yes', 'No', or 'Unclear' for each."},
                {"role": "user", "content": f"Here is the product information: {webpage_text}. Is the supplement vegan, gluten-free, and non-GMO? Provide a clear Yes/No/Unclear answer for each."}
            ],
            max_tokens=300
        )

        assistant_message = response.choices[0].message.content
        return {"analysis": assistant_message}

    except Exception as e:
        return {"error": str(e)}
