from typing import Optional

from app.db_models.models import Event, Partner
from sqlalchemy.orm import Session


def get(db_session: Session, *, event_id: int) -> Optional[Event]:
    return db_session.query(Event).filter(Event.id == event_id).first()
