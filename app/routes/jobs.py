from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.job import Job


router = APIRouter()

VALID_STATUSES = {"new", "interested", "applied", "rejected"}


@router.post("/jobs/{job_id}/status")
async def update_job_status(
    job_id: int,
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    if status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid status '{status}'. "
                f"Must be one of: {', '.join(sorted(VALID_STATUSES))}."
            ),
        )

    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")

    job.application_status = status
    db.commit()

    return RedirectResponse(url="/", status_code=303)


@router.get("/jobs/{job_id}")
async def get_job(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")

    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "match_score": job.match_score,
        "match_reason": job.match_reason,
        "application_status": job.application_status,
        "date_found": job.date_found,
    }
