import pdfplumber
import nltk
import os
import time
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Set NLTK data path to user's home directory
nltk_data_dir = os.path.expanduser('~/nltk_data')
os.makedirs(nltk_data_dir, exist_ok=True)

# Force download NLTK data with retry mechanism
def download_nltk_data_with_retry(package, max_retries=3):
    for attempt in range(max_retries):
        try:
            nltk.download(package, quiet=True, download_dir=nltk_data_dir)
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed to download {package} after {max_retries} attempts")
                return False
            time.sleep(1)  # Wait before retrying

# Initialize NLTK data
required_packages = ['punkt', 'stopwords', 'wordnet', 'omw-1.4']
for package in required_packages:
    download_nltk_data_with_retry(package)

def process_pdf(file):
    try:
        # Configure pdfplumber to handle missing CropBox
        with pdfplumber.open(file, strict=False) as pdf:
            text = ""
            for page in pdf.pages:
                try:
                    extracted = page.extract_text(x_tolerance=2, y_tolerance=2)
                    if extracted:
                        text += " " + extracted.strip()
                except Exception as e:
                    print(f"Warning: Error extracting text from page: {str(e)}")
                    continue

        if not text:
            return []

        # Process text with error handling
        try:
            sentences = sent_tokenize(text)
            stop_words = set(stopwords.words('english'))
            lemmatizer = WordNetLemmatizer()

            concepts = []
            for sentence in sentences:
                if not sentence.strip():
                    continue
                    
                words = word_tokenize(sentence)
                words = [lemmatizer.lemmatize(word.lower()) for word in words 
                        if word.isalnum() and word.lower() not in stop_words]
                
                if words:
                    concepts.append({
                        'name': ' '.join(words[:3]),
                        'content': sentence
                    })

            return concepts[:10] if concepts else []

        except LookupError:
            nltk.download('punkt', quiet=True, download_dir=nltk_data_dir)
            nltk.download('stopwords', quiet=True, download_dir=nltk_data_dir)
            nltk.download('wordnet', quiet=True, download_dir=nltk_data_dir)
            # Try processing again after downloading
            return process_pdf(file)

    except Exception as e:
        print(f"PDF Processing Error: {str(e)}")
        raise Exception("Error processing PDF. Please ensure it's a valid PDF file.")