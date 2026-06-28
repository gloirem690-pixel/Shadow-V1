# handlers/model.py
from telegram import Update
from telegram.ext import ContextTypes
from database import db_set_setting
from config import MODELS

async def change_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Usage : `/model <alias>`\n\nAlias disponibles :\n"
            "🔹 OpenRouter : gpt-20b, gpt-120b, gemini, llama-8b, mistral\n"
            "🔹 Groq : llama-70b, mixtral",
            parse_mode="Markdown"
        )
        return
    alias = context.args[0].lower()
    user_id = update.effective_user.id
    for provider in MODELS.values():
        if alias in provider:
            db_set_setting(user_id, 'model_alias', alias)
            await update.message.reply_text(f"✅ Modèle changé : `{alias}` → `{provider[alias]}`", parse_mode="Markdown")
            return
    await update.message.reply_text(f"❌ Alias `{alias}` inconnu.", parse_mode="Markdown")

async def set_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Usage : `/setprompt <prompt>`\nExemple : `/setprompt Tu es un assistant juridique.`",
            parse_mode="Markdown"
        )
        return
    user_id = update.effective_user.id
    prompt = " ".join(context.args)
    db_set_setting(user_id, 'system_prompt', prompt)
    await update.message.reply_text(f"✅ Prompt personnalisé enregistré !\n\n`{prompt}`", parse_mode="Markdown")