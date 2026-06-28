# handlers/stats.py
import sqlite3
from telegram import Update
from telegram.ext import ContextTypes
from config import DB_PATH
from database import db_get_stats

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = db_get_stats()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0]
    conn.close()
    text = (
        f"📊 **Statistiques**\n\n"
        f"👥 Utilisateurs : {total_users}\n"
        f"💬 Messages : {stats.get('total_messages', 0)}\n"
        f"⚡ Commandes : {stats.get('total_commands', 0)}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")