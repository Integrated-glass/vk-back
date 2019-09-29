from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.db_models.models import VolunteerLogin, Volunteer, EventVolunteer, ParticipationStatus, Event, Role
from app.models.models import VolunteerForm, VolunteerPatch, EventApplication
from app.api.utils.list import get_from_list_or_default


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


def get_by_id(db_session: Session, volunteer_id: int) -> Volunteer:
    return db_session \
        .query(Volunteer) \
        .filter_by(id=volunteer_id) \
        .one_or_none()


def get_by_volunteer_id(db_session: Session, volunteer_id: int) -> Volunteer:
    return db_session \
        .query(Volunteer) \
        .filter_by(volunteer_id=volunteer_id) \
        .one_or_none()


def apply(db_session: Session, application: EventApplication, volunteer: Volunteer,
          event: Event, roles_can_apply: List[Role]):
    roles_can_apply = list(map(lambda x: getattr(x, "id", None), roles_can_apply))
    event_application = EventVolunteer(
        event_id=application.event_id,
        volunteer_id=volunteer.id,
        karma_to_pay=event.base_karma_to_pay,
        need_paper_certificate=application.need_paper_certificate,
        motivation=application.motivation,
        participation_status=ParticipationStatus.WAITING,
        comment=application.comment,
        actual_role_id=None,
        preferable_role1_id=get_from_list_or_default(roles_can_apply, 0),
        preferable_role2_id=get_from_list_or_default(roles_can_apply, 1),
        preferable_role3_id=get_from_list_or_default(roles_can_apply, 2),
    )

    db_session.add(event_application)
    db_session.commit()
    db_session.refresh(event_application)
