import logging
from fastapi import APIRouter, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..model.summarize import predict

logger = logging.getLogger(__name__)
api = APIRouter()
templates = Jinja2Templates(directory="templates")


@api.get("/", response_class=HTMLResponse)
def index_html(request: Request):
    logger.info('Debug request for basic ui.')
    return templates.TemplateResponse("index.html", {"request": request})


@api.post("/upload")
async def upload_file(topic=Form(...), summary_type=Form(...), file: UploadFile = File(...)):
    logger.info(f'Received upload for ${topic}, ${summary_type} and filename ${file.filename}')
    content = (await file.read()).decode('utf-8')
    result = predict(content, topic, summary_type)
    return {'result': result}
