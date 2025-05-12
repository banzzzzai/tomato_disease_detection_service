import logging

from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

logger = logging.getLogger("sms_routing_log")

router = APIRouter()

class RecognitionData(BaseModel):
    image: str


async def common_parameters(skip: int = 0, limit: int = 50):
    return {"skip": skip, "limit": limit}

router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/")
async def home():
    return FileResponse("static/index.html")
