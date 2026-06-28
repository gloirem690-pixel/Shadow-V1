# handlers/ping.py
import time
from telegram import Update
from telegram.ext import ContextTypes

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Renvoie le temps de latence vers l'API Telegram."""
    start = time.time()
    # Envoyer un message "Ping..." puis le modifier pour mesurer le temps
    msg = await update.message.reply_text("🏓 Ping...")
    end = time.time()
    latency_ms = round((end - start) * 1000)
    await msg.edit_text(f"🏓 Pong !\nLatence : {latency_ms} ms")