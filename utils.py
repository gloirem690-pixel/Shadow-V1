# -*- coding: utf-8 -*-
"""
Fonctions utilitaires pour Shadow V1 :
- Appels API OpenRouter / Groq avec logs de débogage
- Mémoire conversationnelle
- Résumé de liens
- File d'attente des questions
- Cache mémoire pour le mode IA
"""

import re
import base64
import requests
from collections import deque
from urllib.parse import urlparse

from config import OPENROUTER_API_KEY, GROQ_API_KEY, MODELS, DEFAULT_MODEL, MAX_HISTORY
from database import db_get_history, db_save_history, db_get_setting, db_set_setting

# ============================================================================
# CACHE MÉMOIRE POUR LE MODE IA
# ============================================================================
user_ai_mode_cache = {}

# ============================================================================
# FILES D'ATTENTE (par utilisateur)
# ============================================================================
user_queues = {}      # user_id -> deque de dicts {"question": str, "image": str}
user_processing = {}  # user_id -> bool (True si une réponse est en cours)

# ============================================================================
# FONCTIONS DE MODÈLE
# ============================================================================

def get_model_full(alias):
    """Retourne le nom complet du modèle à partir de l'alias."""
    for provider in MODELS.values():
        if alias in provider:
            return provider[alias]
    return None

def get_provider(alias):
    """Retourne le fournisseur (openrouter ou groq) pour un alias donné."""
    if alias in MODELS["openrouter"]:
        return "openrouter"
    elif alias in MODELS["groq"]:
        return "groq"
    return "openrouter"  # fallback

def is_vision_compatible(alias):
    """Vérifie si le modèle supporte la vision (images)."""
    return alias in {"gemini", "gpt-20b", "gpt-120b"}

# ============================================================================
# APPELS IA AVEC LOGS
# ============================================================================

async def ask_ai(user_id, question, image_b64=None):
    """
    Interroge l'IA avec l'historique de l'utilisateur et éventuellement une image.
    Retourne la réponse ou None en cas d'échec.
    """
    # Récupérer le modèle préféré
    model_alias = db_get_setting(user_id, 'model_alias') or DEFAULT_MODEL
    model = get_model_full(model_alias)
    if not model:
        model = get_model_full(DEFAULT_MODEL)
        model_alias = DEFAULT_MODEL

    print(f"🧠 Utilisation du modèle : {model_alias} ({model})")

    # Récupérer l'historique et le prompt système
    system_prompt = db_get_setting(user_id, 'system_prompt') or "Tu es un assistant IA utile, amical et concis."
    history = db_get_history(user_id)
    messages = [{"role": "system", "content": system_prompt}] + history

    # Construire le message utilisateur
    if image_b64 and is_vision_compatible(model_alias):
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]
        })
    else:
        messages.append({"role": "user", "content": question})

    provider = get_provider(model_alias)

    if provider == "groq":
        reply = await _call_groq(model, messages)
    else:
        reply = await _call_openrouter(model, messages)

    if reply:
        db_save_history(user_id, "user", question)
        db_save_history(user_id, "assistant", reply)
        return reply
    return None

async def _call_openrouter(model, messages):
    """Appelle l'API OpenRouter avec logs."""
    try:
        print(f"🔍 Appel OpenRouter avec le modèle : {model}")
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.7
            },
            timeout=30
        )
        print(f"🔍 OpenRouter status : {r.status_code}")
        print(f"🔍 OpenRouter réponse : {r.text[:300]}")  # Limité pour lisibilité
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            print(f"❌ OpenRouter erreur {r.status_code}: {r.text}")
    except Exception as e:
        print(f"❌ Exception OpenRouter : {e}")
    return None

async def _call_groq(model, messages):
    """Appelle l'API Groq avec logs."""
    try:
        print(f"🔍 Appel Groq avec le modèle : {model}")
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": messages,
                "max_tokens": 500
            },
            timeout=30
        )
        print(f"🔍 Groq status : {r.status_code}")
        print(f"🔍 Groq réponse : {r.text[:300]}")
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            print(f"❌ Groq erreur {r.status_code}: {r.text}")
    except Exception as e:
        print(f"❌ Exception Groq : {e}")
    return None

