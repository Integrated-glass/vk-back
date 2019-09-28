from sqlalchemy.orm import Session

from app.db_models.models import EventVolunteer


def get_by_event_id_volunteer_id(
  db_session: Session,
  event_id: int,
  volunteer_id: int
) -> EventVolunteer:
  return db_session\
    .query(EventVolunteer)\
    .filter_by(
      event_id=event_id,
      volunteer_id=volunteer_id
    )\
    .one()
