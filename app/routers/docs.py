from fastapi.openapi.docs import get_swagger_ui_html

from fastapi import APIRouter

router = APIRouter(prefix="/docs", tags=["docs"])


@router.get("")
async def docs():
    return get_swagger_ui_html(openapi_url="/openapi.json")

