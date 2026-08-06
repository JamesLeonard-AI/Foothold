from pathlib import Path
from pprint import pprint

from app.database.database import SessionLocal
from app.services.profile_service import save_resume_analysis
from app.services.resume_analyzer import analyze_resume
from app.services.resume_parser import extract_text


resume_path = (
    Path("app/resumes")
    / "James_Leonard_AI_Automation_Resume (2).docx"
)

resume_text = extract_text(str(resume_path))
analysis = analyze_resume(resume_text)

db = SessionLocal()

try:
    saved_analysis = save_resume_analysis(
        db=db,
        filename=resume_path.name,
        raw_text=resume_text,
        analysis=analysis,
    )

    print("\n--- Saved resume analysis ---\n")
    print(f"Database ID: {saved_analysis.id}")
    print(f"Filename: {saved_analysis.filename}")
    pprint(analysis)

finally:
    db.close()