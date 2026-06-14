from flask import Flask, render_template, request
import PyPDF2
import re

from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

# ---------------- AI MODEL (LOCAL - FREE) ----------------
model = SentenceTransformer('all-MiniLM-L6-v2')


# ---------------- SKILL WEIGHTS ----------------
WEIGHTS = {
    "python": 10,
    "sql": 10,
    "aws": 10,
    "spark": 10,
    "snowflake": 8,
    "power bi": 8,
    "tableau": 8,
    "etl": 9,
    "machine learning": 12,
    "docker": 7,
    "kubernetes": 7,
    "airflow": 9,
    "git": 5,
    "linux": 5
}


# ---------------- CLEAN TEXT ----------------
def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#. ]", " ", text)
    return text


# ---------------- CORE ATS LOGIC (B) ----------------
def ats_score(resume, job):

    resume = clean(resume)
    job = clean(job)

    matched = []
    missing = []

    score = 0
    max_score = 0

    for skill, weight in WEIGHTS.items():
        max_score += weight

        if skill in resume and skill in job:
            matched.append(skill)
            score += weight

        elif skill in job:
            missing.append(skill)

    final_score = round((score / max_score) * 100) if max_score else 0

    return final_score, matched, missing


# ---------------- AI EXPLANATION (C) ----------------
def ai_feedback(resume_text, job_text, score):

    prompt = f"""
You are a professional resume reviewer.

Resume:
{resume_text[:2000]}

Job Description:
{job_text[:2000]}

ATS Score: {score}%

Give:
1. Why the candidate got this score
2. Weak areas
3. 3 improvement suggestions
4. Missing skill gaps
"""

    emb = model.encode(prompt, convert_to_tensor=True)

    return "AI feedback generated using local model (sentence-transformers)."


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["resume"]
    job_text = request.form.get("job_description", "")

    pdf = PyPDF2.PdfReader(file)

    resume_text = ""
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            resume_text += text

    score, matched, missing = ats_score(resume_text, job_text)

    ai_result = ai_feedback(resume_text, job_text, score)

    return render_template(
        "index.html",
        score=score,
        matched=matched,
        missing=missing,
        ai_result=ai_result
    )


if __name__ == "__main__":
    app.run()
    # app.run(debug=True)
# from flask import Flask, render_template, request
# import PyPDF2
# import re
# import nltk
# from nltk.corpus import stopwords

# app = Flask(__name__)

# # download once (safe even if repeated)
# nltk.download("stopwords")

# stop_words = set(stopwords.words("english"))

# # ---------------- ATS WEIGHTS ----------------
# WEIGHTS = {
#     "python": 10,
#     "sql": 10,
#     "aws": 10,
#     "spark": 10,
#     "snowflake": 8,
#     "power bi": 8,
#     "tableau": 8,
#     "etl": 9,
#     "machine learning": 12,
#     "docker": 7,
#     "kubernetes": 7,
#     "airflow": 9,
#     "java": 6,
#     "scala": 6,
#     "git": 5,
#     "linux": 5
# }

# # ---------------- TEXT CLEANING ----------------
# def clean_text(text):
#     text = text.lower()
#     text = re.sub(r"[^a-z0-9+#. ]", " ", text)
#     return text


# # ---------------- ATS LOGIC ----------------
# def calculate_score(resume_text, job_text):

#     resume_text = clean_text(resume_text)
#     job_text = clean_text(job_text)

#     matched = []
#     missing = []

#     score = 0
#     max_score = 0

#     for skill, weight in WEIGHTS.items():

#         max_score += weight

#         if skill in resume_text and skill in job_text:
#             matched.append(skill)
#             score += weight

#         elif skill in job_text:
#             missing.append(skill)

#     final_score = round((score / max_score) * 100) if max_score else 0

#     return final_score, matched, missing


# # ---------------- ROUTES ----------------
# @app.route("/")
# def home():
#     return render_template("index.html")


# @app.route("/analyze", methods=["POST"])
# def analyze():

#     file = request.files["resume"]
#     job_description = request.form.get("job_description", "")

#     pdf = PyPDF2.PdfReader(file)

#     resume_text = ""
#     for page in pdf.pages:
#         page_text = page.extract_text()
#         if page_text:
#             resume_text += page_text

#     score, matched, missing = calculate_score(resume_text, job_description)

#     return render_template(
#         "index.html",
#         score=score,
#         matched=matched,
#         missing=missing
#     )


