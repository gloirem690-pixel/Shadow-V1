# handlers/start.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import db_save_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_save_user(user.id, user.username, user.full_name)
    keyboard = [
        [InlineKeyboardButton("➕ Ajouter à un groupe", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("🧠 Modèles IA", callback_data='model_list')],
        [InlineKeyboardButton("🖼️ Aide Image", callback_data='image_help')],
        [InlineKeyboardButton("🔊 Aide Audio", callback_data='tts_help')],
    ]
    text = (
        "⚡ **Shadow V1 - Assistant IA**\n\n"
        "🤖 **Mode IA :**\n"
        "• `/ask_on` – Activer la discussion avec l'IA\n"
        "• `/ask_off` – Désactiver\n"
        "• `/ask <question>` – Question unique\n"
        "• `/vision <question>` – Analyser une image\n\n"
        "🔧 **Personnalisation :**\n"
        "• `/model <alias>` – Changer de modèle\n"
        "• `/setprompt <prompt>` – Définir le rôle du bot\n"
        "• `/clear_memory` – Effacer l'historique\n"
        "• `/status` – État du bot\n\n"
        "🌐 **Utilitaires :**\n"
        "• `/translate <lang> <texte>` – Traduire\n"
        "• `/stats` – Statistiques\n\n"
        "🎨 **Création :**\n"
        "• `/image <prompt>` – Générer une image\n"
        "• `/tts <texte>` – Synthèse vocale\n\n"
        "📸 **Vision :** Envoyez une photo en mode IA."
    )
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📋 **Aide complète**\n\n"
        "🤖 **IA :**\n"
        "/ask_on – Activer le mode conversation\n"
        "/ask_off – Désactiver\n"
        "/ask <question> – Question unique\n"
        "/vision <question> – Analyser une image\n"
        "/setprompt <prompt> – Changer le rôle du bot\n\n"
        "🔧 **Gestion :**\n"
        "/model <alias> – Changer de modèle\n"
        "/clear_memory – Effacer l'historique\n"
        "/status – État du bot\n\n"
        "🌐 **Utilitaires :**\n"
        "/translate <lang> <texte> – Traduire\n"
        "/stats – Statistiques\n\n"
        "🎨 **Création :**\n"
        "/image <prompt> – Générer une image\n"
        "/tts <texte> – Synthèse vocale"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from database import db_get_setting, db_get_history, db_get_warnings
    from config import MAX_HISTORY, DEFAULT_MODEL
    from utils import get_model_full
    user_id = update.effective_user.id
    db_save_user(user_id, update.effective_user.username, update.effective_user.full_name)
    ai_mode = db_get_setting(user_id, 'ai_mode') or False
    model_alias = db_get_setting(user_id, 'model_alias') or DEFAULT_MODEL
    model_full = get_model_full(model_alias)
    prompt = db_get_setting(user_id, 'system_prompt') or "Tu es un assistant IA utile, amical et concis."
    history_len = len(db_get_history(user_id))
    text = (
        f"🟢 **État :**\n"
        f"• Mode IA : {'✅' if ai_mode else '❌'}\n"
        f"• Modèle : `{model_alias}` → `{model_full}`\n"
        f"• Prompt : `{prompt[:30]}...`\n"
        f"• Échanges mémorisés : {history_len//2}/{MAX_HISTORY}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")