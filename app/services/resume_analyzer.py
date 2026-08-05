import json

from app.services.llm import ask_llm


def analyze_resume(resume_text: str) -> dict:
    prompt = f"""
You are an expert technical recruiter.

Analyze the resume below and return ONLY valid JSON.

Always include every field, even when the resume does not provide the information.

Use this exact structure:

{{
    "name": "",
    "skills": [],
    "certifications": [],
    "experience": [],
    "education": []
}}

Resume:
{resume_text}
"""

    response = ask_llm(prompt)
    return json.loads(response)