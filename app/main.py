import logging
import logging.config

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers.static import router as static_router
from routers.recognition import router as recognition_router
from routers.docs import router as docs_router

from config import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("sms_routing_log")


def create_app() -> FastAPI:
    current_app = FastAPI(
        title="RecognitionAPI",
        description="API for image recognition",
        version="0.0.1",
    )

    current_app.include_router(static_router)
    current_app.include_router(recognition_router)
    current_app.include_router(docs_router)

    return current_app

app = create_app()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4000, reload=True)
