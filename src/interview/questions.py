from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Question:
    id: str
    text: str
    category: str # 'HR' or 'TECHNICAL'
    difficulty: str = 'Medium'

class QuestionBank:
    _questions = [
        # HR Questions
        Question("HR_01", "Tell me about yourself.", "HR", "Easy"), # Intro
        Question("HR_02", "What is your greatest strength and weakness?", "HR", "Medium"),
        Question("HR_03", "Describe a challenging situation you handled at work.", "HR", "Hard"),
        Question("HR_04", "Where do you see yourself in 5 years?", "HR", "Medium"),
        
        # Technical Questions (General/Software)
        Question("TECH_01", "Explain the concept of OOP to a 5-year-old.", "TECHNICAL", "Easy"),
        Question("TECH_02", "What is the difference between a process and a thread?", "TECHNICAL", "Medium"),
        Question("TECH_03", "How does HTTP work?", "TECHNICAL", "Medium"),
        Question("TECH_04", "Explain Big O notation with an example.", "TECHNICAL", "Hard"),
        
        # Python
        Question("PY_01", "What are Python decorators?", "PYTHON", "Medium"),
        Question("PY_02", "Explain the Global Interpreter Lock (GIL).", "PYTHON", "Hard"),
        Question("PY_03", "Difference between list and tuple?", "PYTHON", "Easy"),
        Question("PY_04", "How is memory managed in Python?", "PYTHON", "Hard"),
        
        # Data Science
        Question("DS_01", "What is a p-value?", "DATA_SCIENCE", "Medium"),
        Question("DS_02", "Explain bias-variance tradeoff.", "DATA_SCIENCE", "Hard"),
        Question("DS_03", "How do you handle missing data?", "DATA_SCIENCE", "Medium"),
        Question("DS_04", "What is overfitting?", "DATA_SCIENCE", "Easy"),
        
        # Web Development
        Question("WEB_01", "Explain the box model in CSS.", "WEB_DEV", "Easy"),
        Question("WEB_02", "What is the DOM?", "WEB_DEV", "Easy"),
        Question("WEB_03", "Difference between GET and POST requests.", "WEB_DEV", "Medium"),
        Question("WEB_04", "Explain the React Component Lifecycle.", "WEB_DEV", "Hard"),
    ]

    @staticmethod
    def get_random_questions(count=3, category="MIXED") -> List[Question]:
        import random
        pool = QuestionBank._questions
        
        if category != "MIXED":
            pool = [q for q in pool if q.category == category]
            
        # Select random questions
        selected = random.sample(pool, min(count, len(pool)))
        
        # Sort by difficulty for realistic flow
        # Easy -> Medium -> Hard
        difficulty_order = {"Easy": 0, "Medium": 1, "Hard": 2}
        selected.sort(key=lambda x: difficulty_order.get(x.difficulty, 1))
        
        return selected

    @staticmethod
    def get_question_by_id(q_id) -> Optional[Question]:
        for q in QuestionBank._questions:
            if q.id == q_id:
                return q
        return None
