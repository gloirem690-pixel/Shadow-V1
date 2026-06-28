import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_DEFAULT = os.getenv("MODEL_DEFAULT", "gpt-20b")
MAX_HISTORY = int(os.getenv("MAX_HISTORY", 10))
WEB_PORT = int(os.getenv("WEB_PORT", 5000))
DB_PATH = "shadow_bot.db"

# Modèles disponibles
MODELS = {
    "openrouter": {
        "gpt-20b": "openai/gpt-oss-20b:free",
        "gpt-120b": "openai/gpt-oss-120b:free",
        "gemini": "google/gemini-2-flash-exp:free",
        "llama-8b": "meta-llama/llama-3.1-8b-instruct:free",
        "mistral": "mistralai/mistral-7b-instruct:free",
    },
    "groq": {
        "llama-70b": "llama-3.3-70b-versatile",
        "mixtral": "mixtral-8x7b-32768",
    }
}
