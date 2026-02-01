import streamlit as st
from src.config import Config

# Page Configuration
st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

import streamlit as st
import time
from src.config import Config
from src.ui.components import apply_theme, card, animated_header, status_indicator, app_header, profile_header
from src.utils.auth import Auth
from src.utils.database import db

# Page Configuration
st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

def show_login_page():
    st.markdown("<div style='text-align: center; margin-bottom: 2rem;'><h1>🎓 PrepPro Login</h1></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tabs = st.tabs(["Login", "Sign Up"])
        
        with tabs[0]:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Log In", use_container_width=True)
                
                if submit:
                    success, msg = Auth.login(email, password)
                    if success:
                        st.success(f"Welcome back, {msg['name']}!")
                        st.rerun()
                    else:
                        st.error(msg)
                        
        with tabs[1]:
            with st.form("signup_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit = st.form_submit_button("Create Account", use_container_width=True)
                
                if submit:
                    if password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        success, msg = Auth.signup(name, email, password)
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

def show_dashboard():
    user = st.session_state.user
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=64)
        st.markdown(f"### Hello, {user['name']}")
        
        st.header("Navigation")
        # Ensure default
        if "nav_selection" not in st.session_state:
            st.session_state.nav_selection = "Dashboard"
            
        page = st.radio("Go to:", [
            "Dashboard", 
            "Practice Interview", 
            "My Profile",
            "About"
        ], key="nav_selection")
        
        st.divider()
        if st.button("Log Out"):
            Auth.logout()
            
        st.caption(f"Version: {Config.VERSION}")

            
    if page == "Dashboard":
        animated_header("Dashboard")
        
        # Analytics
        stats = db.get_user_analytics(user['id'])
        
        st.markdown("### 📈 Performance Overview")
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.metric("Interviews", stats['total'])
        with c2:
            st.metric("Overall Score", f"{stats['overall']}/100")
        with c3:
            st.metric("Visual Confidence", f"{stats['vision']}%")
        with c4:
            st.metric("Speech Clarity", f"{stats['speech']}%")
            
        st.divider()
        
        # Recent History (Optional or keep existing table below? The Quick Actions takes space)
        # keeping Quick Actions logic below
            
        st.markdown("### Quick Actions")
        
        def go_to_practice():
            st.session_state.nav_selection = "Practice Interview"
            
        st.button("🚀 Start New Interview", type="primary", on_click=go_to_practice)

    elif page == "Practice Interview":
        # Initialize Session Manager in State
        if 'interview_manager' not in st.session_state:
            st.session_state.interview_manager = None
            
        # Ensure recording state is initialized
        if 'is_recording' not in st.session_state:
            st.session_state.is_recording = False
            
        manager = st.session_state.interview_manager
            
        animated_header("Practice Session")
        
        # Logic: Start New vs Continue
        if not manager or not manager.session:
            st.markdown("### ⚙️ Session Setup")
            
            col1, col2 = st.columns(2)
            with col1:
                domain = st.selectbox("Interview Domain", ["MIXED", "HR", "TECHNICAL", "PYTHON", "DATA_SCIENCE", "WEB_DEV"])
            with col2:
                q_count = st.slider("Number of Questions", 1, 20, 3)
                
            if st.button("🚀 Start Interview", type="primary"):
                # Dynamically import manager to avoid circular imports at top level if any
                from src.interview.manager import SessionManager
                st.session_state.interview_manager = SessionManager(user['id'])
                st.session_state.interview_manager.start_new_session(type=domain, count=q_count)
                st.rerun()
        else:
            # Interview In Progress
            q = manager.get_current_question()
            
            if q:
                # Progress Bar
                progress = (manager.current_index + 1) / len(manager.questions)
                st.progress(progress, text=f"Question {manager.current_index + 1} of {len(manager.questions)}")
                
                # Layout
                col_video, col_controls = st.columns([3, 1])
                
                with col_video:
                    st.markdown(f"### {q.text}")
                    st.caption(f"Category: {q.category} | Difficulty: {q.difficulty}")
                    
                    video_placeholder = st.empty()
                    
                    # If not recording, show static placeholder or last frame
                    if not st.session_state.is_recording:
                         video_placeholder.markdown("""
                            <div style="background-color: #000; height: 300px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white;">
                                📷 Click Start Recording to Activate Camera
                            </div>
                        """, unsafe_allow_html=True)

                with col_controls:
                    st.markdown("#### Controls")
                    
                    # Recording State Management
                    # (Initialized at top of page block)
                        
                    if not st.session_state.is_recording:
                        if st.button("🔴 Start Recording", type="primary"):
                            try:
                                manager.start_recording()
                                # Check if it actually started (flag check)
                                if manager.recorder.is_recording:
                                    st.session_state.is_recording = True
                                    st.rerun()
                                else:
                                    st.error("Audio recording unavailable (PyAudio missing). Cannot start session.")
                            except Exception as e:
                                st.error(f"Recording failed: {e}")
                    else:
                        st.info("🎙️ Recording in progress...")
                        if st.button("⏹️ Stop & Submit"):
                            with st.spinner("Processing Audio, Video & AI Analysis..."):
                                path, transcript, wpm, nlp_result = manager.stop_recording(q.id)
                                
                            st.session_state.is_recording = False
                            
                            # Success Message
                            st.success("Answer Submitted & Analyzed!")
                            
                            # Display AI Feedback
                            if nlp_result and nlp_result.get('rating', 0) > 0:
                                st.markdown("### 🤖 Coach's Assessment")
                                col_score, col_details = st.columns([1, 2])
                                import math
                                with col_score:
                                    rating = nlp_result['rating']
                                    stars = "⭐" * int(rating)
                                    card(f"{rating}/10", f"Overall Score\n{stars}", "neutral")
                                
                                with col_details:
                                    st.markdown(f"**Feedback:**\n{nlp_result['feedback']}")
                                    if nlp_result['suggestion']:
                                        st.info(f"💡 **Tip:** {nlp_result['suggestion']}")
                            
                            # Transcript & WPM info
                            with st.expander("Transcript & Speech Metrics"):
                                st.write(f"**Transcript:** {transcript}")
                                st.write(f"**Speaking Speed:** {wpm} WPM")
                            
                            # Capture ID before it might be cleared
                            current_session_id = manager.session['id']
                            
                            # Move to next
                            has_next = manager.next_question()
                            if not has_next:
                                st.success("Interview Completed! Generating Report...")
                                time.sleep(2)
                                st.session_state.show_report_session_id = current_session_id
                                # Clear manager to prevent recording access
                                st.session_state.interview_manager = None
                                st.rerun()
                            else:
                                if st.button("Next Question ➡️"):
                                    st.rerun()
                                time.sleep(4) # Auto advance if no click
                            
                            st.rerun()

                # REAL-TIME VIDEO LOOP (Outside Columns to avoid blocking UI if possible, or inside placeholder)
                # We put this loop at the end of the block so it runs continuously until interaction
                # REAL-TIME VIDEO LOOP
                if st.session_state.is_recording:
                    import cv2
                    
                    # Use a unique key for the capture to avoid re-opening if possible, 
                    # but Streamlit reruns re-execute this.
                    # We rely on OpenCV to handle device contention or we should have opened it in Manager?
                    # For MVP, opening here is standard Streamlit pattern for "live" loops.
                    
                    cap = cv2.VideoCapture(0) 
                    
                    if not cap.isOpened():
                         st.error("Camera not accessible. check permissions.")
                    else:
                        stop_button_pressed = False
                        
                        while st.session_state.is_recording:
                            ret, frame = cap.read()
                            if not ret:
                                st.warning("Camera frame dropped.")
                                break
                            
                            # Vision Analysis
                            try:
                                annotated_frame, metrics = manager.vision.process(frame)
                                # Convert to RGB
                                frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                                video_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
                            except Exception as e:
                                # Fail silently to avoid UI spam, or log one-time
                                pass
                                
                            # Essential for Streamlit loop to allow interruption
                            time.sleep(0.05) 
                        
                        cap.release()
            else:
                st.success("Session Completed Successfully!")
                if st.button("Return to Dashboard"):
                    st.session_state.interview_manager = None
                    st.rerun()

    elif page == "My Profile":
        profile_header(user['name'], user['email'])
        
        st.markdown("### Interview History")
        interviews = db.get_user_interviews(user['id'])
        
        if not interviews.empty:
            # Show a nice table or list
            # Select relevant columns for display
            display_df = interviews[['start_time', 'type', 'status']].copy()
            display_df.columns = ['Date', 'Domain', 'Status']
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No interviews recorded yet. Start one today!")
            
        st.divider()
        st.markdown("### Danger Zone")
        with st.expander("Delete Account"):
            st.warning("This action cannot be undone. All your data will be permanently lost.")
            if st.button("Confirm Deletion", type="primary"):
                if Auth.delete_account():
                    st.success("Account deleted successfully.")
                    st.rerun()
                else:
                    st.error("Failed to delete account.")

    elif page == "About":
        animated_header("About PrepPro")
        
        st.markdown("""
        ### 🚀 Accelerate Your Interview Prep
        **PrepPro** is your personal AI Interview Coach. We combine cutting-edge **Computer Vision**, **Speech Analysis**, and **Large Language Models** to give you 360-degree feedback on your performance.
        
        #### How it Works
        1.  **Start a Session**: Choose your domain (HR, Tech, etc.) and number of questions.
        2.  **Answer Live**: Application records your video and audio.
        3.  **Get Analyzed**:
            - 👁️ **Vision Engine**: Tracks eye contact and emotions.
            - 🗣️ **Speech Engine**: Measures speed (WPM) and filler words.
            - 🧠 **NLP Engine**: Evaluates the quality and correctness of your answer.
        4.  **Review Report**: Get a comprehensive scorecard with tips to improve.
        
        #### Privacy Policy
        Your video frames are processed in real-time and **never stored**. Audio is temporarily saved for transcription and then analyzed. All data is stored locally on your machine (for this MVP).
        """)

def show_feedback_report(session_id):
    st.markdown("## 📊 Interview Feedback Report")
    
    answers = db.get_session_answers(session_id)
    
    if not answers:
        st.warning("No data found for this session.")
        if st.button("Back to Dashboard"):
            st.session_state.nav_selection = "Dashboard"
            st.rerun()
        return

    # --- 1. Aggregation Logic ---
    total_vision = 0
    total_speech = 0
    total_content = 0
    count = len(answers)
    
    for a in answers:
        total_vision += a.get('vision_score', 0)
        total_speech += a.get('speech_clarity_score', 0)
        total_content += a.get('rating', 0) * 10 # Convert 1-10 to 0-100
        
    avg_vision = int(total_vision / count) if count else 0
    avg_speech = int(total_speech / count) if count else 0
    avg_content = int(total_content / count) if count else 0
    
    # Weighted Overall Score
    # Weight: Content 50%, Vision 30%, Speech 20%
    overall_score = int((avg_content * 0.5) + (avg_vision * 0.3) + (avg_speech * 0.2))
    
    # --- 2. Summary Section ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        card(f"{overall_score}/100", "Overall Score", "neutral")
    with col2:
        card(f"{avg_content}%", "Content Quality", "neutral")
    with col3:
        card(f"{avg_vision}%", "Visual Confidence", "neutral")
    with col4:
        card(f"{avg_speech}%", "Speech Clarity", "neutral")
        
    st.divider()
    
    # --- Tips Section ---
    st.subheader("💡 Improvement Tips")
    tips = []
    
    if avg_vision < 60:
        tips.append("👁️ **Eye Contact**: Try to look directly at the camera more often to show confidence.")
    if avg_speech < 60:
        tips.append("🗣️ **Clarity**: Your speech clarity score is lower than average. Try to enunciate your words clearly.")
    if avg_content < 60:
        tips.append("🧠 **Content**: Focus on structuring your answers. Use the STAR method (Situation, Task, Action, Result).")
    
    # Calculate average WPM
    avg_wpm = 0
    if count > 0:
        total_wpm = sum([a.get('wpm', 0) for a in answers])
        avg_wpm = total_wpm / count
        
    if avg_wpm > 160:
        tips.append("⚡ **Speed**: You are speaking quite fast (>160 WPM). Take a breath and slow down.")
    elif avg_wpm < 100:
        tips.append("🐢 **Speed**: You are speaking a bit slowly (<100 WPM). Try to keep a steady conversational pace.")
        
    if not tips:
        st.success("🎉 Excellent work! You performed well across all metrics.")
    else:
        for tip in tips:
            st.info(tip)

    st.divider()
    
    # --- 3. Detailed Breakdown ---
    st.subheader("📝 Question Breakdown")
    
    for i, ans in enumerate(answers):
        with st.expander(f"Q{i+1}: {ans['question_id']} (Score: {ans.get('rating', 0)}/10)"):
            c1, c2 = st.columns([2, 1])
            
            with c1:
                st.markdown(f"**Your Answer:**")
                st.caption(ans.get('transcription', 'No transcript available.'))
                
                if ans.get('feedback'):
                    st.markdown(f"**🤖 Coach's Feedback:**")
                    st.info(ans['feedback'])
                    
            with c2:
                st.markdown("**Metrics**")
                st.write(f"👁️ Focus: {ans.get('eye_contact_score', 0)}%")
                st.write(f"🗣️ Speed: {ans.get('wpm', 0)} WPM")
                st.write(f"😶 Fillers: {ans.get('filler_count', 0)}")
                
    st.divider()
    
    if st.button("⬅️ Return to Dashboard", type="primary"):
        st.session_state.nav_selection = "Dashboard"
        # Reset current session state ensure we don't loop back
        if 'interview_manager' in st.session_state:
            st.session_state.interview_manager = None
        st.rerun()

def main():
    apply_theme()
    app_header()
    
    # Global Error Handling
    try:
        if not Auth.require_auth():
            show_login_page()
        else:
            # Navigation Logic
            if 'nav_selection' not in st.session_state:
                st.session_state.nav_selection = "Dashboard"
                
            # Check for completed session report request
            # We can use a query param or state. Let's use state.
            if st.session_state.get('show_report_session_id'):
                show_feedback_report(st.session_state.show_report_session_id)
                # Clear the flag after showing the report
                del st.session_state.show_report_session_id
            else:
                show_dashboard()
                
    except Exception as e:
        st.error("An unexpected error occurred. Please refresh the page.")
        st.caption(f"Error details: {e}")
        # In production, log this error to a file/service
        if st.button("Reload App"):
            st.rerun()

if __name__ == "__main__":
    Config.ensure_data_dirs()
    main()
