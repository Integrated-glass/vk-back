from typing import List, Optional

from sqlalchemy.orm import Session
from datetime import MINYEAR
from app.db_models.models import VolunteerLogin
from app.models.models import VolunteerForm


def create(db_session: Session, *, user_in: VolunteerForm) -> VolunteerLogin:
    data = dict(user_in)
    user = VolunteerLogin(
        **data
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def get(db_session: Session, *, user_in: VolunteerForm) -> VolunteerLogin:
    user = db_session.query(VolunteerLogin).filter(VolunteerLogin.vk_id == user_in.vk_id).one_or_none()
    return user
