import logging

from fastapi import APIRouter, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from ..model.model_loader import ModelManager, ModelSettings
from ..model.summarize import GenerationSettings, gen_settings
from ..model.summarize import LongSettings, long_settings, ShortSettings, short_settings
from ..model.summarize import predict
from ..utils.tracing import TracingSettings, tracing_settings

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
    content = (await file.read()).decode('utf-8', 'ignore')
    result = predict(content, topic, summary_type, ModelManager.instance())
    return {'result': result}


class ConfigResponse(BaseModel):
    model_settings: ModelSettings
    generation_settings: GenerationSettings
    short_settings: ShortSettings
    long_settings: LongSettings
    tracing_settings: TracingSettings


@api.get("/config")
def get_config() -> ConfigResponse:
    """Get the current service configuration."""
    return ConfigResponse(model_settings=ModelManager.instance().read_config(),
                          generation_settings=gen_settings,
                          short_settings=short_settings,
                          long_settings=long_settings,
                          tracing_settings=tracing_settings)
