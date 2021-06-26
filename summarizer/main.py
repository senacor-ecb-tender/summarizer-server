from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import api
from routes.readiness import readiness
from routes.liveness import liveness
import logging, sys

logging.getLogger("uvicorn").propagate = False
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = FastAPI()
app.include_router(api)
app.include_router(readiness)
app.include_router(liveness)

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