import sqlite3
import os
import datetime
import pandas as pd
from src.config import Config

class DatabaseManager:
    def __init__(self):
        self.db_path = os.path.join(Config.DATA_DIR, "preppro.db")
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def init_db(self):
        """Initialize the database tables if they don't exist."""
        conn = self.get_connection()
        c = conn.cursor()
        
        # Users Table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Interview Sessions Table
        c.execute('''
            CREATE TABLE IF NOT EXISTS interview_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'IN_PROGRESS', -- IN_PROGRESS, COMPLETED
                type TEXT DEFAULT 'MIXED', -- HR, TECHNICAL, MIXED
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Interview Answers Table
        c.execute('''
            CREATE TABLE IF NOT EXISTS interview_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                question_id TEXT NOT NULL,
                audio_path TEXT,
                video_path TEXT,
                duration_seconds INTEGER,
                vision_score INTEGER DEFAULT 0,
                eye_contact_score INTEGER DEFAULT 0,
                dominant_emotion TEXT DEFAULT 'Neutral',
                transcription TEXT DEFAULT '',
                wpm INTEGER DEFAULT 0,
                filler_count INTEGER DEFAULT 0,
                speech_clarity_score INTEGER DEFAULT 0,
                feedback TEXT DEFAULT '',
                rating INTEGER DEFAULT 0,
                relevance_score INTEGER DEFAULT 0,
                technical_score INTEGER DEFAULT 0,
                struct_clarity_score INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES interview_sessions (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def create_user(self, email, name, password_hash):
        """Create a new user. Returns user_id if successful, None if email exists."""
        try:
            conn = self.get_connection()
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
                (email, name, password_hash)
            )
            user_id = c.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            return None

    def get_user_by_email(self, email):
        """Retrieve user data by email."""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()
        return dict(user) if user else None

    def get_user_interviews(self, user_id):
        """Get interview history for a user."""
        conn = self.get_connection()
        # Adjusted to query interview_sessions instead of old interviews table if needed, 
        # but for now let's keep it compatible or specific to new schema.
        # The old interviews table was removed/replaced by interview_sessions logic effectively.
        # Let's query interview_sessions for history.
        query = "SELECT * FROM interview_sessions WHERE user_id = ? ORDER BY start_time DESC"
        df = pd.read_sql_query(query, conn, params=(user_id,))
        conn.close()
        return df

    def create_session(self, user_id, type="MIXED"):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO interview_sessions (user_id, type) VALUES (?, ?)", (user_id, type))
        session_id = c.lastrowid
        conn.commit()
        conn.close()
        return session_id

    def get_active_session(self, user_id):
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM interview_sessions WHERE user_id = ? AND status = 'IN_PROGRESS' ORDER BY id DESC LIMIT 1", (user_id,))
        session = c.fetchone()
        conn.close()
        return dict(session) if session else None

    def save_answer(self, session_id, question_id, audio_path, duration, 
                   vision_score=0, eye_contact_score=0, dominant_emotion="Neutral",
                   transcription="", wpm=0, filler_count=0, speech_clarity_score=0,
                   feedback="", rating=0, relevance_score=0, technical_score=0, struct_clarity_score=0):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("""
            INSERT INTO interview_answers 
            (session_id, question_id, audio_path, duration_seconds, 
             vision_score, eye_contact_score, dominant_emotion,
             transcription, wpm, filler_count, speech_clarity_score,
             feedback, rating, relevance_score, technical_score, struct_clarity_score) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (session_id, question_id, audio_path, duration, 
             vision_score, eye_contact_score, dominant_emotion,
             transcription, wpm, filler_count, speech_clarity_score,
             feedback, rating, relevance_score, technical_score, struct_clarity_score))
        conn.commit()
        conn.close()

    def complete_session(self, session_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("UPDATE interview_sessions SET status = 'COMPLETED' WHERE id = ?", (session_id,))
        conn.commit()
        conn.close()

    def get_session_answers(self, session_id):
        """Retrieve all answers and metrics for a specific session."""
        conn = self.get_connection()
        # Use pandas for easier aggregation later, or just return dicts
        # Given dependencies, let's use row_factory for pure dicts
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM interview_answers WHERE session_id = ? ORDER BY id ASC", (session_id,))
        rows = c.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def delete_user(self, user_id):
        """Delete a user and all their associated data."""
        conn = self.get_connection()
        c = conn.cursor()
        try:
            # Get all session IDs for this user
            c.execute("SELECT id FROM interview_sessions WHERE user_id = ?", (user_id,))
            sessions = c.fetchall()
            session_ids = [s[0] for s in sessions]
            
            if session_ids:
                # Delete answers for these sessions
                # SQLite doesn't support array parameters easily, so we loop or use string fmt (carefully)
                # Loop is safer/easier for small scale MVP
                for sid in session_ids:
                    c.execute("DELETE FROM interview_answers WHERE session_id = ?", (sid,))
            
            # Delete sessions
            c.execute("DELETE FROM interview_sessions WHERE user_id = ?", (user_id,))
            
            # Delete user
            c.execute("DELETE FROM users WHERE id = ?", (user_id,))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    def get_user_analytics(self, user_id):
        """Calculate aggregate metrics for a user across all sessions."""
        conn = self.get_connection()
        c = conn.cursor()
        
        # Get total completed interviews
        c.execute("SELECT COUNT(*) FROM interview_sessions WHERE user_id = ? AND status = 'COMPLETED'", (user_id,))
        total_interviews = c.fetchone()[0]
        
        if total_interviews == 0:
            conn.close()
            return {'total': 0, 'content': 0, 'vision': 0, 'speech': 0, 'overall': 0}
            
        # Get averages
        # Note: rating is 1-10, others are 0-100 usually (or need normalization)
        # Vision/Speech scores in save_answer seem to be 0-100 based on usage.
        # Rating is 1-10.
        query = """
            SELECT 
                AVG(a.rating) as avg_content,
                AVG(a.vision_score) as avg_vision,
                AVG(a.speech_clarity_score) as avg_speech
            FROM interview_answers a
            JOIN interview_sessions s ON a.session_id = s.id
            WHERE s.user_id = ?
        """
        c.execute(query, (user_id,))
        result = c.fetchone()
        conn.close()
        
        avg_content = result[0] if result[0] else 0
        avg_vision = result[1] if result[1] else 0
        avg_speech = result[2] if result[2] else 0
        
        # Normalize content to 0-100
        avg_content_norm = avg_content * 10
        
        # Calculate Weighted Overall
        # 50% Content, 30% Vision, 20% Speech
        overall = (avg_content_norm * 0.5) + (avg_vision * 0.3) + (avg_speech * 0.2)
        
        return {
            'total': total_interviews,
            'content': int(avg_content_norm),
            'vision': int(avg_vision),
            'speech': int(avg_speech),
            'overall': int(overall)
        }

db = DatabaseManager()
