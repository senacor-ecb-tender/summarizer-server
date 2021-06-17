from fastapi import FastAPI
from routes.api import api
from routes.readiness import readiness
from routes.liveness import liveness

app = FastAPI()
app.include_router(api)
app.include_router(readiness)
app.include_router(liveness)

