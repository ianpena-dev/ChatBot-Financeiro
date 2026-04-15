"""
Context Persistence Module
Handles conversation history and user context storage
"""

import json
import sqlite3
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class ContextManager:
    """Manage conversation context and persistence"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize context manager
        
        Args:
            db_path: Path to SQLite database
        """
        if db_path is None:
            db_path = os.getenv('DATABASE_PATH', 'data/chatbot.db')
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            # Conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role TEXT,
                    message TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    intent TEXT,
                    context TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                )
            ''')
            
            # User profiles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id TEXT PRIMARY KEY,
                    profile_data TEXT,
                    preferences TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Financial goals table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS financial_goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    goal_type TEXT,
                    target_amount REAL,
                    current_amount REAL DEFAULT 0,
                    deadline TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
                )
            ''')
            
            conn.commit()
    
    def create_session(self, session_id: str, user_id: Optional[str] = None) -> Dict:
        """
        Create a new conversation session
        
        Args:
            session_id: Unique session identifier
            user_id: Optional user identifier
        
        Returns:
            Session information
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO sessions (session_id, user_id) VALUES (?, ?)',
                (session_id, user_id)
            )
            conn.commit()
        
        return {
            'session_id': session_id,
            'user_id': user_id,
            'created_at': datetime.now().isoformat()
        }
    
    def save_message(self, session_id: str, role: str, message: str,
                    intent: Optional[str] = None, context: Optional[Dict] = None):
        """
        Save a conversation message
        
        Args:
            session_id: Session identifier
            role: Message role (user/assistant/system)
            message: Message content
            intent: Detected intent
            context: Message context
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO conversations (session_id, role, message, intent, context) VALUES (?, ?, ?, ?, ?)',
                (session_id, role, message, intent, json.dumps(context) if context else None)
            )
            
            # Update session last activity
            cursor.execute(
                'UPDATE sessions SET last_activity = CURRENT_TIMESTAMP WHERE session_id = ?',
                (session_id,)
            )
            conn.commit()
    
    def get_conversation_history(self, session_id: str, limit: int = 20) -> List[Dict]:
        """
        Get conversation history for a session
        
        Args:
            session_id: Session identifier
            limit: Maximum number of messages to retrieve
        
        Returns:
            List of conversation messages
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT role, message, timestamp, intent, context
                   FROM conversations
                   WHERE session_id = ?
                   ORDER BY timestamp DESC
                   LIMIT ?''',
                (session_id, limit)
            )
            
            messages = cursor.fetchall()
            return [
                {
                    'role': msg['role'],
                    'message': msg['message'],
                    'timestamp': msg['timestamp'],
                    'intent': msg['intent'],
                    'context': json.loads(msg['context']) if msg['context'] else None
                }
                for msg in reversed(messages)
            ]
    
    def save_user_profile(self, user_id: str, profile_data: Dict, preferences: Optional[Dict] = None):
        """
        Save or update user profile
        
        Args:
            user_id: User identifier
            profile_data: Profile information
            preferences: User preferences
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO user_profiles (user_id, profile_data, preferences)
                   VALUES (?, ?, ?)
                   ON CONFLICT(user_id) DO UPDATE SET
                   profile_data = excluded.profile_data,
                   preferences = excluded.preferences,
                   updated_at = CURRENT_TIMESTAMP''',
                (user_id, json.dumps(profile_data), json.dumps(preferences))
            )
            conn.commit()
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        Get user profile
        
        Args:
            user_id: User identifier
        
        Returns:
            User profile data or None
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    'user_id': row['user_id'],
                    'profile_data': json.loads(row['profile_data']),
                    'preferences': json.loads(row['preferences']) if row['preferences'] else {},
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
            return None
    
    def save_financial_goal(self, user_id: str, goal_type: str, target_amount: float,
                           deadline: Optional[datetime] = None) -> int:
        """
        Save a financial goal
        
        Args:
            user_id: User identifier
            goal_type: Type of goal (emergency_fund, retirement, purchase, etc.)
            target_amount: Target amount
            deadline: Optional deadline
        
        Returns:
            Goal ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO financial_goals (user_id, goal_type, target_amount, deadline) VALUES (?, ?, ?, ?)',
                (user_id, goal_type, target_amount, deadline.isoformat() if deadline else None)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_financial_goals(self, user_id: str) -> List[Dict]:
        """
        Get user's financial goals
        
        Args:
            user_id: User identifier
        
        Returns:
            List of financial goals
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM financial_goals WHERE user_id = ? ORDER BY deadline',
                (user_id,)
            )
            
            return [
                {
                    'id': row['id'],
                    'goal_type': row['goal_type'],
                    'target_amount': row['target_amount'],
                    'current_amount': row['current_amount'],
                    'deadline': row['deadline'],
                    'progress': (row['current_amount'] / row['target_amount'] * 100) if row['target_amount'] > 0 else 0
                }
                for row in cursor.fetchall()
            ]
    
    def update_goal_progress(self, goal_id: int, current_amount: float):
        """
        Update financial goal progress
        
        Args:
            goal_id: Goal identifier
            current_amount: Current amount saved
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE financial_goals SET current_amount = ? WHERE id = ?',
                (current_amount, goal_id)
            )
            conn.commit()
    
    def get_session_stats(self, session_id: str) -> Dict:
        """
        Get session statistics
        
        Args:
            session_id: Session identifier
        
        Returns:
            Session statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total messages
            cursor.execute('SELECT COUNT(*) FROM conversations WHERE session_id = ?', (session_id,))
            total_messages = cursor.fetchone()[0]
            
            # User messages
            cursor.execute('SELECT COUNT(*) FROM conversations WHERE session_id = ? AND role = "user"', (session_id,))
            user_messages = cursor.fetchone()[0]
            
            # Session duration
            cursor.execute(
                '''SELECT MIN(timestamp), MAX(timestamp)
                   FROM conversations
                   WHERE session_id = ?''',
                (session_id,)
            )
            time_range = cursor.fetchone()
            
            return {
                'total_messages': total_messages,
                'user_messages': user_messages,
                'assistant_messages': total_messages - user_messages,
                'started_at': time_range[0],
                'last_message_at': time_range[1]
            }
    
    def export_session(self, session_id: str) -> Dict:
        """
        Export complete session data
        
        Args:
            session_id: Session identifier
        
        Returns:
            Complete session data
        """
        return {
            'session_id': session_id,
            'conversation': self.get_conversation_history(session_id, limit=1000),
            'stats': self.get_session_stats(session_id),
            'exported_at': datetime.now().isoformat()
        }
    
    def cleanup_old_sessions(self, days: int = 30):
        """
        Clean up old sessions
        
        Args:
            days: Delete sessions older than this many days
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Delete old conversations
            cursor.execute(
                'DELETE FROM conversations WHERE session_id IN (SELECT session_id FROM sessions WHERE last_activity < ?)',
                (cutoff_date,)
            )
            
            # Delete old sessions
            cursor.execute('DELETE FROM sessions WHERE last_activity < ?', (cutoff_date,))
            
            conn.commit()
