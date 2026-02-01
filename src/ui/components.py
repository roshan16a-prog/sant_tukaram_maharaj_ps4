import streamlit as st
from src.ui.styles import get_css

def apply_theme():
    """Injects custom CSS into the Streamlit app."""
    st.markdown(get_css(), unsafe_allow_html=True)

def card(title, content, context="neutral"):
    """
    Renders a styled card with optional context styling.
    """
    st.markdown(f"""
        <div class="custom-card animate-fade-in">
            <h3 style="margin-top: 0; font-size: 1.2rem;">{title}</h3>
            <p>{content}</p>
        </div>
    """, unsafe_allow_html=True)

def status_indicator(label, is_active):
    """
    Displays a status badge using custom CSS classes.
    """
    status_class = "status-active" if is_active else "status-inactive"
    status_text = "ACTIVE" if is_active else "INACTIVE"
    icon = "🟢" if is_active else "🟠"
    
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <span style="font-weight: 600;">{label}</span>
            <span class="status-badge {status_class}">
                {icon} {status_text}
            </span>
        </div>
    """, unsafe_allow_html=True)

def animated_header(text):
    """
    Displays a header with a fade-in animation.
    """
    st.markdown(f"""
        <div class="animate-fade-in">
            <h1>{text}</h1>
        </div>
    """, unsafe_allow_html=True)

def profile_header(name, email):
    """
    Displays a user profile header.
    """
    st.markdown(f"""
        <div class="custom-card animate-fade-in" style="display: flex; align-items: center; gap: 20px; border-left: 4px solid #667EEA;">
            <div style="background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%); color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: bold; box-shadow: 0 4px 10px rgba(102, 126, 234, 0.4);">
                {name[0].upper()}
            </div>
            <div>
                <h2 style="margin: 0; color: white;">{name}</h2>
                <p style="margin: 0; color: #B0B3B8;">{email}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def app_header():
    """
    Displays the main application header with logo/branding.
    """
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 30px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                 <div style="font-size: 28px;">🎓</div>
                 <div>
                    <h2 style="margin: 0; color: white; font-size: 1.5rem; background: linear-gradient(135deg, #667EEA 0%, #e0e0e0 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">InterviewIQ</h2>
                 </div>
            </div>
            <div style="color: #B0B3B8; font-size: 0.9rem; font-weight: 500;">
                AI Interview Coach
            </div>
        </div>
    """, unsafe_allow_html=True)
