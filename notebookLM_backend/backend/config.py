import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecret")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHATBOT_LLM_MODEL = os.getenv("CHATBOT_LLM_MODEL", "mixtral-8x7b-32768")
MCQ_LLM_MODEL = os.getenv("MCQ_LLM_MODEL", "mixtral-8x7b-32768")