# ============================================================================
# RÉSUMÉ DE LIENS
# ============================================================================

async def summarize_url(url):
    """Extrait le contenu d'un lien et le résume avec l'IA."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=10)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)[:2000]

        prompt = f"Résume le contenu suivant de manière concise (2-3 phrases) :\n\n{text}"
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "google/gemini-2-flash-exp:free",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 150,
                "temperature": 0.3
            },
            timeout=15
        )
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Summarize error: {e}")
    return None

# ============================================================================
# FILE D'ATTENTE DES QUESTIONS
# ============================================================================

async def enqueue_question(user_id, question, update, context, image_b64=None):
    """
    Ajoute une question à la file d'attente de l'utilisateur.
    Si aucune réponse en cours, démarre le traitement immédiat.
    """
    if user_id not in user_queues:
        user_queues[user_id] = deque()
    if user_id not in user_processing:
        user_processing[user_id] = False

    if user_processing[user_id]:
        user_queues[user_id].append({"question": question, "image": image_b64})
        await update.message.reply_text(
            f"⏳ Question en file d'attente. Position : {len(user_queues[user_id])}"
        )
        return

    user_processing[user_id] = True
    await _process_next(user_id, update, context)

async def _process_next(user_id, update, context):
    """Traite la question suivante dans la file d'attente."""
    if user_id not in user_queues or not user_queues[user_id]:
        user_processing[user_id] = False
        return

    task = user_queues[user_id].popleft()
    question = task.get("question")
    image_b64 = task.get("image")

    try:
        reply = await ask_ai(user_id, question, image_b64)
        if reply:
            await update.message.reply_text(f"🤖 **Réponse :**\n{reply[:4096]}", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Je n'ai pas pu obtenir de réponse.")
    except Exception as e:
        print(f"Process error: {e}")
        await update.message.reply_text("❌ Une erreur est survenue.")

    await _process_next(user_id, update, context)

# ============================================================================
# GESTION DES MESSAGES (MODE IA)
# ============================================================================

async def handle_ai_message(update, context):
    """
    Fonction appelée par le handler de messages pour traiter les messages en mode IA.
    Cette fonction est importée depuis handlers/ask.py.
    """
    from telegram import Update
    from telegram.ext import ContextTypes

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    text = update.message.text or update.message.caption or ""
    is_group = update.effective_chat.type in ["group", "supergroup"]

    # Enregistrer l'utilisateur et incrémenter les stats
    from database import db_save_user, db_increment_stats
    db_save_user(user_id, update.effective_user.username, update.effective_user.full_name)
    db_increment_stats('total_messages')

    # Vérifier le mode IA (utiliser le cache)
    ai_mode = user_ai_mode_cache.get(user_id, False) or db_get_setting(user_id, 'ai_mode')

    if not ai_mode:
        if is_group:
            return
        await update.message.reply_text(
            "Utilisez `/ask_on` pour discuter avec l'IA.",
            parse_mode="Markdown"
        )
        return

    # --- Mode IA activé ---

    # Si c'est une photo
    if update.message.photo:
        caption = text or "Que vois-tu sur cette image ?"
        msg = await update.message.reply_text("🖼️ Analyse...")
        try:
            photo = update.message.photo[-1]
            file = await context.bot.get_file(photo.file_id)
            file_data = await file.download_as_bytearray()
            image_b64 = base64.b64encode(file_data).decode('utf-8')
            await msg.edit_text("🧠 Réflexion...")
            await enqueue_question(user_id, caption, update, context, image_b64)
            await msg.delete()
        except Exception as e:
            print(f"Vision error: {e}")
            await msg.edit_text("❌ Erreur d'analyse.")
        return

    # Si le message contient un lien
    if text and re.search(r'https?://[^\s]+', text):
        urls = re.findall(r'https?://[^\s]+', text)
        for url in urls[:1]:
            summary = await summarize_url(url)
            if summary:
                await update.message.reply_text(f"📝 **Résumé** :\n{summary}", parse_mode="Markdown")
            else:
                await update.message.reply_text("❌ Impossible d'analyser ce lien.")
        return

    # Message texte normal
    if text and not text.startswith('/'):
        await enqueue_question(user_id, text, update, context)
