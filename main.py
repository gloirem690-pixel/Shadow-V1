# -*- coding: utf-8 -*-
import os
import sys
import logging
import threading

from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, filters

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

# ===== CRÉER L'APPLICATION FLASK POUR VERCEL =====
# Vercel cherche une instance nommée "app" dans le fichier d'entrée
app = create_app()

# ===== Lancement du bot Telegram (en local ou en arrière‑plan) =====
def run_bot():
    """Lance le bot Telegram."""
    bot_app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Commandes
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("help", help_command))
    bot_app.add_handler(CommandHandler("status", status))
    bot_app.add_handler(CommandHandler("ask", ask_command))
    bot_app.add_handler(CommandHandler("vision", vision_command))
    bot_app.add_handler(CommandHandler("ask_on", ask_on))
    bot_app.add_handler(CommandHandler("ask_off", ask_off))
    bot_app.add_handler(CommandHandler("clear_memory", clear_memory))
    bot_app.add_handler(CommandHandler("model", change_model))
    bot_app.add_handler(CommandHandler("setprompt", set_prompt))
    bot_app.add_handler(CommandHandler("image", generate_image))
    bot_app.add_handler(CommandHandler("tts", text_to_speech))
    bot_app.add_handler(CommandHandler("translate", translate_command))
    bot_app.add_handler(CommandHandler("stats", stats_command))

    # Gestion des messages (mode IA)
    from handlers import handle_message
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    bot_app.add_handler(MessageHandler(filters.PHOTO, handle_message))

    logger.info("🤖 Bot Telegram démarré")
    bot_app.run_polling()

# ===== Point d'entrée pour l'exécution locale =====
if __name__ == "__main__":
    # Initialiser la DB
    init_db()

    # Démarrer le serveur web dans un thread (pour le monitoring)
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    logger.info(f"🌐 Serveur web démarré sur le port {WEB_PORT}")

    # Démarrer le bot
    run_bot()
