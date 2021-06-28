import logging
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.api import api
from .routes.model import model_api
from .routes.readiness import readiness

logging.getLogger("uvicorn").propagate = False
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = FastAPI()
app.include_router(api)
app.include_router(model_api)
app.include_router(readiness)

origins = [
    "*",
    ":8080"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
