import streamlit as st
import time
from src.utils.database import db
from src.interview.questions import QuestionBank
from src.speech.recorder import AudioRecorder
from src.vision.analyzer import VisionAnalyzer
from src.speech.analyzer import SpeechAnalyzer
from src.nlp.gemini_client import GeminiClient
import wave
import contextlib

class SessionManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = None
        self.questions = []
        self.current_index = 0
        self.recorder = AudioRecorder()
        self.vision = VisionAnalyzer()
        self.speech = SpeechAnalyzer()
        self.nlp = GeminiClient()
        
        # Load or create session
        self._load_active_session()

    def _load_active_session(self):
        # Check DB for in-progress session
        session_data = db.get_active_session(self.user_id)
        if session_data:
            self.session = session_data
            # ideally we should load the questions assigned to this session
            # For this MVP, we might re-randomize or store question IDs in DB.
            # to keep it deterministic on refresh, we'd store the specific Q-IDs.
            # For now, let's keep it simple: if refreshed, we might get new questions 
            # unless we store list in session_state or DB.
            # Let's rely on st.session_state for specific questions during the run.
        else:
            self.session = None

    def start_new_session(self, type="MIXED", count=3):
        session_id = db.create_session(self.user_id, type)
        self.session = {'id': session_id, 'status': 'IN_PROGRESS', 'type': type}
        self.questions = QuestionBank.get_random_questions(count, type)
        self.current_index = 0
        return self.session

    def get_current_question(self):
        if 0 <= self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def next_question(self):
        self.current_index += 1
        if self.current_index >= len(self.questions):
            self.complete_session()
            return False # Session ended
        return True

    def complete_session(self):
        if self.session:
            db.complete_session(self.session['id'])
            self.session = None
    
    def start_recording(self):
        self.recorder.start_recording()
        self.vision.reset()
        
    def stop_recording(self, question_id):
        # Save filename: session_{id}_q_{qid}.wav
        filename = f"session_{self.session['id']}_{question_id}.wav"
        path = self.recorder.stop_recording(filename)
        
        # Get Vision Metrics
        v_score, focus_score, emotion = self.vision.get_summary_metrics()
        
        # Get Speech Metrics
        transcription = ""
        wpm = 0
        filler_count = 0
        clarity = 0
        duration = 0
        nlp_result = {}
        
        if path:
            # Get duration
            try:
                with contextlib.closing(wave.open(path, 'r')) as f:
                    frames = f.getnframes()
                    rate = f.getframerate()
                    duration = frames / float(rate)
            except Exception:
                duration = 0
            
            # Speech Analysis
            transcription = self.speech.transcribe(path)
            speech_metrics = self.speech.analyze(transcription, duration)
            wpm = speech_metrics["wpm"]
            filler_count = speech_metrics["filler_count"]
            clarity = speech_metrics["speech_clarity_score"]

            # NLP Analysis (Gemini)
            question_text = "Unknown Question"
            category = "General"
            # Find question object
            current_q = next((q for q in self.questions if q.id == question_id), None)
            if current_q:
                question_text = current_q.text
                category = current_q.category
                
            nlp_result = self.nlp.evaluate_answer(question_text, transcription, category)
            
            # Save to DB
            db.save_answer(self.session['id'], question_id, path, duration, 
                           vision_score=v_score, 
                           eye_contact_score=focus_score, 
                           dominant_emotion=emotion,
                           transcription=transcription,
                           wpm=wpm,
                           filler_count=filler_count,
                           speech_clarity_score=clarity,
                           feedback=nlp_result['feedback'],
                           rating=nlp_result['rating'],
                           relevance_score=nlp_result['relevance_score'],
                           technical_score=nlp_result['technical_score'],
                           struct_clarity_score=nlp_result['struct_clarity_score'])
                           
        return path, transcription, wpm, nlp_result
