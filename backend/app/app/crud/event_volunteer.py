from sqlalchemy.orm import Session

from app.db_models.models import EventVolunteer, ParticipationStatus


def get_by_id(db_session: Session, *, volunteer_event_id: int) -> EventVolunteer:
  return db_session\
    .query(EventVolunteer)\
    .filter_by(id=volunteer_event_id)\
    .one_or_none()


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
    .one_or_none()


def get_by_id_and_status(
  db_session: Session,
  *,
  volunteer_event_id: int,
  status: ParticipationStatus
) -> EventVolunteer:
  return db_session\
    .query(EventVolunteer)\
    .filter_by(
      id=volunteer_event_id,
      participation_status=status
    )\
    .one_or_none()
