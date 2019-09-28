from typing import List, Optional

from sqlalchemy.orm import Session

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
