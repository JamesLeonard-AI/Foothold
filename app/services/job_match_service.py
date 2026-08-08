import json

from app.services.llm import ask_llm


def compare_resume_to_job(
    resume_analysis: dict,
    job_description: str,
) -> dict:
    prompt = f"""
You are a precise job-match evaluation system.

Compare the candidate's structured resume data against the job description.

Return ONLY valid JSON with exactly this structure:

{{
    "match_score": 0,
    "strengths": [],
    "missing_skills": [],
    "recommendations": []
}}

Rules:
- match_score must be an integer from 0 to 100.
- strengths should identify clear areas where the candidate aligns with the job.
- missing_skills should include important requirements from the job description that are not supported by the resume.
- recommendations should be specific, practical changes the candidate could make to better align with the job.
- Do not invent experience, skills, certifications, or projects.
- Base the comparison only on the supplied resume analysis and job description.

Resume Analysis:
{json.dumps(resume_analysis, indent=2)}

Job Description:
{job_description}
"""

    response = ask_llm(prompt)

    return json.loads(response)