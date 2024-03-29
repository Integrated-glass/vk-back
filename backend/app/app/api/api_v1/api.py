from fastapi import APIRouter

from app.api.api_v1.endpoints import \
    login, organizers, ping, volunteer, partner, qr

api_router = APIRouter()


@api_router.post("/")
def hello():
    return {"hello": "world"}


api_router.include_router(login.router, tags=["login"])
api_router.include_router(organizers.router, prefix="/organizers", tags=["organizers"])
api_router.include_router(ping.router, prefix="/ping", tags=["test"])
api_router.include_router(volunteer.router, prefix='/volunteer', tags=['volunteer'])
api_router.include_router(partner.router, prefix='/partner', tags=['partner'])
api_router.include_router(qr.qr_router, prefix="/qr", tags=["qr"])
