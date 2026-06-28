# handlers/ask.py
import base64
import re
from telegram import Update
from telegram.ext import ContextTypes
from database import db_get_setting, db_set_setting
from utils import enqueue_question, summarize_url, user_ai_mode_cache

async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage : `/ask <question>`", parse_mode="Markdown")
        return
    question = " ".join(context.args)
    user_id = update.effective_user.id
    await enqueue_question(user_id, question, update, context)

async def vision_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not update.message.photo:
        await update.message.reply_text("❌ Usage : `/vision <question>` avec une photo", parse_mode="Markdown")
        return
    question = " ".join(context.args)
    user_id = update.effective_user.id
    msg = await update.message.reply_text("🖼️ Analyse...")
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        file_data = await file.download_as_bytearray()
        image_b64 = base64.b64encode(file_data).decode('utf-8')
        await msg.edit_text("🧠 Réflexion...")
        await enqueue_question(user_id, question, update, context, image_b64)
        await msg.delete()
    except Exception as e:
        await msg.edit_text("❌ Erreur d'analyse.")

async def ask_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db_set_setting(user_id, 'ai_mode', True)
    user_ai_mode_cache[user_id] = True
    await update.message.reply_text(
        "🧠 **Mode IA activé !**\n\nJe répondrai à toutes vos questions.\nPour désactiver : `/ask_off`",
        parse_mode="Markdown"
    )

async def ask_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db_set_setting(user_id, 'ai_mode', False)
    user_ai_mode_cache[user_id] = False
    await update.message.reply_text("🔇 **Mode IA désactivé.**", parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les messages en mode IA."""
    from utils import handle_ai_message
    await handle_ai_message(update, context)