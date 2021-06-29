import logging
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

from ..model.model_loader import ModelManager

logger = logging.getLogger(__name__)
model_api = APIRouter()
templates = Jinja2Templates(directory='templates')


@model_api.get('/model')
def get_model_form(request: Request):
    logger.info('Debug request for basic ui.')
    model_names = ModelManager.load_model_names()
    return templates.TemplateResponse('model.html', {'request': request, 'models': model_names})


@model_api.post('/model')
def load_model(model_name=Form(...), version=Form(...)):
    logger.info(f'Loading model {model_name} of version {version}')
