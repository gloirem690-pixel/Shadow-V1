import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuration des logs pour voir si tout fonctionne
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# ⚠️ REMPLACE ICI PAR TON TOKEN BOTFATHER
TOKEN = "8839158242:AAEpT2-eG6t4lDCsT1bo4j6UqJtd4hxt3G0"

# Commande /start (Message de bienvenue avec boutons)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "⚡ **Shadow V1 est opérationnel.**\n\n"
        "Bonjour ! Je suis l'assistant de l'ombre conçu pour sécuriser, "
        "modérer et automatiser vos espaces sur Telegram.\n\n"
        "Utilisez les boutons ci-dessous pour explorer mes capacités ou m'ajouter à votre communauté."
    )
    
    # Création des boutons sous le message
    keyboard = [
        [InlineKeyboardButton("➕ Ajouter Shadow V1 à un groupe", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("🛡️ Menu Admin / Modération", callback_data='admin_menu')],
        [InlineKeyboardButton("📢 Canal d'Annonces", url="https://t.me/Telegram")] # Tu pourras changer ce lien plus tard
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# Commande /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "🤖 **Commandes disponibles :**\n\n"
        "👤 *Pour tous :*\n"
        "/start - Relancer le bot\n"
        "/help - Afficher l'aide\n"
        "/status - Vérifier l'état du bot\n\n"
        "🛡️ *Pour les Admins (Dans un groupe) :*\n"
        "/ban [nom] - Bannir un membre\n"
        "/mute [nom] - Muter un membre\n"
        "/unmute [nom] - Unmute un membre\n"
        "/warn [nom] - Donner un avertissement\n"
        "/clear [nombre] - Supprimer des messages"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# Commande /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🟢 Shadow V1 est en ligne et tous les systèmes sont opérationnels.")

def main() -> None:
    # Lancement du bot
    application = Application.builder().token(TOKEN).build()

    # Liaison des commandes aux fonctions
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))

    # Démarrage du bot (polling)
    print("⚡ Shadow V1 est en cours de démarrage...")
    application.run_polling()

if __name__ == '__main__':
    main()
