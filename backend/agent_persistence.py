"""
Agent Memory Persistence Layer
Handles all database operations for self-improvement features
"""

import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager
from typing import Dict, List, Optional

DB_PATH = '/home/agentpi003/dish-chat/backend/agent_memory.db'

@contextmanager
def get_db_connection():
    """Database connection context manager"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Journal Functions
def save_journal_entry(entry: Dict) -> int:
    """Save journal entry and return ID"""
    with get_db_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO journal_entries (type, chat_id, content, metadata) 
               VALUES (?, ?, ?, ?)""",
            (entry['type'], entry.get('chat_id'), entry['content'], 
             json.dumps(entry.get('metadata', {})))
        )
        return cursor.lastrowid

def load_journal_entries(limit: int = 100) -> List[Dict]:
    """Load recent journal entries"""
    with get_db_connection() as conn:
        cursor = conn.execute(
            "SELECT * FROM journal_entries ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        return [dict(row) for row in cursor.fetchall()]

# Methodology Functions
def save_methodology_rule(rule_id: str, rule_data: Dict):
    """Save or update methodology rule"""
    with get_db_connection() as conn:
        conn.execute(
            """INSERT OR REPLACE INTO methodology_rules 
               (rule_id, title, effectiveness, times_applied, last_updated)
               VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)""",
            (rule_id, rule_data['title'], rule_data['effectiveness'], 
             rule_data['times_applied'])
        )

def load_methodology_rules() -> Dict:
    """Load all methodology rules"""
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM methodology_rules")
        rules = {}
        for row in cursor.fetchall():
            rules[row['rule_id']] = {
                'title': row['title'],
                'effectiveness': row['effectiveness'],
                'times_applied': row['times_applied']
            }
        return rules

# Long-term Memory Functions
def save_long_term_message(chat_id: str, role: str, content: str, 
                          importance: float = 0.5, tags: Optional[str] = None):
    """Save message to long-term memory"""
    with get_db_connection() as conn:
        conn.execute(
            """INSERT INTO long_term_memory 
               (chat_id, message_role, message_content, importance_score, tags)
               VALUES (?, ?, ?, ?, ?)""",
            (chat_id, role, content, importance, tags)
        )

def get_relevant_memories(chat_id: Optional[str] = None, 
                         limit: int = 50) -> List[Dict]:
    """Retrieve relevant long-term memories"""
    with get_db_connection() as conn:
        if chat_id:
            cursor = conn.execute(
                """SELECT * FROM long_term_memory 
                   WHERE chat_id = ? 
                   ORDER BY importance_score DESC, timestamp DESC 
                   LIMIT ?""",
                (chat_id, limit)
            )
        else:
            cursor = conn.execute(
                """SELECT * FROM long_term_memory 
                   ORDER BY importance_score DESC, timestamp DESC 
                   LIMIT ?""",
                (limit,)
            )
        return [dict(row) for row in cursor.fetchall()]

def calculate_importance(content: str) -> float:
    """Calculate importance score for memory"""
    score = 0.5
    
    # Length bonus
    if len(content) > 200: score += 0.1
    
    # Keyword importance
    important_keywords = ['error', 'fix', 'issue', 'problem', 'solution']
    if any(kw in content.lower() for kw in important_keywords):
        score += 0.2
    
    # Positive feedback
    if any(kw in content.lower() for kw in ['thank', 'great', 'perfect', 'excellent']):
        score += 0.1
    
    return min(score, 1.0)

# Personality Functions
def save_personality_dimension(dimension: str, value: float):
    """Save personality dimension value"""
    with get_db_connection() as conn:
        # Get current history
        cursor = conn.execute(
            "SELECT evolution_history FROM personality_profile WHERE dimension = ?",
            (dimension,)
        )
        row = cursor.fetchone()
        
        history = []
        if row and row['evolution_history']:
            history = json.loads(row['evolution_history'])
        
        history.append({'value': value, 'timestamp': datetime.utcnow().isoformat()})
        
        conn.execute(
            """INSERT OR REPLACE INTO personality_profile 
               (dimension, value, last_updated, evolution_history)
               VALUES (?, ?, CURRENT_TIMESTAMP, ?)""",
            (dimension, value, json.dumps(history[-10:]))  # Keep last 10 changes
        )

def load_personality_profile() -> Dict:
    """Load personality profile"""
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM personality_profile")
        return {row['dimension']: row['value'] for row in cursor.fetchall()}

# Analytics Functions
def log_tool_usage(tool_name: str, success: bool, 
                  execution_time_ms: int, context: Optional[str] = None):
    """Log tool usage for analytics"""
    with get_db_connection() as conn:
        conn.execute(
            """INSERT INTO tool_usage_analytics 
               (tool_name, success, execution_time_ms, context)
               VALUES (?, ?, ?, ?)""",
            (tool_name, success, execution_time_ms, context)
        )

def get_tool_analytics(days: int = 7) -> List[Dict]:
    """Get tool usage analytics"""
    with get_db_connection() as conn:
        cursor = conn.execute(
            """SELECT tool_name, 
                      COUNT(*) as total_uses,
                      SUM(CASE WHEN success THEN 1 ELSE 0 END) as successes,
                      AVG(execution_time_ms) as avg_time_ms
               FROM tool_usage_analytics
               WHERE timestamp > datetime('now', '-' || ? || ' days')
               GROUP BY tool_name""",
            (days,)
        )
        return [dict(row) for row in cursor.fetchall()]

# Database Statistics
def get_database_stats() -> Dict:
    """Get database statistics"""
    with get_db_connection() as conn:
        stats = {}
        
        # Count entries in each table
        for table in ['journal_entries', 'methodology_rules', 'long_term_memory', 
                     'personality_profile', 'tool_usage_analytics']:
            cursor = conn.execute(f"SELECT COUNT(*) as count FROM {table}")
            stats[table] = cursor.fetchone()['count']
        
        return stats

def init_database():
    """Initialize database (called from init_db.py)"""
    import init_db
    init_db.init_database()

if __name__ == '__main__':
    # Test database connection
    try:
        stats = get_database_stats()
        print("✅ Database connection successful")
        print("📊 Database statistics:")
        for table, count in stats.items():
            print(f"   {table}: {count} entries")
    except Exception as e:
        print(f"❌ Database error: {e}")
