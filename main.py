from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.job import Job
from app.routes.upload import router as upload_router


app = FastAPI()

app.include_router(upload_router)

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