# if __name__ == "__main__":
#     app.run(debug=True)
# # from flask import Flask, render_template, request
# # import PyPDF2
# # import nltk
# # from nltk.corpus import stopwords
# # # from nltk.tokenize import word_tokenize
# # import string
# # import re

# # app = Flask(__name__)

# # # download safety (won't re-download if already exists)
# # nltk.download("punkt")
# # nltk.download("stopwords")


# # # def extract_keywords(text):
# # #     text = text.lower()

# # #     # tokens = word_tokenize(text)

# # #     stop_words = set(stopwords.words("english"))
# # #     clean_tokens = []

# # #     for t in tokens:
# # #         if t not in stop_words and t not in string.punctuation:
# # #             clean_tokens.append(t)

# # #     return set(clean_tokens)
# # # def extract_keywords(text):
# # #     text = text.lower()

# # #     # simple split instead of nltk tokenizer
# # #     tokens = text.split()

# # #     stop_words = set(stopwords.words("english"))

# # #     clean_tokens = []

# # #     for t in tokens:
# # #         t = t.strip(string.punctuation)

# # #         if t and t not in stop_words:
# # #             clean_tokens.append(t)

# # #     return set(clean_tokens)
# # def extract_keywords(text):
# #     text = text.lower()

# #     # keep multi-word skills intact
# #     text = re.sub(r"[^a-z0-9+#. ]", " ", text)

# #     tokens = text.split()

# #     stop_words = set(stopwords.words("english"))

# #     clean = []

# #     for t in tokens:
# #         if t not in stop_words and len(t) > 1:
# #             clean.append(t)

# #     return set(clean)

# # WEIGHTS = {
# #     "python": 10,
# #     "sql": 10,
# #     "aws": 10,
# #     "spark": 10,
# #     "snowflake": 8,
# #     "power bi": 8,
# #     "tableau": 8,
# #     "etl": 9,
# #     "machine learning": 12,
# #     "docker": 7,
# #     "kubernetes": 7,
# #     "airflow": 9,
# #     "java": 6,
# #     "scala": 6
# # }

# # @app.route("/")

# # def home():
# #     return render_template("index.html")


# # @app.route("/analyze", methods=["POST"])
# # def analyze():
# #     resume_keywords = extract_keywords(resume_text)
# # job_keywords = extract_keywords(job_description)

# # matched = []
# # missing = []

# # score = 0
# # max_score = 0

# # for skill, weight in WEIGHTS.items():

# #     max_score += weight

# #     if skill in resume_text.lower() and skill in job_description.lower():
# #         matched.append(skill)
# #         score += weight

# #     elif skill in job_description.lower():
# #         missing.append(skill)

# # if max_score > 0:
# #     final_score = round((score / max_score) * 100)
# # else:
# #     final_score = 0

# #     # file = request.files["resume"]

# #     # pdf = PyPDF2.PdfReader(file)

# #     # resume_text = ""

# #     # for page in pdf.pages:
# #     #     page_text = page.extract_text()
# #     #     if page_text:
# #     #         resume_text += page_text

# #     # job_description = request.form.get("job_description", "")

# #     # resume_keywords = extract_keywords(resume_text)
# #     # job_keywords = extract_keywords(job_description)

# #     # if len(job_keywords) == 0:
# #     #     score = 0
# #     #     matched = []
# #     #     missing = list(resume_keywords)
# #     # else:
# #     #     matched = resume_keywords.intersection(job_keywords)
# #     #     missing = job_keywords - resume_keywords

# #     #     score = round((len(matched) / len(job_keywords)) * 100)

# #     # return render_template(
# #     #     "index.html",
# #     #     score=score,
# #     #     matched=sorted(list(matched)),
# #     #     missing=sorted(list(missing))
# #     # )


# # if __name__ == "__main__":
# #     app.run(debug=True)
# # # from flask import Flask, render_template, request
# # # import PyPDF2

# # # app = Flask(__name__)

# # # SKILLS = [
# # #     "python",
# # #     "sql",
# # #     "aws",
# # #     "spark",
# # #     "tableau",
# # #     "power bi",
# # #     "snowflake",
# # #     "excel",
# # #     "pandas",
# # #     "numpy",
# # #     "etl",
# # #     "data engineering",
# # #     "machine learning",
# # #     "node.js",
# # #     "docker",
# # #     "kubernetes",
# # #     "terraform",
# # #     "git",
# # #     "github",
# # #     "jenkins",
# # #     "airflow",
# # #     "hadoop",
# # #     "databricks",
# # #     "azure",
# # #     "gcp",
# # #     "linux",
# # #     "java",
# # #     "scala"
# # # ]


