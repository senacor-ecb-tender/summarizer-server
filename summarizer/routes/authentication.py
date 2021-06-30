import secrets
from fastapi import APIRouter
from fastapi import Depends, status
from fastapi import HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

authentication = APIRouter()

security = HTTPBasic()


def check_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "ecb_test_user")
    correct_password = secrets.compare_digest(credentials.password, "B#@/:RX2uuS=`&29")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@authentication.get("/login")
def login(username: str = Depends(check_user)):
    return {"username": username}
