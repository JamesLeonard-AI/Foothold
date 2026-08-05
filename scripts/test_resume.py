from pathlib import Path
from pprint import pprint

from app.services.resume_analyzer import analyze_resume
from app.services.resume_parser import extract_text


resume_path = (
    Path("app/resumes")
    / "James_Leonard_AI_Automation_Resume (2).docx"
)

resume_text = extract_text(str(resume_path))

print("\n--- Extracted text preview ---\n")
print(resume_text[:1000])

print("\n--- AI analysis ---\n")
analysis = analyze_resume(resume_text)
pprint(analysis)