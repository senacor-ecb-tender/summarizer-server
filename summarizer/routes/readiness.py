from fastapi import APIRouter
from model.summarize import model
from fastapi import HTTPException

readiness = APIRouter()


@readiness.get("/probes/healthz")
def get_readiness():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not ready")
    return {"isReady": "true"}
