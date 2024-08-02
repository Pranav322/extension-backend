from flask import Flask, request, send_file
from flask_cors import CORS
from pdf2docx import Converter
import os

app = Flask(__name__)
CORS(app)

def pdf_to_word(pdf_file, word_file):
    cv = Converter(pdf_file)
    cv.convert(word_file, start=0, end=None)
    cv.close()

@app.route('/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    # Save the uploaded PDF file
    pdf_path = os.path.join('uploads', file.filename)
    file.save(pdf_path)

    # Define the output Word file path
    word_path = pdf_path.replace('.pdf', '.docx')

    # Convert the PDF to Word
    pdf_to_word(pdf_path, word_path)

    # Send the Word file back to the client and delete the files afterwards
    response = send_file(word_path, as_attachment=True)
    response.call_on_close(lambda: clean_up_files(pdf_path, word_path))
    
    return response

def clean_up_files(pdf_path, word_path):
    try:
        os.remove(pdf_path)
        os.remove(word_path)
    except Exception as e:
        print(f"Error deleting files: {e}")

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(host='0.0.0.0', port=5000)
