import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not found.")

    def evaluate_answer(self, question, answer_text, category):
        """
        Evaluates the answer using Gemini. 
        Returns a dict with scores and feedback.
        """
        # Fallback if no API key or empty answer
        default_response = {
            "relevance_score": 0,
            "technical_score": 0,
            "struct_clarity_score": 0,
            "rating": 0,
            "feedback": "Evaluation unavailable (No API Key or Empty Answer).",
            "suggestion": "N/A"
        }

        if not self.model:
            return default_response
            
        if not answer_text or len(answer_text.strip()) < 5:
            default_response["feedback"] = "Answer too short for evaluation."
            return default_response

        # Prompt Engineering
        prompt = f"""
        You are an expert Interview Coach. Evaluate the following answer.
        
        Question ({category}): "{question}"
        Candidate Answer: "{answer_text}"
        
        Provide a JSON response with the following keys:
        - relevance_score (0-100): Alignment with question.
        - technical_score (0-100): Accuracy/Logic.
        - struct_clarity_score (0-100): Organization/Flow.
        - rating (1-10): Overall quality.
        - feedback: concise bullet points (max 3) on what was good/bad.
        - suggestion: 1-sentence improved version or tip.
        
        Return ONLY valid JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # clean response text (remove backticks if any)
            text = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(text)
            
            # Ensure safe fallback for missing keys
            return {
                "relevance_score": data.get("relevance_score", 0),
                "technical_score": data.get("technical_score", 0),
                "struct_clarity_score": data.get("struct_clarity_score", 0),
                "rating": data.get("rating", 0),
                "feedback": str(data.get("feedback", "No feedback.")),
                "suggestion": str(data.get("suggestion", ""))
            }
            
        except Exception as e:
            print(f"Gemini Error: {e}")
            default_response["feedback"] = f"AI Evaluation Failed: {str(e)}"
            return default_response
