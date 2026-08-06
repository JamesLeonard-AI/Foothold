from sqlalchemy.orm import Session

from app.models.resume_analysis import ResumeAnalysis


def save_resume_analysis(
    db: Session,
    filename: str,
    raw_text: str,
    analysis: dict,
) -> ResumeAnalysis:
    record = ResumeAnalysis(
        filename=filename,
        name=analysis.get("name"),
        raw_text=raw_text,
        analysis_json=analysis,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record