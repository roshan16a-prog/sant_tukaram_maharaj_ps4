import cv2
import cv2
import numpy as np
import os

class VisionAnalyzer:
    def __init__(self):
        # Load Haar Cascades
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.smile_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_smile.xml'
        )
        
        # Stats tracking
        self.total_frames = 0
        self.focused_frames = 0
        self.smiling_frames = 0
        self.dominant_emotion = "Neutral"

    def process(self, frame):
        """
        Process a single frame using OpenCV Haar Cascades.
        """
        self.total_frames += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        metrics = {
            "has_face": False,
            "is_focused": False,
            "is_smiling": False,
            "emotion": "Neutral"
        }
        
        # Detect Faces
        # scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        
        if len(faces) > 0:
            metrics["has_face"] = True
            
            # Assume the largest face is the user
            # (x, y, w, h)
            largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
            x, y, w, h = largest_face
            
            # Focus Check: Is face reasonably centered?
            frame_center_x = frame.shape[1] // 2
            face_center_x = x + w // 2
            
            # Allow 15% deviation from center
            margin = frame.shape[1] * 0.15
            if abs(frame_center_x - face_center_x) < margin:
                metrics["is_focused"] = True
                self.focused_frames += 1
                
            # Draw Face Box
            color = (0, 255, 0) if metrics["is_focused"] else (0, 255, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Smile Detection (within face ROI)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            # Smile detection is sensitive. adjust parameters.
            # scaleFactor=1.7, minNeighbors=20 works better for smiles typically
            smiles = self.smile_cascade.detectMultiScale(roi_gray, 1.7, 20)
            
            if len(smiles) > 0:
                metrics["is_smiling"] = True
                metrics["emotion"] = "Happy"
                self.smiling_frames += 1
                
                for (sx, sy, sw, sh) in smiles:
                    cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 1)
            
            # Overlay Status
            status_text = f"Emotion: {metrics['emotion']} | Focus: {'Yes' if metrics['is_focused'] else 'No'}"
            cv2.putText(frame, status_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
        else:
            cv2.putText(frame, "No Face Detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
        return frame, metrics

    def get_summary_metrics(self):
        """Calculate final scores for the session/question."""
        if self.total_frames == 0:
            return 0, 0, "Neutral"
            
        focus_score = int((self.focused_frames / self.total_frames) * 100)
        smile_percent = (self.smiling_frames / self.total_frames) * 100
        
        dom_emotion = "Neutral"
        if smile_percent > 20: # Lower threshold for cascade
            dom_emotion = "Confident"
        elif focus_score < 50:
            dom_emotion = "Nervous"
            
        # Composite vision score
        vision_score = int((focus_score + (100 if dom_emotion == "Confident" else 50)) / 2)
        
        return vision_score, focus_score, dom_emotion

    def reset(self):
        self.total_frames = 0
        self.focused_frames = 0
        self.smiling_frames = 0
