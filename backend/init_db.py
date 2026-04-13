import sqlite3
import os

DB_PATH = "/home/agentpi003/dish-chat/backend/agent_memory.db"

def init_database():
    """Create database and tables"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Journal entries
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            chat_id TEXT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            metadata TEXT
        )
    """)
    
    # Methodology rules
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS methodology_rules (
            rule_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            effectiveness REAL DEFAULT 0.5,
            times_applied INTEGER DEFAULT 0,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    """)
    
    # Long-term memory
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS long_term_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            message_role TEXT NOT NULL,
            message_content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            importance_score REAL DEFAULT 0.5,
            tags TEXT
        )
    """)
    
    # Personality profile
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personality_profile (
            dimension TEXT PRIMARY KEY,
            value REAL NOT NULL,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            evolution_history TEXT
        )
    """)
    
    # Tool usage analytics
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tool_usage_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_name TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            success BOOLEAN,
            execution_time_ms INTEGER,
            context TEXT
        )
    """)
    
    # Conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            chat_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            messages TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            metadata TEXT
        )
    """)
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized: {DB_PATH}")
    if os.path.exists(DB_PATH):
        print(f"   Size: {os.path.getsize(DB_PATH) / 1024:.2f} KB")

if __name__ == "__main__":
    init_database()
