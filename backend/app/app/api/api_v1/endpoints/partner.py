from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from pydantic.types import EmailStr
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.core import config
from app.api.utils.security import get_current_user
from app.db_models.models import Volunteer
from app.models.models import PartnerCreate, OrganizerInDB

router = APIRouter()


@router.post("/create", response_model=PartnerCreate)
def create(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
        *,
        partner: PartnerCreate
):
    return crud.partner.create(db, partner_in=partner)


@router.post("/link")
def link_to_event(
        db: Session = Depends(get_db),
        current_user: OrganizerInDB = Depends(get_current_user),
        event_id=Query(..., ge=0),
        partner_id=Query(..., gt=0)
):
    event = crud.event.get(db, event_id=event_id)
    partner = crud.partner.get(db, user_id=partner_id)
    

