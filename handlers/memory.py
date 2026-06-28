# handlers/memory.py
import sqlite3
from telegram import Update
from telegram.ext import ContextTypes
from config import DB_PATH

async def clear_memory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM history WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    await update.message.reply_text("🧹 Mémoire effacée.")