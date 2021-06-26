from fastapi import APIRouter, Request, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from model.summarize import predict

api = APIRouter()
templates = Jinja2Templates(directory="templates")


@api.get("/", response_class=HTMLResponse)
def index_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@api.post("/upload")
async def upload_file(topic=Form(...), summary_type=Form(...), file: UploadFile = File(...)):
    content = (await file.read()).decode('utf-8')
    result = predict(content, topic, summary_type)
    return {'result': result}
