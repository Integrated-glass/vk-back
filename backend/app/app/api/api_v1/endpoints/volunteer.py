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
from app.models.models import VolunteerForm, VolunteerFormResponse, VolunteerPatch

router = APIRouter()


@router.post("/login", response_model=VolunteerFormResponse)
def form_step_0(
        *,
        db: Session = Depends(get_db),
        data: VolunteerForm
):
    user = crud.volunteer.get_login(db, user_in=data)
    if user is None:
        data = crud.volunteer.create(db, user_in=data)
        return {
            "vk_id": data.vk_id,
            "name": data.name,
            "surname": data.surname,
            "date_of_birth": data.date_of_birth,
            "photo": data.photo,
            "login_id": data.id,
            "email": None,
            "phone_number": None
        }
    else:
        volunteer = user.volunteer
        return {
            "vk_id": user.vk_id,
            "name": user.name,
            "surname": user.surname,
            "date_of_birth": user.date_of_birth,
            "photo": user.photo,
            "login_id": user.id,
            "email": getattr(volunteer, "email", None),
            "phone_number": getattr(volunteer, "phone_number", None)
        }


@router.post("/patch", response_model=VolunteerPatch)
def patch(
        db: Session = Depends(get_db),
        *,
        vk_id: int = Body(...),
        update_data: VolunteerPatch
):
    volunteer_login = crud.volunteer.get_login_vk_id(db, vk_id=vk_id)
    if volunteer_login is None:
        raise HTTPException(status_code=404, detail="No login information for given volunteer found")
    else:
        volunteer = crud.volunteer.get_vk_id(db, login_id=volunteer_login.id)
        if volunteer is None:
            new_volunteer = Volunteer(login_id=volunteer_login.id)
            db.add(new_volunteer)
            db.commit()
            db.refresh(new_volunteer)
            return crud.volunteer.update(db, user=new_volunteer, user_in=update_data)
        return crud.volunteer.update(db, user=volunteer, user_in=update_data)
