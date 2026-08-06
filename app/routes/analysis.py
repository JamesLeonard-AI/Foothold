from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
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

    resume_text = extract_text(str(resume_path))
    analysis = analyze_resume(resume_text)

    saved_analysis = save_resume_analysis(
        db=db,
        filename=filename,
        raw_text=resume_text,
        analysis=analysis,
    )

    return templates.TemplateResponse(
        request=request,
        name="analysis_results.html",
        context={
            "record": saved_analysis,
            "analysis": analysis,
        },
    )