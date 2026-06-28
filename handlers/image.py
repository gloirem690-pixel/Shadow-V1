# handlers/image.py
import os, tempfile
from urllib.parse import quote
import requests
from telegram import Update
from telegram.ext import ContextTypes

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🖼️ Usage : `/image <prompt>`", parse_mode="Markdown")
        return
    prompt = " ".join(context.args)
    msg = await update.message.reply_text(f"🎨 Génération : {prompt[:50]}...")
    try:
        encoded = quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=flux"
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(r.content)
                tmp_path = tmp.name
            with open(tmp_path, "rb") as photo:
                await update.message.reply_photo(photo, caption=f"✨ {prompt[:100]}")
            os.unlink(tmp_path)
            await msg.delete()
        else:
            await msg.edit_text(f"❌ Erreur {r.status_code}")
    except Exception as e:
        await msg.edit_text("❌ Erreur de génération.")