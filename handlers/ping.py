# handlers/ping.py
from telegram import Update
from telegram.ext import ContextTypes

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Répond simplement 'Pong !' pour tester la connexion."""
    await update.message.reply_text("🏓 Pong !")