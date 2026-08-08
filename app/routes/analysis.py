from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.ats_service import calculate_ats_score
from app.services.profile_service import save_resume_analysis
from app.services.resume_analyzer import analyze_resume
from app.services.resume_parser import extract_text


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

RESUME_FOLDER = Path("app/resumes")


@router.get("/analyze/{filename}")
def analyze_resume_page(
    filename: str,
    request: Request,
):
    resume_path = RESUME_FOLDER / filename

    if not resume_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Resume file not found.",
        )

    return templates.TemplateResponse(
        request=request,
        name="analyze_resume.html",
        context={
            "filename": filename,
        },
    )


@router.post("/analyze/{filename}")
def run_resume_analysis(
    filename: str,
    request: Request,
    db: Session = Depends(get_db),
):
    resume_path = RESUME_FOLDER / filename

    if not resume_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Resume file not found.",
        )

    # Extract the resume text.
    resume_text = extract_text(str(resume_path))

    # Analyze the resume with the LLM.
    analysis = analyze_resume(resume_text)

    # Calculate the deterministic ATS score.
    ats_result = calculate_ats_score(analysis)

    # Save the complete AI analysis.
    saved_analysis = save_resume_analysis(
        db=db,
        filename=filename,
        raw_text=resume_text,
        analysis=analysis,
    )

    # Send prepared data to the results template.
    return templates.TemplateResponse(
        request=request,
        name="analysis_results.html",
        context={
            "record": saved_analysis,
            "name": analysis.get("name", "Candidate"),
            "skills": analysis.get("skills", []),
            "certifications": analysis.get(
                "certifications",
                [],
            ),
            "projects": analysis.get("projects", []),
            "professional_experience": analysis.get(
                "professional_experience",
                [],
            ),
            "education": analysis.get("education", []),
            "ats_score": ats_result["overall_score"],
"ats_categories": ats_result["categories"],
"ats_strengths": ats_result["strengths"],
"ats_improvements": ats_result["improvements"],
"ats_reasons": ats_result["reasons"],
        },
    )