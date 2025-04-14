from transformers import pipeline
import random

class QuizGenerator:
    def __init__(self):
        self.qa_pipeline = pipeline("question-generation")
        
    def generate_quiz(self, concept):
        try:
            # Generate questions from content
            questions = self.qa_pipeline(concept['content'])
            
            if not questions:
                # Fallback question generation
                return {
                    'question': f"What is the main idea of {concept['name']}?",
                    'options': [
                        concept['content'][:100] + "...",
                        "Not enough information",
                        "Cannot be determined",
                        "None of the above"
                    ],
                    'correct': 'A'
                }
            
            # Take the first generated question
            question = questions[0]
            
            return {
                'question': question['question'],
                'options': [
                    question['answer'],
                    "Not mentioned in the text",
                    "Cannot be determined from the content",
                    "None of the above"
                ],
                'correct': 'A'
            }
            
        except Exception as e:
            print(f"Error generating quiz: {str(e)}")
            return None