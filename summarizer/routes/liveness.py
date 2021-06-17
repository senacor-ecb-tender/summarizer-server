from fastapi import APIRouter
from socket import gethostname
liveness = APIRouter()


@liveness.get("/probes/liveness")
def get_liveness():
    return {"hostname": gethostname()}
