"""
Memory System for Gena AI
Manages all persistent data using SQLite
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path


class Memory:
    """SQLite-based memory management"""
    
    def __init__(self, db_path="memory.db"):
        """Initialize memory database"""
        self.db_path = Path(db_path)
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Create database tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Access columns by name
        cursor = self.conn.cursor()
        
        # Settings table (persona, preferences, configs)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            )
        ''')
        
        # User info table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_info (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            )
        ''')
        
        # Learned facts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facts (
                topic TEXT PRIMARY KEY,
                content TEXT,
                learned_at TEXT
            )
        ''')
        
        # Learned procedures table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS procedures (
                name TEXT PRIMARY KEY,
                steps TEXT,
                learned_at TEXT
            )
        ''')
        
        # Conversation history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                role TEXT,
                message TEXT
            )
        ''')
        
        # Metadata table (interaction count, etc.)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        self.conn.commit()
        
        # Initialize defaults
        self._init_defaults()
    
    def _init_defaults(self):
        """Set default values if not present"""
        if not self.get_metadata('interaction_count'):
            self.set_metadata('interaction_count', '0')
        
        if not self.get_metadata('first_interaction'):
            self.set_metadata('first_interaction', datetime.now().isoformat())
    
    # ==================== METADATA ====================
    
    def get_metadata(self, key):
        """Get metadata value"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT value FROM metadata WHERE key = ?', (key,))
        row = cursor.fetchone()
        return row['value'] if row else None
    
    def set_metadata(self, key, value):
        """Set metadata value"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO metadata (key, value) 
            VALUES (?, ?)
        ''', (key, str(value)))
        self.conn.commit()
    
    def increment_interaction_count(self):
        """Increment and return interaction count"""
        count = int(self.get_metadata('interaction_count') or 0)
        count += 1
        self.set_metadata('interaction_count', count)
        return count
    
    # ==================== USER INFO ====================
    
    def get_user_info(self, key=None):
        """Get user info (all or specific key)"""
        cursor = self.conn.cursor()
        if key:
            cursor.execute('SELECT value FROM user_info WHERE key = ?', (key,))
            row = cursor.fetchone()
            return row['value'] if row else None
        else:
            cursor.execute('SELECT key, value FROM user_info')
            return {row['key']: row['value'] for row in cursor.fetchall()}
    
    def set_user_info(self, key, value):
        """Set user info"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO user_info (key, value, updated_at) 
            VALUES (?, ?, ?)
        ''', (key, value, datetime.now().isoformat()))
        self.conn.commit()
    
    # ==================== SETTINGS ====================
    
    def get_setting(self, key):
        """Get a setting"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cursor.fetchone()
        return row['value'] if row else None
    
    def set_setting(self, key, value):
        """Set a setting"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value, updated_at) 
            VALUES (?, ?, ?)
        ''', (key, value, datetime.now().isoformat()))
        self.conn.commit()
    
    # ==================== FACTS ====================
    
    def get_fact(self, topic):
        """Get a learned fact"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT content FROM facts WHERE topic = ?', (topic,))
        row = cursor.fetchone()
        return row['content'] if row else None
    
    def get_all_facts(self):
        """Get all learned facts"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT topic, content FROM facts')
        return {row['topic']: row['content'] for row in cursor.fetchall()}
    
    def learn_fact(self, topic, content):
        """Learn a new fact"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO facts (topic, content, learned_at) 
            VALUES (?, ?, ?)
        ''', (topic, content, datetime.now().isoformat()))
        self.conn.commit()
        return f"Got it! I'll remember that about {topic}."
    
    def get_facts_count(self):
        """Get count of learned facts"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM facts')
        return cursor.fetchone()['count']
    
    # ==================== PROCEDURES ====================
    
    def get_procedure(self, name):
        """Get a learned procedure"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT steps FROM procedures WHERE name = ?', (name,))
        row = cursor.fetchone()
        if row:
            return json.loads(row['steps'])
        return None
    
    def get_all_procedures(self):
        """Get all learned procedures"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT name, steps FROM procedures')
        return {row['name']: json.loads(row['steps']) for row in cursor.fetchall()}
    
    def learn_procedure(self, name, steps):
        """Learn a new procedure"""
        cursor = self.conn.cursor()
        # Store steps as JSON
        steps_json = json.dumps(steps if isinstance(steps, list) else [steps])
        cursor.execute('''
            INSERT OR REPLACE INTO procedures (name, steps, learned_at) 
            VALUES (?, ?, ?)
        ''', (name, steps_json, datetime.now().isoformat()))
        self.conn.commit()
        return f"Yay! I learned how to {name}!"
    
    def get_procedures_list(self):
        """Get list of procedure names"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT name FROM procedures')
        return [row['name'] for row in cursor.fetchall()]
    
    # ==================== CONVERSATION HISTORY ====================
    
    def add_message(self, role, message):
        """Add message to conversation history"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (timestamp, role, message) 
            VALUES (?, ?, ?)
        ''', (datetime.now().isoformat(), role, message))
        self.conn.commit()
    
    def get_recent_conversations(self, limit=10):
        """Get recent conversation history"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT timestamp, role, message 
            FROM conversations 
            ORDER BY id DESC 
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        return [(row['timestamp'], row['role'], row['message']) for row in reversed(rows)]
    
    def clear_old_conversations(self, keep_last=20):
        """Keep only recent conversations"""
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM conversations 
            WHERE id NOT IN (
                SELECT id FROM conversations 
                ORDER BY id DESC 
                LIMIT ?
            )
        ''', (keep_last,))
        self.conn.commit()
    
    # ==================== CONTEXT BUILDING ====================
    
    def get_context_summary(self):
        """Build compact context for LLM"""
        context = f"\n[MEMORY]\n"
        
        # Interaction count
        count = self.get_metadata('interaction_count')
        context += f"Chats: {count} | "
        
        # User info
        user_info = self.get_user_info()
        if user_info:
            context += f"User: {json.dumps(user_info)}\n"
        else:
            context += "\n"
        
        # Facts summary
        facts_count = self.get_facts_count()
        if facts_count > 0:
            context += f"Facts learned: {facts_count}\n"
        
        # Procedures summary
        procedures = self.get_procedures_list()
        if procedures:
            context += f"Procedures: {', '.join(procedures)}\n"
        
        # Recent conversations
        recent = self.get_recent_conversations(limit=4)
        if recent:
            context += "Recent:\n"
            for timestamp, role, message in recent:
                time_str = datetime.fromisoformat(timestamp).strftime("%H:%M")
                role_char = 'U' if role == 'user' else 'G'
                context += f"[{time_str}] {role_char}: {message}\n"
        
        return context
    
    # ==================== CLEANUP ====================
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def export_all(self):
        """Export all memory as JSON (for debugging)"""
        return {
            'metadata': {
                'interaction_count': self.get_metadata('interaction_count'),
                'first_interaction': self.get_metadata('first_interaction')
            },
            'user_info': self.get_user_info(),
            'settings': self._get_all_settings(),
            'facts': self.get_all_facts(),
            'procedures': self.get_all_procedures(),
            'recent_conversations': self.get_recent_conversations(limit=20)
        }
    
    def _get_all_settings(self):
        """Get all settings"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT key, value FROM settings')
        return {row['key']: row['value'] for row in cursor.fetchall()}
