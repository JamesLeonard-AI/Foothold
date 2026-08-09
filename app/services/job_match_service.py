import json

from app.services.llm import ask_llm_json

JOB_MATCH_SCHEMA = {
    "type": "object",
    "properties": {
        "required_skills": {
            "type": "array",
            "items": {"type": "string"},
        },
        "matched_required_skills": {
            "type": "array",
            "items": {"type": "string"},
        },
        "required_experience": {
            "type": "array",
            "items": {"type": "string"},
        },
        "matched_required_experience": {
            "type": "array",
            "items": {"type": "string"},
        },
        "preferred_skills": {
            "type": "array",
            "items": {"type": "string"},
        },
        "matched_preferred_skills": {
            "type": "array",
            "items": {"type": "string"},
        },
        "education_requirement": {
            "type": "string",
        },
        "education_match": {
            "type": "string",
            "enum": ["none", "equivalent", "meets"],
        },
        "strengths": {
            "type": "array",
            "items": {"type": "string"},
        },
        "missing_skills": {
            "type": "array",
            "items": {"type": "string"},
        },
        "recommendations": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": [
        "required_skills",
        "matched_required_skills",
        "required_experience",
        "matched_required_experience",
        "preferred_skills",
        "matched_preferred_skills",
        "education_requirement",
        "education_match",
        "strengths",
        "missing_skills",
        "recommendations",
    ],
    "additionalProperties": False,
}

def compare_resume_to_job(
    resume_analysis: dict,
    job_description: str,
) -> dict:
    prompt = f"""
You are a technical recruiter and job-fit evaluator.

Compare the candidate's structured resume data against the supplied job description.

Evaluate fit conservatively and realistically.

Return ONLY valid JSON with exactly this structure:

{{
    "required_skills": [],
    "matched_required_skills": [],
    "required_experience": [],
    "matched_required_experience": [],
    "preferred_skills": [],
    "matched_preferred_skills": [],
    "education_requirement": "",
    "education_match": "none",
    "strengths": [],
    "missing_skills": [],
    "recommendations": []
}}

Rules:
- required_skills must contain distinct technical skills, platforms, tools, systems, or technical capabilities that the job description requires or clearly expects.
- matched_required_skills may contain only required skills directly supported by evidence in the resume.
- Related knowledge does not automatically count as a match for a specific required technology.
- required_experience must contain distinct professional experience requirements, such as years of experience, production deployment experience, consulting experience, enterprise integration experience, or stakeholder enablement.
- matched_required_experience may contain only experience requirements clearly supported by professional experience on the resume.
- Projects, certifications, coursework, or skills marked as learning do not count as professional experience.
- preferred_skills must contain qualifications explicitly described as preferred, desired, a plus, nice-to-have, or equivalent optional language.
- matched_preferred_skills may contain only preferred qualifications directly supported by the resume.
- education_requirement must contain the job's stated education requirement. Use an empty string if none exists.
- education_match must be exactly one of: "none", "equivalent", or "meets".
- Use "meets" only when the resume directly satisfies the stated education requirement.
- Use "equivalent" only when the job explicitly permits equivalent experience and the resume provides reasonable evidence for that equivalency.
- Do not place education or years-of-experience requirements in required_skills.
- Education requirements must appear only in education_requirement and must never appear in required_experience or required_skills.
- A required_experience item may be included in matched_required_experience only when it is supported by the professional_experience section of the resume.
- Skills, certifications, education, coursework, and projects must not be used as evidence for matched_required_experience.
- Transferable professional experience may count only when it demonstrates substantially the same capability required by the job; adjacent or loosely related experience is not sufficient.
- Do not count the same requirement in more than one category.
- Do not invent requirements that are not supported by the job description.
- strengths should identify the strongest evidence-backed areas of alignment.
- missing_skills should identify important requirements not supported by the resume.
- recommendations should be practical and specific.
- If relevant experience is present but poorly emphasized, recommend highlighting it instead of treating it as missing.
- Keep recommendations focused on truthful resume improvements only.
- Base the comparison only on the supplied resume analysis and job description.

Resume Analysis:
{json.dumps(resume_analysis, indent=2)}

Job Description:
{job_description}
"""

    return ask_llm_json(
        prompt=prompt,
        schema=JOB_MATCH_SCHEMA,
    )