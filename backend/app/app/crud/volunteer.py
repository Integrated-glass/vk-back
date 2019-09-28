from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from datetime import MINYEAR
from app.db_models.models import VolunteerLogin, Volunteer
from app.models.models import VolunteerForm, VolunteerPatch


def create(db_session: Session, *, user_in: VolunteerForm) -> VolunteerLogin:
    data = dict(user_in)
    user = VolunteerLogin(
        **data
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def get_login(db_session: Session, *, user_in: VolunteerForm) -> Optional[VolunteerLogin]:
    user = db_session.query(VolunteerLogin).filter(VolunteerLogin.vk_id == user_in.vk_id).one_or_none()
    return user


def get_login_vk_id(db_session: Session, *, vk_id: int) -> Optional[VolunteerLogin]:
    user = db_session.query(VolunteerLogin).filter(VolunteerLogin.vk_id == vk_id).one_or_none()
    return user


def get_vk_id(db_session: Session, *, login_id: int) -> Optional[Volunteer]:
    return db_session.query(Volunteer).filter(Volunteer.login_id == login_id).first()


def update(db_session: Session, *, user: Volunteer, user_in: VolunteerPatch):
    user_data = jsonable_encoder(user)
    update_data = user_in.dict(skip_defaults=True)

    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user
