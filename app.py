from flask import Flask, render_template, request
from chatbot import ask_question
from main import extract_text_from_pdf
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Store extracted text in memory
pdf_text = ""

@app.route("/", methods=["GET", "POST"])
def index():
    global pdf_text
    answer = None

    if request.method == "POST":
        if 'pdf' in request.files:
            pdf_file = request.files['pdf']
            if pdf_file.filename != "":
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
                pdf_file.save(filepath)
                pdf_text = extract_text_from_pdf(filepath)
        elif 'question' in request.form:
            question = request.form['question']
            if pdf_text:
                answer = ask_question(question, pdf_text)
            else:
                answer = "Please upload a PDF first."

    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
