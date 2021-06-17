from fastapi import APIRouter

readiness = APIRouter()


@readiness.get("/probes/readiness")
def get_readiness():
    return {"isReady": "true"}
