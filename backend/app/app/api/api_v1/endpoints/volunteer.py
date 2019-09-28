from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.types import EmailStr
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.core import config
from app.api.utils.security import get_current_user
from app.db_models.models import Volunteer
from app.models.models import VolunteerForm, VolunteerFormResponse

router = APIRouter()


@router.post("/login", response_model=VolunteerFormResponse)
def form_step_0(
        *,
        db: Session = Depends(get_db),
        data: VolunteerForm
):
    user = crud.volunteer.get(db, user_in=data)
    if user is None:
        data = crud.volunteer.create(db, user_in=data)
        return {
            "vk_id": data.vk_id,
            "name": data.name,
            "surname": data.surname,
            "date_of_birth": data.date_of_birth,
            "photo": data.photo,
            "login_id": data.id
        }
    else:
        return {
            "vk_id": user.vk_id,
            "name": user.name,
            "surname": user.surname,
            "date_of_birth": user.date_of_birth,
            "photo": user.photo,
            "login_id": user.id
        }
