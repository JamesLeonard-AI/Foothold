from app.database.database import SessionLocal
from app.models.job import Job


db = SessionLocal()


jobs = [
    Job(
        source="Demo",
        title="AI Automation Engineer",
        company="CloudFlow Systems",
        location="Remote",
        remote=True,
        salary_min=80000,
        salary_max=120000,
        description="Build AI automation workflows using Python, LangChain, and RAG.",
        match_score=87,
        match_reason="Strong match: Python, LangChain, and RAG experience."
    ),

    Job(
        source="Demo",
        title="Junior AI Developer",
        company="NovaTech",
        location="Remote",
        remote=True,
        salary_min=65000,
        salary_max=90000,
        description="Develop AI-powered applications and APIs.",
        match_score=78,
        match_reason="Good match: FastAPI, APIs, and machine learning skills."
    )
]


db.add_all(jobs)

db.commit()

db.close()


print("Jobs added successfully!")