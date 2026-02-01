import sqlite3
import os
from src.config import Config

db_path = os.path.join(Config.DATA_DIR, "preppro.db")

def migrate():
    print(f"Migrating database at {db_path}...")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    columns_to_add = [
        ("vision_score", "INTEGER DEFAULT 0"),
        ("eye_contact_score", "INTEGER DEFAULT 0"),
        ("dominant_emotion", "TEXT DEFAULT 'Neutral'"),
        ("transcription", "TEXT DEFAULT ''"),
        ("wpm", "INTEGER DEFAULT 0"),
        ("filler_count", "INTEGER DEFAULT 0"),
        ("speech_clarity_score", "INTEGER DEFAULT 0"),
        ("feedback", "TEXT DEFAULT ''"),
        ("rating", "INTEGER DEFAULT 0"),
        ("relevance_score", "INTEGER DEFAULT 0"),
        ("technical_score", "INTEGER DEFAULT 0"),
        ("struct_clarity_score", "INTEGER DEFAULT 0")
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            c.execute(f"ALTER TABLE interview_answers ADD COLUMN {col_name} {col_type}")
            print(f"Added column: {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column" in str(e).lower():
                print(f"Column {col_name} already exists.")
            else:
                print(f"Error adding {col_name}: {e}")
                
    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
