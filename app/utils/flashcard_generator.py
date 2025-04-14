import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import random

class FlashcardGenerator:
    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
        
    def generate_flashcard(self, concept):
        try:
            content = concept['content']
            sentences = sent_tokenize(content)
            
            # Get key sentences for the answer
            if len(sentences) > 2:
                answer = ' '.join(sentences[:2])  # First two sentences
            else:
                answer = content[:200]
            
            return {
                'question': f"What are the key concepts in: {concept['name']}?",
                'answer': answer
            }
            
        except Exception as e:
            print(f"Error generating flashcard: {str(e)}")
            return None