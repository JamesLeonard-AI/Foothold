from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.job import Job
from app.models.resume_analysis import ResumeAnalysis
from app.services.job_evidence_service import evaluate_resume_evidence
from app.services.job_match_score import calculate_job_match_score
from app.services.job_requirement_service import extract_job_requirements


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
    job_title: str = Form(""),
    company_name: str = Form(""),
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
                "job_title": job_title,
                "company_name": company_name,
                "error": "No analyzed resume was found.",
            },
        )

    # Stage 1: Extract canonical job requirements.
    job_requirements = extract_job_requirements(
        job_description=job_description,
    )

    # Stage 2: Evaluate resume evidence.
    evidence_result = evaluate_resume_evidence(
        resume_analysis=latest_analysis.analysis_json,
        job_requirements=job_requirements,
    )

    # Stage 3: Calculate deterministic score.
    match_score = calculate_job_match_score(
        capability_results=evidence_result["capability_results"],
        experience_status=evidence_result["experience_status"],
        education_status=evidence_result["education_status"],
    )

    matched_capabilities = [
        result
        for result in evidence_result["capability_results"]
        if result["status"] == "matched"
    ]

    partial_capabilities = [
        result
        for result in evidence_result["capability_results"]
        if result["status"] == "partial"
    ]

    missing_capabilities = [
        result
        for result in evidence_result["capability_results"]
        if result["status"] == "not_matched"
    ]

    CATEGORY_LABELS = {
        "ai_solution_development": "AI Solution Development",
        "agent_architecture_rag": "Agent Architecture & RAG",
        "ai_platform_administration": "AI Platform Administration",
        "enterprise_integrations": "Enterprise Integrations",
        "data_pipelines": "Data Pipelines",
        "api_connectivity": "API & Connectivity",
        "workflow_automation": "Workflow Automation",
        "debugging": "Debugging & Root-Cause Analysis",
        "monitoring_observability": "Monitoring & Observability",
        "documentation_enablement": "Documentation & Enablement",
    }

    strengths = [
        (
            f'{CATEGORY_LABELS.get(result["category"], result["category"])}: '
            f'{result["evidence"]}'
        )
        for result in matched_capabilities
    ]

    missing_skills = [
        CATEGORY_LABELS.get(
            result["category"],
            result["category"],
        )
        for result in missing_capabilities
    ]

    recommendations = [
        (
            "Strengthen or document evidence for: "
            + CATEGORY_LABELS.get(
                result["category"],
                result["category"],
            )
        )
        for result in (
            partial_capabilities
            + missing_capabilities
        )
    ]

    # Persist this match result so it shows up on the dashboard and
    # can be tracked (applied / interested / rejected) over time.
    match_reason_summary = (
        f"{len(matched_capabilities)} matched, "
        f"{len(partial_capabilities)} partial, "
        f"{len(missing_capabilities)} missing capabilities. "
        f"Experience: {evidence_result['experience_status']}. "
        f"Education: {evidence_result['education_status']}."
    )

    saved_job = Job(
        source="manual",
        title=job_title.strip() if job_title.strip() else "Untitled Position",
        company=company_name.strip() if company_name.strip() else "Unknown Company",
        description=job_description,
        match_score=match_score,
        match_reason=match_reason_summary,
        application_status="new",
    )

    db.add(saved_job)
    db.commit()
    db.refresh(saved_job)

    match_result = {
        "capabilities": job_requirements["capabilities"],
        "capability_results": evidence_result["capability_results"],
        "matched_capabilities": matched_capabilities,
        "partial_capabilities": partial_capabilities,
        "missing_capabilities": missing_capabilities,
        "experience_requirement": job_requirements[
            "experience_requirement"
        ],
        "experience_status": evidence_result["experience_status"],
        "experience_evidence": evidence_result[
            "experience_evidence"
        ],
        "education_requirement": job_requirements[
            "education_requirement"
        ],
        "education_match": evidence_result["education_status"],
        "education_evidence": evidence_result[
            "education_evidence"
        ],
        "strengths": strengths,
        "missing_skills": missing_skills,
        "recommendations": recommendations,
    }

    return templates.TemplateResponse(
        request=request,
        name="job_match.html",
        context={
            "job_description": job_description,
            "job_title": job_title,
            "company_name": company_name,
            "match_result": match_result,
            "match_score": match_score,
            "saved_job_id": saved_job.id,
        },
    )