from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.job import Job
from app.routes.analysis import router as analysis_router
from app.routes.upload import router as upload_router
from app.routes.job_match import router as job_match_router
from app.routes.jobs import router as jobs_router
from app.init_db import create_tables

app = FastAPI()

create_tables()

app.include_router(upload_router)
app.include_router(analysis_router)
app.include_router(job_match_router)
app.include_router(jobs_router)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def home(
    request: Request,
    db: Session = Depends(get_db),
):
    jobs = db.query(Job).all()

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"jobs": jobs},
    )