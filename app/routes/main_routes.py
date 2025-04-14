from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
from app import app
from app.utils.pdf_handler import extract_text_from_pdf
from app.utils.quiz_generator import QuizGenerator
from app.utils.flashcard_generator import FlashcardGenerator
from database.neo4j_connection import Neo4jConnection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith('.pdf'):
        try:
            # Ensure upload directory exists
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print(f"File saved to: {filepath}")
            
            # Extract text from PDF
            text_chunks = extract_text_from_pdf(filepath)
            if not text_chunks:
                os.remove(filepath)
                return jsonify({'error': 'No text extracted from PDF'}), 400
            
            print(f"Extracted {len(text_chunks)} chunks")
            
            # Initialize database connection
            db = Neo4jConnection()
            if not db.connect():
                os.remove(filepath)
                return jsonify({'error': 'Database connection failed'}), 500
            
            try:
                # Clear existing concepts first
                db.query("MATCH (n:Concept) DETACH DELETE n")
                
                concepts = []
                # Create nodes first
                for i, chunk in enumerate(text_chunks, 1):
                    title = chunk['title']
                    content = chunk['content']
                    
                    # Clean up the title and content
                    title = title.replace('\n', ' ').strip()
                    content = content.strip()
                    
                    # Ensure we have valid content
                    if not title or not content:
                        continue
                        
                    # Make title more readable
                    if len(title) > 30:
                        title = title[:27] + '...'
                    
                    print(f"Processing chunk {i}: {title}")  # Debug print
                    
                    node = db.create_concept_node(title, content)
                    if node:
                        concepts.append({
                            'name': title,
                            'content': content,
                            'related': []
                        })
                        print(f"Node created: {title}")
                    else:
                        print(f"Failed to create node: {title}")  # Debug print
                
                # Create relationships
                for i in range(len(concepts)):
                    if i > 0:
                        source = concepts[i]['name']
                        target = concepts[i-1]['name']
                        rel = db.create_relationship(source, target, "RELATED_TO")
                        if rel:
                            concepts[i]['related'].append(target)
                            concepts[i-1]['related'].append(source)
                            print(f"Relationship created: {source} -> {target}")
                
                return jsonify({
                    'message': 'PDF processed successfully',
                    'concepts': concepts
                })
            
            finally:
                db.close()
                os.remove(filepath)
                
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            # Clean up file if it exists
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
            
    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/generate_quiz/<concept_name>')
def generate_quiz(concept_name):
    db = Neo4jConnection()
    if db.connect():
        try:
            concept = db.get_concept(concept_name)
            if concept:
                quiz_gen = QuizGenerator()
                quiz = quiz_gen.generate_quiz(concept)
                return jsonify(quiz)
            return jsonify({'error': 'Concept not found'}), 404
        finally:
            db.close()
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/generate_flashcard/<concept_name>')
def generate_flashcard(concept_name):
    db = Neo4jConnection()
    if db.connect():
        try:
            concept = db.get_concept(concept_name)
            if concept:
                flashcard_gen = FlashcardGenerator()
                flashcard = flashcard_gen.generate_flashcard(concept)
                return jsonify(flashcard)
            return jsonify({'error': 'Concept not found'}), 404
        finally:
            db.close()
    return jsonify({'error': 'Database connection failed'}), 500