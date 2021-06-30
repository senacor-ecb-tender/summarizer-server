from fastapi import APIRouter
from fastapi import HTTPException

from ..model.model_loader import model_mgr

readiness = APIRouter()


@readiness.get("/probes/healthz")
def get_readiness():
    if model_mgr.model is None:
        raise HTTPException(status_code=503, detail="Model not ready")
    return {"isReady": "true"}
