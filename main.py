from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def home(request: Request):

    jobs = [
        {
            "title": "AI Automation Engineer",
            "company": "CloudFlow Systems",
            "score": 87,
            "skills": [
                "Python",
                "LangChain",
                "RAG"
            ]
        },
        {
            "title": "Junior AI Developer",
            "company": "NovaTech",
            "score": 78,
            "skills": [
                "FastAPI",
                "APIs",
                "Machine Learning"
            ]
        }
    ]

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "jobs": jobs
        }
    )