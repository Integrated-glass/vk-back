from fastapi import FastAPI
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.api.api_v1.api import api_router
from app.core import config
from app.db.session import Session
from app.api.api_v1.endpoints.qr import qr_images_directory

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI(title=config.PROJECT_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/qr-img", StaticFiles(directory=qr_images_directory), name="qr-img")
app.include_router(api_router, prefix=config.API_V1_STR)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    logger.debug("Entered middleware")
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response
