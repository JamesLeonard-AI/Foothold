import json

from app.services.llm import ask_llm


def analyze_resume(resume_text: str) -> dict:
    prompt = f"""
You are a precise resume data-extraction system.

Extract information only from the resume text provided.
Do not invent, infer, rename, or embellish information.
Keep professional employment separate from projects.
Return ONLY valid JSON with exactly this structure:

{{
    "name": "",
    "skills": [],
    "certifications": [],
    "professional_experience": [
        {{
            "title": "",
            "company": "",
            "start_date": "",
            "end_date": "",
            "responsibilities": []
        }}
    ],
    "projects": [
        {{
            "name": "",
            "status": "",
            "description": [],
            "technologies": []
        }}
    ],
    "education": [
        {{
            "school": "",
            "degree": "",
            "field": "",
            "expected_graduation": ""
        }}
    ]
}}

Rules:
- Include every top-level field.
- Use empty strings or empty lists when information is missing.
- Do not place projects under professional_experience.
- Do not infer technologies that are not explicitly listed.
- Preserve phrases such as "(Learning)" when present.
- Do not add fields outside the required structure.

Resume:
{resume_text}
"""

    response = ask_llm(prompt)
    return json.loads(response)