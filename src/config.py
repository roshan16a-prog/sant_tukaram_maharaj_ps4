import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    APP_NAME = "PrepPro - AI Interview Coach"
    VERSION = "0.1.0"
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
    
    # Settings
    CAMERA_INDEX = 0  # Default camera index
    AUDIO_SAMPLE_RATE = 16000
    
    @staticmethod
    def ensure_data_dirs():
        """Ensure necessary data directories exist."""
        os.makedirs(Config.DATA_DIR, exist_ok=True)
