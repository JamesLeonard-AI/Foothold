from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.job import Job

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def home(
    request: Request,
    db: Session = Depends(get_db)
):

    jobs = db.query(Job).all()

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "jobs": jobs
        }
    )