import os
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# HS256 verification (matches your token’s alg)
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
SUPABASE_ISSUER = f"{SUPABASE_URL}/auth/v1"
SUPABASE_AUDIENCE = os.getenv("SUPABASE_AUDIENCE", "authenticated")

# (keep your other keys as-is)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHATBOT_LLM_MODEL = os.getenv("CHATBOT_LLM_MODEL", "mixtral-8x7b-32768")
MCQ_LLM_MODEL = os.getenv("MCQ_LLM_MODEL", "mixtral-8x7b-32768")
