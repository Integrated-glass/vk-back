from typing import List, Optional

from sqlalchemy.orm import Session

from app.db_models.models import VolunteerLogin, Volunteer
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


def get_by_id(db_session: Session, volunteer_id: int) -> Volunteer:
    return db_session\
        .query(Volunteer)\
        .filter(Volunteer.id == volunteer_id)\
        .one_or_none()
