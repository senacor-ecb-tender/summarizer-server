from fastapi import APIRouter

api = APIRouter()


@api.get("/")
def index_html():
    return {"hello": "world"}
