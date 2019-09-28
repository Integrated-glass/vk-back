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
from app.models.models import VolunteerForm1, VolunteerForm2, VolunteerForm3

router = APIRouter()

@router.post("/step1")
def form_step_1(
        *,
        db: Session = Depends(get_db),
        data: VolunteerForm1
):
    pass