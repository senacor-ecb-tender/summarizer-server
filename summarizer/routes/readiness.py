from fastapi import APIRouter
from fastapi import HTTPException

from ..model.model_loader import model_mgr

readiness = APIRouter()


@readiness.get("/probes/healthz")
def get_readiness():
    """ Kubernetes end point to determine the liveness & readiness of the service

    :return: A static JSON '{"isReady": "true"}' with response code 200 if the ml model is responsive and
    status 503 otherwise.
    """
    if model_mgr.model is None:
        raise HTTPException(status_code=503, detail="Model not ready")
    return {"isReady": "true"}
