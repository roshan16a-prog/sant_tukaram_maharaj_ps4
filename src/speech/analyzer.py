import speech_recognition as sr
import os

class SpeechAnalyzer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_path):
        """
        Transcribe audio file to text using Google Speech Recognition.
        """
        if not os.path.exists(audio_path):
            return ""
            
        try:
            with sr.AudioFile(audio_path) as source:
                audio_data = self.recognizer.record(source)
                try:
                    text = self.recognizer.recognize_google(audio_data)
                    return text
                except sr.UnknownValueError:
                    return "" # Unintelligible speech
                except sr.RequestError:
                    return "" # API unreachable
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""

    def analyze(self, text, duration_seconds):
        """
        Calculate metrics: WPM, Filler Count, Clarity Score.
        """
        metrics = {
            "wpm": 0,
            "filler_count": 0,
            "speech_clarity_score": 0
        }
        
        if not text or duration_seconds <= 0:
            return metrics
            
        # Word Count & WPM
        words = text.split()
        word_count = len(words)
        metrics["wpm"] = int(word_count / (duration_seconds / 60))
        
        # Filler Detection
        fillers = ["um", "uh", "like", "so", "actually", "basically", "literally"]
        filler_count = sum(1 for w in words if w.lower().strip(",.") in fillers)
        metrics["filler_count"] = filler_count
        
        # Clarity Score (Simple Heuristic)
        # Base 100, penalize fillers heavily
        # Penalty: 5 pts per filler
        clarity = max(0, 100 - (filler_count * 5))
        metrics["speech_clarity_score"] = clarity
        
        return metrics
