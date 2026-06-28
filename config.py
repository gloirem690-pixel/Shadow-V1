# -*- coding: utf-8 -*-
"""
Configuration du bot – variables d'environnement et constantes.
"""

import os
from dotenv import load_dotenv

# Charger .env uniquement en local (Render injecte ses propres variables)
load_dotenv()

# ===== Variables Telegram =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN manquant !")

# ===== Clés API =====
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ===== Modèles =====
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
# ✅ Définition du modèle par défaut (alias)
DEFAULT_MODEL = os.getenv("MODEL_DEFAULT", "gpt-20b")

# ===== Autres paramètres =====
MAX_HISTORY = int(os.getenv("MAX_HISTORY", 10))
WEB_PORT = int(os.getenv("WEB_PORT", 5000))
DB_PATH = "shadow_bot.db"