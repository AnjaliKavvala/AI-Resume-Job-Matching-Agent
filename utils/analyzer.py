import json
import os
from dotenv import load_dotenv
from google import genai
import streamlit as st

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        GEMINI_API_KEY = None

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found.")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.6-flash"
# ============================================================
# CALL GEMINI
# ============================================================

def call_llm(prompt):
    """
    Send one request to Gemini and return the response.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "temperature": 0,
            "response_mime_type": "application/json"
        }
    )

    return response.text


# ============================================================
# RESUME + JOB ANALYSIS
# ============================================================

def resume_job_analysis(resume_text, job_description):
    """
    Analyze the resume against the job description.
    Returns structured JSON.
    """

    # Keep input reasonably small
    resume_text = resume_text[:6500]
    job_description = job_description[:4500]

    prompt = f"""
You are an AI Resume and Job Matching Agent.

Analyze this resume against this job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON.

Use exactly these keys:

{{
  "candidate_name": "",
  "education": [],
  "technical_skills": [],
  "projects": [],
  "experience": [],
  "certifications": [],
  "required_job_skills": [],
  "preferred_job_skills": [],
  "job_responsibilities": [],
  "matching_skills": [],
  "partial_matches": [],
  "missing_skills": [],
  "match_score": 0,
  "technical_gaps": [],
  "tools_framework_gaps": [],
  "knowledge_gaps": [],
  "skills_to_learn": [],
  "project_ideas": [],
  "learning_order": [],
  "technical_questions": [],
  "project_questions": [],
  "behavioral_questions": [],
  "skill_gap_questions": []
}}

RULES:

1. Return JSON only.
2. Do not use markdown.
3. Do not use ``` symbols.
4. match_score must be an integer from 0 to 100.
5. Do not invent information about the candidate.
6. Use [] when information is unavailable.
7. Keep lists short and concise.
8. Give actual job responsibilities from the job description.
9. Matching skills must be supported by both the resume and job description.
10. Missing skills should be required job skills not clearly present in the resume.
11. Generate exactly 2 technical questions.
12. Generate exactly 2 project questions.
13. Generate exactly 2 behavioral questions.
14. Generate exactly 2 skill-gap questions.
15. Keep every question short.
16. Keep project ideas short.
17. Keep learning order short.
18. Finish the complete JSON object before stopping.
"""

    raw_response = call_llm(prompt)

    print("\nAI response received.")

    try:

        result = json.loads(raw_response)

        print("✅ Valid JSON received.")

        return result

    except json.JSONDecodeError:

        print("❌ Invalid JSON received from Gemini.")

        print("\nRaw AI response:")
        print(raw_response)

        return create_empty_result()


# ============================================================
# EMPTY RESULT FALLBACK
# ============================================================

def create_empty_result():

    return {
        "candidate_name": "Not available",
        "education": [],
        "technical_skills": [],
        "projects": [],
        "experience": [],
        "certifications": [],
        "required_job_skills": [],
        "preferred_job_skills": [],
        "job_responsibilities": [],
        "matching_skills": [],
        "partial_matches": [],
        "missing_skills": [],
        "match_score": 0,
        "technical_gaps": [],
        "tools_framework_gaps": [],
        "knowledge_gaps": [],
        "skills_to_learn": [],
        "project_ideas": [],
        "learning_order": [],
        "technical_questions": [],
        "project_questions": [],
        "behavioral_questions": [],
        "skill_gap_questions": []
    }
