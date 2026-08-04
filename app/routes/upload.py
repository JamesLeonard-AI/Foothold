from pathlib import Path

from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

UPLOAD_FOLDER = Path("app/resumes")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@router.get("/upload")
def upload_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="upload.html",
    )


@router.post("/upload")
async def upload_resume(resume: UploadFile = File(...)):
    destination = UPLOAD_FOLDER / resume.filename

    with destination.open("wb") as buffer:
        buffer.write(await resume.read())

    return RedirectResponse(url="/", status_code=303)