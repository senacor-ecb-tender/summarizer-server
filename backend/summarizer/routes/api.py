import logging
from fastapi import APIRouter, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..model.summarize import predict
from ..model.model_loader import ModelManager

logger = logging.getLogger(__name__)
api = APIRouter()
templates = Jinja2Templates(directory="templates")


@api.get("/", response_class=HTMLResponse)
def index_html(request: Request):
    """  Delivers a debug ui in form of a static index html (not used in production)

    \f
    :param request: FastAPI request object.
    :return:  TemplateResponse holding the index html and the request object.
    """
    logger.info('Debug request for basic ui.')
    return templates.TemplateResponse("index.html", {"request": request})


@api.post("/upload")
async def upload_file(topic=Form(...), summary_type=Form(...), file: UploadFile = File(...)):
    """ Post route for uploading text files to be summarized

    \f
    :param topic: String holding a value of one of the topics ('climate_risk', 'asset_quality', 'credit_lending', 'pandemic')
    :param summary_type: String holding one value of ('short', 'long')
    :param file: A text file with the input to be summarized.
    :return: A JSON with one element 'result', that holds an array of summary sentences.
    """
    logger.info(f'Received upload for {topic}, {summary_type} and filename {file.filename}')
    content = (await file.read()).decode('utf-8')
    result = predict(content, topic, summary_type, ModelManager.instance())
    return {'result': result}