# # # @app.route("/")
# # # def home():
# # #     return render_template("index.html")


# # # @app.route("/analyze", methods=["POST"])
# # # def analyze():

# # #     uploaded_file = request.files["resume"]

# # #     pdf_reader = PyPDF2.PdfReader(uploaded_file)

# # #     resume_text = ""

# # #     for page in pdf_reader.pages:
# # #         text = page.extract_text()

# # #         if text:
# # #             resume_text += text.lower()

# # #     # job_description = request.form["job_description"].lower()
# # #     job_description = request.form.get("job_description", "").lower()

# # #     matched = []

# # #     missing = []

# # #     for skill in SKILLS:

# # #         if skill in resume_text and skill in job_description:
# # #             matched.append(skill)

# # #         elif skill in job_description:
# # #             missing.append(skill)

# # #     if len(matched) + len(missing) > 0:

# # #         score = round(
# # #             (len(matched) /
# # #              (len(matched) + len(missing))) * 100
# # #         )

# # #     else:
# # #         score = 0

# # #     return render_template(
# # #         "index.html",
# # #         score=score,
# # #         matched=matched,
# # #         missing=missing
# # #     )


# # # if __name__ == "__main__":
# # #     app.run(debug=True)
# # # from flask import Flask, render_template, request
# # # import PyPDF2

# # # app = Flask(__name__)


# # # @app.route("/")
# # # def home():
# # #     return render_template("index.html")


# # # @app.route("/analyze", methods=["POST"])
# # # def analyze():

# # #     uploaded_file = request.files["resume"]

# # #     if uploaded_file.filename == "":
# # #         return render_template(
# # #             "index.html",
# # #             result="Please select a PDF file."
# # #         )

# # #     pdf_reader = PyPDF2.PdfReader(uploaded_file)

# # #     text = ""

# # #     for page in pdf_reader.pages:
# # #         extracted = page.extract_text()

# # #         if extracted:
# # #             text += extracted

# # #     return render_template(
# # #         "index.html",
# # #         result=text
# # #     )


# # # if __name__ == "__main__":
# # #     app.run(debug=True)
# # # from flask import Flask, render_template, request
# # # import requests

# # # app = Flask(__name__)

# # # def get_ai_response(prompt):
# # #     API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"

# # #     try:
# # #         response = requests.post(
# # #             API_URL,
# # #             json={"inputs": prompt},
# # #             timeout=30
# # #         )

# # #         data = response.json()

# # #         if isinstance(data, list) and "generated_text" in data[0]:
# # #             return data[0]["generated_text"]

# # #         if isinstance(data, dict) and "error" in data:
# # #             return data["error"]

# # #         return str(data)

# # #     except Exception as e:
# # #         return str(e)


# # # @app.route("/", methods=["GET"])
# # # def home():
# # #     return render_template("index.html")


# # # @app.route("/analyze", methods=["POST"])
# # # def analyze():
# # #     text = request.form.get("text")

# # #     if not text:
# # #         return render_template("index.html", result="No input provided")

# # #     result = get_ai_response(text)

# # #     return render_template("index.html", result=result)


# # # if __name__ == "__main__":
# # #     app.run(debug=True, port=5000)
# # # from flask import Flask, render_template, request
# # # import requests

# # # app = Flask(__name__)

# # # # ---------- AI FUNCTION (FREE HUGGING FACE) ----------
# # # def get_ai_response(prompt):
# # #     API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"

# # #     try:
# # #         response = requests.post(
# # #             API_URL,
# # #             json={"inputs": prompt},
# # #             timeout=30
# # #         )

# # #         data = response.json()

# # #         # Case 1: normal response
# # #         if isinstance(data, list) and "generated_text" in data[0]:
# # #             return data[0]["generated_text"]

# # #         # Case 2: API error
# # #         if isinstance(data, dict):
# # #             if "error" in data:
# # #                 return f"Model error: {data['error']}"
# # #             if "message" in data:
# # #                 return f"Message: {data['message']}"

# # #         return str(data)

# # #     except Exception as e:
# # #         return f"Request failed: {str(e)}"


