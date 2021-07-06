import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .model.model_loader import ModelManager
from .model.post_process import download_dict
from .routes.api import api
from .routes.authentication import authentication
from .routes.readiness import readiness
from .routes.vue_router import vue_frontend
from .utils import tracing

logging.getLogger("uvicorn").propagate = False
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

tracing.set_up()

app = FastAPI()
app.include_router(vue_frontend(__file__))
app.include_router(api)
app.include_router(readiness)
app.include_router(authentication)

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tracing.instrument_app(app)


@app.on_event("startup")
async def load_model():
    """ Load ml model and download dictionaries at startup. """
    ModelManager.instance().fetch_model()
    download_dict()
