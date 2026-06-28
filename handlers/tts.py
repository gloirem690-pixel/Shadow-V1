# handlers/tts.py
import os, tempfile
from urllib.parse import quote
import requests
from telegram import Update
from telegram.ext import ContextTypes

async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🔊 Usage : `/tts <texte>`", parse_mode="Markdown")
        return
    text = " ".join(context.args)
    msg = await update.message.reply_text("🎙️ Synthèse vocale...")
    try:
        encoded = quote(text)
        url = f"https://text.pollinations.ai/{encoded}?model=openai-audio&voice=nova"
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp.write(r.content)
                tmp_path = tmp.name
            with open(tmp_path, "rb") as audio:
                await update.message.reply_voice(audio, caption=f"🔊 {text[:50]}...")
            os.unlink(tmp_path)
            await msg.delete()
        else:
            await msg.edit_text(f"❌ Erreur {r.status_code}")
    except Exception as e:
        await msg.edit_text("❌ Erreur de synthèse.")