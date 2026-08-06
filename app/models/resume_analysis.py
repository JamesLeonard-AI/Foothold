from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String, Text

from app.database.database import Base


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)
    name = Column(String, nullable=True)
    raw_text = Column(Text, nullable=True)
    analysis_json = Column(JSON, nullable=False)

    analyzed_at = Column(
        DateTime,
        default=datetime.utcnow,
    )