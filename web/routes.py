import time
import sqlite3
import requests
from flask import jsonify, render_template_string
from config import TELEGRAM_TOKEN, DB_PATH
from web.templates import HTML_TEMPLATE

def register_routes(app):
    
    @app.route('/')
    def index():
        return render_template_string(HTML_TEMPLATE)
    
    @app.route('/logs')
    def logs():
        try:
            with open('logs/shadow_bot.log', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            last_lines = lines[-100:] if len(lines) >= 100 else lines
            return ''.join(last_lines)
        except Exception as e:
            return f"Erreur de lecture des logs: {e}"
    
    @app.route('/ping')
    def ping():
        try:
            start = time.time()
            r = requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe", timeout=5)
            ping_ms = round((time.time() - start) * 1000)
            if r.status_code == 200:
                return jsonify({'status': 'ok', 'ping': ping_ms})
            return jsonify({'status': 'error', 'ping': None})
        except:
            return jsonify({'status': 'error', 'ping': None})
    
    @app.route('/stats')
    def stats():
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM users')
        users = c.fetchone()[0]
        c.execute('SELECT stat_key, stat_value FROM stats')
        stats = dict(c.fetchall())
        conn.close()
        return jsonify({
            'users': users,
            'messages': stats.get('total_messages', 0),
            'commands': stats.get('total_commands', 0)
        })
    
    @app.route('/charts_data')
    def charts_data():
        # Données d'exemple
        return jsonify({
            'activity': [12, 19, 3, 5, 2, 3, 15],
            'models': {'GPT-20B': 45, 'Gemini': 30, 'Llama-70B': 25}
        })
