# -*- coding: utf-8 -*-
import os
import sys
import logging
import threading

from config import TELEGRAM_TOKEN, WEB_PORT
from database import init_db
from handlers import (
    start, help_command, status, ask_command, vision_command,
    ask_on, ask_off, clear_memory, change_model, set_prompt,
    generate_image, text_to_speech, translate_command, stats_command
)
from web import create_app, run_web_server

# ===== Configuration des logs =====
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/shadow_bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ===== Lancement du bot Telegram =====
def run_bot():
    """Lance le bot Telegram en polling."""
    from telegram.ext import Application, CommandHandler, MessageHandler, filters

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commandes
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("ask", ask_command))
    app.add_handler(CommandHandler("vision", vision_command))
    app.add_handler(CommandHandler("ask_on", ask_on))
    app.add_handler(CommandHandler("ask_off", ask_off))
    app.add_handler(CommandHandler("clear_memory", clear_memory))
    app.add_handler(CommandHandler("model", change_model))
    app.add_handler(CommandHandler("setprompt", set_prompt))
    app.add_handler(CommandHandler("image", generate_image))
    app.add_handler(CommandHandler("tts", text_to_speech))
    app.add_handler(CommandHandler("translate", translate_command))
    app.add_handler(CommandHandler("stats", stats_command))

    # Gestion des messages (mode IA)
    from handlers import handle_message
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_message))

    logger.info("🤖 Bot Telegram démarré")
    app.run_polling()

# ===== Point d'entrée =====
if __name__ == "__main__":
    # Initialiser la DB
    init_db()

    # Démarrer le serveur web dans un thread (pour le monitoring)
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    logger.info(f"🌐 Serveur web démarré sur le port {WEB_PORT}")

    # Démarrer le bot (bloque le thread principal)
    run_bot()