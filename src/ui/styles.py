import streamlit as st

def get_css():
    return """
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

        :root {
            --bg-color: #0E1117;
            --card-bg: #1A1C24;
            --primary-gradient: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
            --secondary-gradient: linear-gradient(135deg, #2AF598 0%, #009EFD 100%);
            --accent-color: #FF0080;
            --text-primary: #FFFFFF;
            --text-secondary: #B0B3B8;
            --border-color: rgba(255, 255, 255, 0.1);
        }

        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
            color: var(--text-primary);
        }

        .stApp {
            background-color: var(--bg-color);
        }

        /* Titles & Headers */
        h1, h2, h3 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            color: white !important;
            letter-spacing: -0.5px;
        }

        /* Modern Glassmorphism Cards */
        .custom-card {
            background: rgba(26, 28, 36, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .custom-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            border-color: rgba(118, 75, 162, 0.5);
        }

        /* Buttons Update */
        div.stButton > button {
            background: var(--primary-gradient);
            color: white;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.9rem;
            box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4);
        }

        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(118, 75, 162, 0.6);
        }
        
        div.stButton > button:active {
            transform: scale(0.98);
        }
        
        /* Secondary/Outline Button styling override if needed */
        button[kind="secondary"] {
             background: transparent !important;
             border: 1px solid rgba(255,255,255,0.2) !important;
        }

        /* Input Fields */
        div[data-baseweb="input"] > div {
            background-color: #262730;
            border-color: rgba(255,255,255,0.1);
            color: white;
            border-radius: 8px;
        }
        
        div[data-baseweb="select"] > div {
             background-color: #262730;
             color: white;
             border-radius: 8px;
        }

        /* Status Indicators */
        .status-badge {
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        
        .status-active {
            background: rgba(42, 245, 152, 0.15);
            color: #2AF598;
            border: 1px solid rgba(42, 245, 152, 0.3);
        }
        
        .status-inactive {
            background: rgba(255, 0, 128, 0.15);
            color: #FF0080;
            border: 1px solid rgba(255, 0, 128, 0.3);
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .animate-fade-in {
            animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0E1117; 
        }
        ::-webkit-scrollbar-thumb {
            background: #262730; 
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #555; 
        }
    </style>
    """
