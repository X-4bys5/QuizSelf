import os
import base64
import json
import re
import io
from pypdf import PdfReader
from PIL import Image
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

# groq for question generation, gemini for ocr on scanned pdfs
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

<<<<<<< HEAD
MAX_TEXT_LENGTH = 12000  # groq has a context limit cutting off at 12000 chars was the best balance of performance and quiz quality in testing


def extract_text_from_pdf(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))   # normal pdfs with selectable text just extract directly
=======
# groq has a context limit, cutting off at 12000 chars was the sweet spot
MAX_TEXT_LENGTH = 12000


def extract_text_from_pdf(file_bytes):
    # normal pdfs with selectable text, just extract directly
    reader = PdfReader(io.BytesIO(file_bytes))
>>>>>>> 297ac9d2b883e1221d3d7f66e6285871cbfec0ff
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def ocr_with_gemini(file_bytes):
<<<<<<< HEAD
    reader = PdfReader(io.BytesIO(file_bytes))  # scanned pdfs have no selectable text, so we pull the images out and send them to gemini
=======
    # scanned pdfs have no selectable text, so we pull the images out and send them to gemini
    reader = PdfReader(io.BytesIO(file_bytes))
>>>>>>> 297ac9d2b883e1221d3d7f66e6285871cbfec0ff
    all_text = []

    for page in reader.pages:
        img_list = page.images
        for img in img_list:
            img_bytes = img.data
<<<<<<< HEAD
            img_b64 = base64.b64encode(img_bytes).decode("utf-8")  # gemini needs base64 encoded images
=======
            # gemini needs base64 encoded images
            img_b64 = base64.b64encode(img_bytes).decode("utf-8")
>>>>>>> 297ac9d2b883e1221d3d7f66e6285871cbfec0ff
            response = gemini_model.generate_content([
                {"mime_type": "image/jpeg", "data": img_b64},
                "Transcribe all text from this image exactly."
            ])
            all_text.append(response.text or "")

    return "\n\n".join(all_text).strip()


def generate_quiz(text, question_count, question_types, difficulty):
    type_str = ", ".join(question_types)

    # medium is the default, easy was too surface level in testing
    difficulty_note = {
        "Easy": "Focus on basic facts and definitions.",
        "Medium": "Focus on relationships and comparisons.",
        "Hard": "Focus on synthesis, implications and subtle details."
    }.get(difficulty, "Focus on relationships and comparisons.")

    # the prompt took a while to get right
    # groq kept returning different formats so had to be very specific with the rules
<<<<<<< HEAD

=======
>>>>>>> 297ac9d2b883e1221d3d7f66e6285871cbfec0ff
    prompt = f"""You are a quiz generator. Generate {question_count} questions from the text below.

Question types to use: {type_str}
Difficulty: {difficulty} — {difficulty_note}

Rules:
- For MCQ: provide exactly 4 options, no A/B/C/D prefixes
- For T/F: correct_answer must be exactly "True" or "False", options must be ["True", "False"]
- For Theory: provide a model answer, options must be []
- Every question must include a brief explanation and a short quote from the source text
- Cover the entire document, not just the beginning
- Return ONLY valid JSON, nothing else

Format:
{{
  "questions": [
    {{
      "type": "MCQ",
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "correct_answer": "...",
      "explanation": "...",
      "source_text": "..."
    }}
  ]
}}

Document:
{text[:MAX_TEXT_LENGTH]}
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
<<<<<<< HEAD
        temperature=0.3   # lower temperature = more consistent json output
    )

    raw = response.choices[0].message.content
    
=======
        temperature=0.3  # lower temperature = more consistent json output
    )

    raw = response.choices[0].message.content

>>>>>>> 297ac9d2b883e1221d3d7f66e6285871cbfec0ff
    # groq wraps the json in markdown fences sometimes even when you tell it not to
    raw = re.sub(r'^```json', '', raw.strip())
    raw = re.sub(r'^```', '', raw.strip())
    raw = re.sub(r'```$', '', raw.strip())

    # grab just the json part in case theres extra text before or after it
    first_brace = raw.find('{')
    last_brace = raw.rfind('}')
    if first_brace != -1 and last_brace != -1:
        raw = raw[first_brace:last_brace + 1]

    data = json.loads(raw)
    return data.get("questions", [])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["pdf"]
    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    file_bytes = file.read()

    try:
        text = extract_text_from_pdf(file_bytes)

        # less than 100 chars basically means the pdf is scanned, switch to ocr
        if len(text) < 100:
            text = ocr_with_gemini(file_bytes)

        if len(text) < 50:
            return jsonify({"error": "Could not extract readable text from this PDF"}), 400

        return jsonify({"text": text[:MAX_TEXT_LENGTH], "length": len(text)})

    except Exception as e:
        return jsonify({"error": f"Failed to process PDF: {str(e)}"}), 500


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    text = data.get("text", "").strip()
    question_count = int(data.get("question_count", 5))
    question_types = data.get("question_types", ["MCQ"])
    difficulty = data.get("difficulty", "Medium")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    if not question_types:
        return jsonify({"error": "Select at least one question type"}), 400

    try:
        questions = generate_quiz(text, question_count, question_types, difficulty)
        return jsonify({"questions": questions})
    except Exception as e:
        return jsonify({"error": f"Failed to generate quiz: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
