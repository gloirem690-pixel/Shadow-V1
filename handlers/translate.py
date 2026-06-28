# handlers/translate.py
import requests
from telegram import Update
from telegram.ext import ContextTypes
from config import OPENROUTER_API_KEY

async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage : `/translate <langue> <texte>`\nExemple : `/translate en Bonjour`", parse_mode="Markdown")
        return
    target_lang = context.args[0]
    text = " ".join(context.args[1:])
    await update.message.reply_text("🌐 Traduction en cours...")
    prompt = f"Traduis le texte suivant en {target_lang} : {text}"
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
            json={"model": "google/gemini-2-flash-exp:free", "messages": [{"role": "user", "content": prompt}], "max_tokens": 200, "temperature": 0.3},
            timeout=15
        )
        if r.status_code == 200:
            translation = r.json()["choices"][0]["message"]["content"]
            await update.message.reply_text(f"🌐 **Traduction ({target_lang}) :**\n{translation}", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Erreur de traduction.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur : {e}")