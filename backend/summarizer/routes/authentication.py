import secrets
from fastapi import APIRouter
from fastapi import Depends, status
from fastapi import HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

authentication = APIRouter()

security = HTTPBasic()


def check_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "senacor")
    correct_password = secrets.compare_digest(credentials.password, "frankfurt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@authentication.get("/login")
def login(username: str = Depends(check_user)):
    """ Simple Login Request that returns the username if the user has logged in before """
    return {"username": username}
