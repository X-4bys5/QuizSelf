# QuizCraft

Upload a PDF and get AI-generated quiz questions from it. Supports normal and scanned PDFs. Built with Python and Flask.

## How it works

- Normal PDFs get text extracted directly
- Scanned PDFs get sent to Gemini for OCR
- Extracted text gets sent to Groq (Llama 3.3) to generate questions
- Supports MCQ, True/False, and Theory questions with difficulty settings

## Stack

- Python + Flask
- Groq API (Llama 3.3 70B) for question generation
- Gemini API for OCR on scanned PDFs
- PyMuPDF for PDF text extraction
- Plain HTML, CSS, JS frontend

## Setup

You need two free API keys:
- Groq: https://console.groq.com
- Gemini: https://aistudio.google.com

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

And add chnage the following the in the .env

```
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
```

Run it:

```bash
python app.py
```

Open http://localhost:5000
# QuizSelf