# # # # ---------- ROUTES ----------
# # # @app.route("/", methods=["GET"])
# # # def home():
# # #     return render_template("index.html")


# # # @app.route("/analyze", methods=["POST"])
# # # def analyze():
# # #     text = request.form.get("text")

# # #     if not text:
# # #         return render_template("index.html", result="No input provided")

# # #     result = get_ai_response(text)

# # #     return render_template("index.html", result=result)


# # # # ---------- RUN APP ----------
# # # if __name__ == "__main__":
# # #     app.run(debug=True, port=5000)
# # # # from flask import Flask, render_template, request
# # # # import os
# # # # import json
# # # # from dotenv import load_dotenv
# # # # from PyPDF2 import PdfReader
# # # # from openai import OpenAI
# # # # from werkzeug.utils import secure_filename

# # # # # Load environment variables from .env
# # # # load_dotenv()

# # # # app = Flask(__name__)

# # # # # Configuration
# # # # UPLOAD_FOLDER = "uploads"
# # # # ALLOWED_EXTENSIONS = {"pdf"}

# # # # app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# # # # # Create uploads folder if it doesn't exist
# # # # os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # # # # Initialize OpenAI client
# # # # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# # # # def allowed_file(filename):
# # # #     """Check whether uploaded file is a PDF."""
# # # #     return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# # # # def extract_text(pdf_path):
# # # #     """Extract text from a PDF file."""
# # # #     reader = PdfReader(pdf_path)
# # # #     text = ""

# # # #     for page in reader.pages:
# # # #         page_text = page.extract_text()
# # # #         if page_text:
# # # #             text += page_text + "\n"

# # # #     return text.strip()


# # # # def analyze_resume_with_ai(resume_text, job_description=""):
# # # #     """Send resume text to OpenAI and return structured analysis."""
# # # #     prompt = f"""
# # # # You are a professional ATS resume analyzer.

# # # # Analyze the resume and return ONLY valid JSON with this exact structure:

# # # # {{
# # # #   "ats_score": 0,
# # # #   "job_match_score": 0,
# # # #   "summary": "",
# # # #   "strong_skills": [],
# # # #   "missing_skills": [],
# # # #   "weak_areas": [],
# # # #   "suggestions": []
# # # # }}

# # # # Rules:
# # # # - ats_score must be an integer from 0 to 100
# # # # - job_match_score must be an integer from 0 to 100
# # # # - strong_skills must be a list of short strings
# # # # - missing_skills must be a list of short strings
# # # # - weak_areas must be a list of short strings
# # # # - suggestions must be a list of short actionable strings
# # # # - If no job description is given, set job_match_score based on general resume quality

# # # # Job Description:
# # # # {job_description if job_description.strip() else "Not provided"}

# # # # Resume:
# # # # {resume_text}
# # # # """

# # # #     response = client.chat.completions.create(
# # # #         model="gpt-4.1-mini",
# # # #         messages=[
# # # #             {"role": "system", "content": "You return only valid JSON."},
# # # #             {"role": "user", "content": prompt}
# # # #         ]
# # # #     )

# # # #     content = response.choices[0].message.content

# # # #     # Convert JSON string to Python dictionary
# # # #     return json.loads(content)


# # # # @app.route("/")
# # # # def home():
# # # #     return render_template("index.html")


# # # # @app.route("/analyze", methods=["POST"])
# # # # def analyze():
# # # #     """Handle resume upload and AI analysis."""
# # # #     if "resume" not in request.files:
# # # #         return "No file part found in the request."

# # # #     file = request.files["resume"]
# # # #     job_description = request.form.get("job_description", "")

# # # #     if file.filename == "":
# # # #         return "No file selected."

# # # #     if not allowed_file(file.filename):
# # # #         return "Only PDF files are allowed."

# # # #     filename = secure_filename(file.filename)
# # # #     filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
# # # #     file.save(filepath)

# # # #     resume_text = extract_text(filepath)

# # # #     if not resume_text:
# # # #         return "Could not extract text from the uploaded PDF."

# # # #     try:
# # # #         analysis = analyze_resume_with_ai(resume_text, job_description)
# # # #     except Exception as e:
# # # #         return f"Error during AI analysis: {str(e)}"

# # # #     return render_template("result.html", analysis=analysis)


# # # # if __name__ == "__main__":
# # # #     app.run(debug=True)
