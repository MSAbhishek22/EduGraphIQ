from flask import render_template, request, jsonify, send_from_directory
from app import app
import fitz  # PyMuPDF
import nltk
import os

# Set up NLTK data path and download required data
nltk_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nltk_data')
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', download_dir=nltk_data_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
            
        file = request.files['pdf']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Invalid file type. Please upload a PDF'}), 400

        # Process PDF
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        
        # Basic text processing without NLTK tokenization
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 0]
        concepts = []
        
        for sentence in sentences:
            words = sentence.split()
            if len(words) > 5:
                concepts.append({
                    'name': ' '.join(words[:3]),
                    'content': sentence
                })
                if len(concepts) >= 10:
                    break
        
        return jsonify({
            'status': 'success',
            'concepts': concepts
        })
        
    except Exception as e:
        print(f"Error processing upload: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)