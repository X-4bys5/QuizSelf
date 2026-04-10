# QuizSelf

Upload any PDF and get AI-generated quiz questions from it automatically. 
Works with both normal and scanned PDFs.

🔗 Live Demo: https://quizself-1.onrender.com

## What it does

You upload a PDF, it reads it and generates quiz questions from the actual 
content. Supports MCQ, True/False, and Theory questions. You can also pick 
the difficulty level — easy, medium, or hard.

The cool part is it handles scanned PDFs too. If normal text extraction 
fails it automatically falls back to Gemini's vision API to OCR the 
document, so both cases work in a single upload flow.

## Stack

* Python + Flask
* Groq API (Llama 3.3 70B) for question generation
* Google Gemini API for OCR on scanned/image-based PDFs
* PyMuPDF for direct PDF text extraction
* Plain HTML, CSS, JS frontend
* Deployed on Render

## Setup

You need two free API keys:
* Groq: https://console.groq.com
* Gemini: https://aistudio.google.com
git clone https://github.com/X-4bys5/QuizSelf.git
cd QuizSelf
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Create a `.env` file and add your keys:
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key

Then run it:
python app.py

## How it works

1. You upload a PDF
2. App tries to extract text directly using PyMuPDF
3. If that fails (scanned PDF), it falls back to Gemini OCR
4. Extracted text gets sent to Groq with a prompt to generate questions
5. Questions come back structured by type and difficulty
