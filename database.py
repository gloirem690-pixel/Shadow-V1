import sqlite3
from datetime import datetime
from config import DB_PATH, MAX_HISTORY

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        first_seen TIMESTAMP,
        last_seen TIMESTAMP,
        message_count INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        content TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_settings (
        user_id INTEGER PRIMARY KEY,
        model_alias TEXT DEFAULT 'gpt-20b',
        system_prompt TEXT DEFAULT 'Tu es un assistant IA utile, amical et concis.',
        language TEXT DEFAULT 'fr',
        ai_mode INTEGER DEFAULT 0,
        UNIQUE(user_id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stat_key TEXT UNIQUE,
        stat_value INTEGER DEFAULT 0
    )''')
    for key in ['total_messages', 'total_commands']:
        c.execute('INSERT OR IGNORE INTO stats (stat_key, stat_value) VALUES (?, 0)', (key,))
    conn.commit()
    conn.close()

def db_save_user(user_id, username, full_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('SELECT first_seen, message_count FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    if row:
        first_seen = row[0]
        message_count = row[1] + 1
    else:
        first_seen = now
        message_count = 1
    c.execute('''
        INSERT OR REPLACE INTO users (user_id, username, full_name, first_seen, last_seen, message_count)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, username or '', full_name or '', first_seen, now, message_count))
    conn.commit()
    conn.close()

# ... (toutes les autres fonctions de DB du code précédent)
# Je ne répète pas tout ici pour la lisibilité, mais elles sont toutes reprises
