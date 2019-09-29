from sqlalchemy.orm import Session
from app.db_models.models import VolunteerVisit


def log_volunteer_visit(db_session: Session, *, volunteer_id: int) -> VolunteerVisit:
  new_visit: VolunteerVisit = VolunteerVisit(volunteer_id=volunteer_id)
  db_session.add(new_visit)
  db_session.commit()
  db_session.refresh(new_visit)

  return new_visit


def log_volunteer_event_visit(
  db_session: Session,
  *,
  volunteer_id: int,
  event_id: int
) -> VolunteerVisit:
  new_visit: VolunteerVisit = VolunteerVisit(volunteer_id=volunteer_id, event_id=event_id)
  db_session.add(new_visit)
  db_session.commit()
  db_session.refresh(new_visit)

  return new_visit


def get_by_volunteer_id_event_id(
  db_session: Session,
  *,
  volunteer_id: int,
  event_id: int
) -> VolunteerVisit:
  return db_session\
    .query(VolunteerVisit)\
    .filter_by(
      volunteer_id=volunteer_id,
      event_id=event_id
    )\
    .one_or_none()
