# =====================================================
# ATS RESUME ANALYZER
# =====================================================
# Author: Sree Lasya Lagamsani
#
# Project Purpose:
# This application compares a candidate's resume
# against a job description and calculates an
# ATS-style compatibility score.
#
# Features:
# - PDF Resume Upload
# - Resume Text Extraction
# - Skill Detection
# - ATS Score Calculation
# - Missing Skill Identification
# - Resume Recommendations
#
# Technologies:
# Python, Flask, PyPDF2, HTML, CSS
# =====================================================

from flask import Flask, render_template, request
import PyPDF2
import re

# Create Flask application instance
app = Flask(__name__)


# =====================================================
# TEXT CLEANING FUNCTION
# -----------------------------------------------------
# Converts text to lowercase and removes special
# characters to improve matching accuracy.
# =====================================================
def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#. ]", " ", text)
    return text


# =====================================================
# SKILL DATABASE
# -----------------------------------------------------
# Collection of technical skills used for matching
# resumes against job descriptions.
#
# Skills are grouped by role categories.
# =====================================================
SKILLS = set([

# Data Analyst
"python","sql","excel","power bi","tableau","looker","data visualization",
"data analysis","business intelligence","statistics","pandas","numpy",
"matplotlib","seaborn","reporting","dashboard","etl","data cleaning",
"kpi","metrics","forecasting","r","spss",

# Data Engineer
"spark","pyspark","hadoop","hdfs","kafka","airflow","dbt","snowflake",
"redshift","bigquery","databricks","data pipeline","data engineering",
"data warehouse","data lake","etl","elt","orchestration","dimensional modeling",
"star schema","data modeling","sql","python",

# DevOps
"docker","kubernetes","jenkins","ci cd","git","github","gitlab","linux",
"bash","terraform","ansible","cloudformation","monitoring","logging",
"prometheus","grafana","elk","devops","infrastructure as code",

# Cloud
"aws","azure","gcp","ec2","s3","lambda","rds","dynamodb","iam","vpc",
"cloudwatch","cloudtrail","api gateway","load balancing","autoscaling",
"serverless","cloud computing","cloud architecture",

# Systems Analyst
"requirements gathering","business analysis","system design","uml",
"agile","scrum","jira","confluence","sdlc","documentation",
"api integration","data mapping","stakeholder management"

])


# =====================================================
# SKILL EXTRACTION ENGINE
# -----------------------------------------------------
# Searches text and identifies technical skills
# found in the predefined skill database.
#
# Input:
# - Resume text
# - Job description text
#
# Output:
# - List of detected skills
# =====================================================
def extract_skills(text):
    text = clean(text)
    found = []

    for skill in SKILLS:
        if skill in text:
            found.append(skill)

    return sorted(set(found))


# =====================================================
# ATS SCORING ENGINE
# -----------------------------------------------------
# Compares skills found in the resume against
# skills found in the job description.
#
# Calculates:
# - ATS Score
# - Matched Skills
# - Missing Skills
# =====================================================
def ats_score(resume_text, job_text):

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_text)

    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = round((len(matched) / len(job_skills)) * 100) if job_skills else 0

    return score, matched, missing


# =====================================================
# RECOMMENDATION ENGINE
# -----------------------------------------------------
# Generates personalized recommendations based
# on ATS score and missing skills.
# =====================================================
def generate_recommendations(score, matched, missing):

    recommendations = []

    recommendations.append(
        f"You matched {len(matched)} skills and missed {len(missing)} skills."
    )

    if score < 50:
        recommendations.append("Your resume is weak for this role.")
    elif score < 75:
        recommendations.append("Your resume is moderately aligned.")
    else:
        recommendations.append("Your resume is strongly aligned.")

    for skill in missing:
        recommendations.append(f"Add experience/projects in {skill}")

    return recommendations


# =====================================================
# HOME PAGE ROUTE
# -----------------------------------------------------
# Displays the ATS Resume Analyzer interface.
# =====================================================
@app.route("/")
def home():
    return render_template("index.html")

# =====================================================
# ANALYSIS ROUTE
# -----------------------------------------------------
# Handles:
# - Resume Upload
# - PDF Parsing
# - Skill Detection
# - ATS Score Calculation
# - Recommendation Generation
#
# Returns analysis results to the user interface.
# =====================================================
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

    recommendations = generate_recommendations(score, matched, missing)

    return render_template(
        "index.html",
        score=score,
        matched=matched,
        missing=missing,
        recommendations=recommendations
    )

# =====================================================
# APPLICATION ENTRY POINT
# -----------------------------------------------------
# Runs Flask development server locally.
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)
