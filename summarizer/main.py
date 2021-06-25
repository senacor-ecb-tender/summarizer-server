from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import api
from routes.readiness import readiness
from routes.liveness import liveness

app = FastAPI()
app.include_router(api)
app.include_router(readiness)
app.include_router(liveness)

origins = [
    "http://localhost",
    "http://localhost:8080",
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