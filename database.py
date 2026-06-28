# -*- coding: utf-8 -*-
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

# ===== FONCTIONS MANQUANTES =====
def db_get_setting(user_id, key):
    """Récupère un paramètre utilisateur (model_alias, system_prompt, ai_mode, etc.)."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f'SELECT {key} FROM user_settings WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    if result is not None:
        value = result[0]
        if key == 'ai_mode':
            return bool(value)
        return value
    if key == 'ai_mode':
        return False
    return None

def db_set_setting(user_id, key, value):
    """Enregistre un paramètre utilisateur."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if key == 'ai_mode':
        value = 1 if value else 0
    c.execute(f'INSERT OR REPLACE INTO user_settings (user_id, {key}) VALUES (?, ?)', (user_id, value))
    conn.commit()
    conn.close()

def db_save_history(user_id, role, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO history (user_id, role, content) VALUES (?, ?, ?)', (user_id, role, content))
    c.execute('''
        DELETE FROM history 
        WHERE id NOT IN (
            SELECT id FROM history WHERE user_id = ? 
            ORDER BY timestamp DESC LIMIT ?
        )
    ''', (user_id, MAX_HISTORY * 2))
    conn.commit()
    conn.close()

def db_get_history(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT role, content FROM history WHERE user_id = ? ORDER BY timestamp ASC', (user_id,))
    rows = c.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]

def db_increment_stats(key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE stats SET stat_value = stat_value + 1 WHERE stat_key = ?', (key,))
    conn.commit()
    conn.close()

def db_get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT stat_key, stat_value FROM stats')
    stats = dict(c.fetchall())
    conn.close()
    return stats