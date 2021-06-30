import logging
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .model.model_loader import ModelManager
from .routes.api import api
from .routes.readiness import readiness
from .routes.authentication import authentication

logging.getLogger("uvicorn").propagate = False
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = FastAPI()
app.include_router(api)
app.include_router(readiness)
app.include_router(authentication)

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


@app.on_event("startup")
async def load_model():
    ModelManager.instance().fetch_model()
