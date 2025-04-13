# Everyday AI Assistant 🧠💬

A FastAPI-based chatbot assistant that helps with everyday tasks like cooking, cleaning, and fixing things. It uses a MySQL database to store specific knowledge entries, and falls back to OpenAI when needed.

---

## 🚀 Features

- 🤖 FastAPI-powered backend
- 💬 Smart chatbot using OpenAI's GPT-4
- 🧠 Internal knowledge base with MySQL (local database, for now)
- 🧼 Structured, concise answers
- 📚 Extendable database of task entries
- 🔁 Falls back to GPT when no match is found (not functional at the moment)

---

## 🧰 Tech Stack

| Tool        | Purpose                            |
|-------------|------------------------------------|
| **FastAPI** | Web framework and API server       |
| **OpenAI**  | Natural language response engine   |
| **MySQL**   | Persistent knowledge base          |
| **SQLAlchemy** | ORM for database interaction  |
| **Jinja2**  | HTML templating for the UI         |
| **Uvicorn** | Development server                 |
| **dotenv**  | Environment variable loading       |

---


## 📦 Requirements
fastapi
uvicorn
sqlalchemy
pydantic
python-dotenv
openai
pymysql
jinja2
httpx
bs4

**Install everything with:**
pip install -r requirements.txt

🔐 **Environment Setup**
Create a .env file based on the .env.example:
OPENAI_API_KEY=sk-your-openai-key
MYSQL_URL=mysql+pymysql://root:yourpassword@localhost:3306/ai_assistant

🐬 **MySQL Setup**
You’ll need a running MySQL instance. You can use local MySQL:
CREATE DATABASE ai_assistant;


🧪 **Run the App**
uvicorn app:app --reload

**Visit**:
http://localhost:8000

Swagger UI (API docs):
http://localhost:8000/docs


🧠 **Add Knowledge Entries**
Use the /add_knowledge route in Swagger to add entries like:
{
  "topic": "cooking",
  "title": "How to Cook Rice",
  "content": "1. Boil water...\n2. Add rice...",
  "tags": "rice,cooking,boil",
  "source": "internal"
}


💡 **Contributing**
Fork this repo
Clone your fork
Create a new branch
Submit a pull request
