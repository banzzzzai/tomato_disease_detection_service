import base64
import redis
import logging

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel
from starlette.responses import JSONResponse

from config import  REDIS_HOST, REDIS_PORT
from asynchrony.tasks.recognize_image import recognize_image_task

logger = logging.getLogger("sms_routing_log")

router = APIRouter(prefix="/recognition", tags=["recognition"])

redis_conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

class RecognitionData(BaseModel):
    image: str


async def common_parameters(skip: int = 0, limit: int = 50):
    return {"skip": skip, "limit": limit}


@router.get("/")
def check_status():
    return {"status": "recognition service is running"}


@router.post("/")
async def recognize_image(file: UploadFile = File(...)):
    logger.info("recognize_image method start")
    try:
        # читаем файл и кодируем в base64
        image_bytes = await file.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        # синхронный вызов задачи
        output = recognize_image_task.apply(
            args=[image_b64],
            queue="image_recognition"
        ).get()

        logger.info(f"recognition result: {output}")
        return JSONResponse(output)

    except Exception as e:
        logger.exception("Error while recognize_image method")
        return JSONResponse({"error": "Something went wrong."}, status_code=500)


