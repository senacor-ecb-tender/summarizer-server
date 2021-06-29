from fastapi import APIRouter
from fastapi import HTTPException

from ..model.model_loader import ModelManager

readiness = APIRouter()


@readiness.get("/probes/healthz")
def get_readiness():
    if ModelManager.instance().model is None:
        raise HTTPException(status_code=503, detail="Model not ready")
    return {"isReady": "true"}
