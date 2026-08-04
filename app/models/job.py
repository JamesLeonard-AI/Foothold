from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime

from app.database.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String, nullable=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)

    location = Column(String, nullable=True)
    remote = Column(Boolean, default=False)

    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)

    url = Column(String, nullable=True)

    description = Column(Text, nullable=True)

    match_score = Column(Integer, default=0)

    match_reason = Column(Text, nullable=True)

    application_status = Column(
        String,
        default="new"
    )

    date_found = Column(
        DateTime,
        default=datetime.utcnow
    )