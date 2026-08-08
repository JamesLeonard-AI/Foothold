from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.resume_analysis import ResumeAnalysis
from app.services.job_match_service import compare_resume_to_job

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/job-match", response_class=HTMLResponse)
async def job_match_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="job_match.html",
        context={
            "job_description": "",
        },
    )


@router.post("/job-match", response_class=HTMLResponse)
async def compare_job(
    request: Request,
    job_description: str = Form(...),
    db: Session = Depends(get_db),
):
    latest_analysis = (
        db.query(ResumeAnalysis)
        .order_by(ResumeAnalysis.analyzed_at.desc())
        .first()
    )

    if latest_analysis is None:
        return templates.TemplateResponse(
            request=request,
            name="job_match.html",
            context={
                "job_description": job_description,
                "error": "No analyzed resume was found.",
            },
        )

    match_result = compare_resume_to_job(
        resume_analysis=latest_analysis.analysis_json,
        job_description=job_description,
    )

    return templates.TemplateResponse(
        request=request,
        name="job_match.html",
        context={
            "job_description": job_description,
            "match_result": match_result,
        },
    )