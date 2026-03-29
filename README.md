# QuizSelf

upload a pdf and get quiz questions generated from it. i made this to study for exams by uploading my notes and quizzing myself on them. supports normal and scanned pdfs.

## how it works

- normal pdfs get text extracted directly with pymupdf
- scanned pdfs (no selectable text) get sent to gemini for ocr
- the extracted text goes to groq which generates the questions
- supports mcq, true/false, and theory questions
- you can set difficulty and how many questions you want

## stack
```
- python + flask
- groq api for generating questions
- gemini api for ocr on scanned pdfs
- pymupdf for text extraction
- html css js frontend
```
## setup

you need two free api keys:
- groq: https://console.groq.com
- gemini: https://aistudio.google.com
```
git clone https://github.com/X-4bys5/QuizSelf.git
cd QuizSelf
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
create a .env file and add:
```
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
```
run:
python app.py

open http://localhost:5000

## known issues

- scanned pdfs with really bad quality sometimes return garbage text
- groq occasionally wraps the json response in markdown even when told not to, theres a fix in the code for this but it doesnt always catch everything
- theory questions can sometimes be vague depending on the pdf
