from typing import List
from datetime import date, datetime

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.types import EmailStr
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, \
    HTTP_403_FORBIDDEN, HTTP_412_PRECONDITION_FAILED, HTTP_422_UNPROCESSABLE_ENTITY

from app import crud
from app.api.utils.db import get_db
from app.core import config
from app.api.utils.security import get_current_user
from app.db_models.models import Volunteer, VolunteerLogin, Event, EventVolunteer, ParticipationStatus, Role, Organizer
from app.models.models import VolunteerForm, VolunteerFormResponse, \
    EventApplication, OkResponse, Resolve, VolunteerPatch

router = APIRouter()


@router.post("/login")
def form_step_0(
        *,
        db: Session = Depends(get_db),
        data: VolunteerForm
):
    user = crud.volunteer.get_login(db, user_in=data)
    if user is None:
        data = crud.volunteer.create(db, user_in=data)  # type:VolunteerLogin

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
        return_data = {}
        if volunteer is not None:
            volunteer_data = jsonable_encoder(volunteer)
            return_data.update({"interests": volunteer.interests})
            for field in volunteer_data:
                return_data.update({field: getattr(volunteer, field, None)})

        user_data = jsonable_encoder(user)
        for field in user_data:
            return_data.update({field: getattr(user, field, None)})
        return_data["login_id"] = user.id
        del return_data["id"]
        del return_data["volunteer"]
        return return_data


@router.post("/patch", response_model=VolunteerFormResponse)
def patch(
        db: Session = Depends(get_db),
        *,
        vk_id: int = Body(...),
        update_data: VolunteerPatch
):
    volunteer_login = crud.volunteer.get_login_vk_id(db, vk_id=vk_id)
    if volunteer_login is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No login information for given volunteer found")
    else:
        volunteer = crud.volunteer.get_vk_id(db, login_id=volunteer_login.id)
        if volunteer is None:
            new_volunteer = Volunteer(login_id=volunteer_login.id)
            db.add(new_volunteer)
            db.commit()
            db.refresh(new_volunteer)
            return crud.volunteer.update(db, user=new_volunteer, user_in=update_data)
        return crud.volunteer.update(db, user=volunteer, user_in=update_data)


@router.post("/apply", response_model=OkResponse)
def apply_to_event(
        db: Session = Depends(get_db),
        *,
        application: EventApplication
):
    event = db.query(Event).filter(Event.id == application.event_id).first()  # type: Event
    if event is None:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Мероприятие с данным id не существует"
                            )
    if event.start_datetime < datetime.today():
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Мероприятие уже началось"
                            )
    if not event.can_apply:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Регистрация на данное мероприятие закрыта"
                            )
    volunteer_login = db.query(VolunteerLogin).filter(
        VolunteerLogin.vk_id == application.vk_id).first()  # type:VolunteerLogin
    if volunteer_login is None:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Вы не авторизировались"
                            )
    volunteer = volunteer_login.volunteer  # type: Volunteer
    if volunteer is None:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Вы не заполнили анкету волонтера"
                            )
    roles_can_apply = []
    asked_roles = db.query(Role).filter(or_(Role.id == application.preferable_role1_id,
                                            Role.id == application.preferable_role2_id,
                                            Role.id == application.preferable_role3_id)).all()
    for role in asked_roles:
        if role.event_id != event.id:
            raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=f"Роль {role.name} не принадлежит мероприятию {event.name}"
                                )
        if role.age_restriction > 0:
            if volunteer_login.date_of_birth is None:
                raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                                    detail="Вы не указали дату рождения")
            else:
                # TODO check it
                if (date.today() - volunteer_login.date_of_birth).days > event.age_restriction * 365:
                    roles_can_apply.append(role)
        elif role.max_people <= db.query(func.count(event.volunteers)).filter(and_(EventVolunteer.actual_role == role,
                                                                                   EventVolunteer.participation_status == ParticipationStatus.APPROVED)).scalar():
            pass
        else:
            roles_can_apply.append(role)
    if len(roles_can_apply) == 0:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Нет свободных мест или вы не подходите по возрасту к выбранным ролям")
    existing_application = db.query(EventVolunteer).filter(and_(EventVolunteer.volunteer_id == volunteer.id,
                                                                EventVolunteer.event_id == event.id)).first()  # type: EventVolunteer
    if existing_application is not None:
        if existing_application.participation_status == ParticipationStatus.WAITING:
            existing_application.preferable_role1_id = application.preferable_role1_id
            existing_application.preferable_role2_id = application.preferable_role2_id
            existing_application.preferable_role3_id = application.preferable_role3_id
            db.add(existing_application)
            db.commit()
            db.refresh(existing_application)
        else:
            raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Вы ранее подавали заявку на участие в данном мероприятии и уже не можете её изменить")
    else:
        crud.volunteer.apply(db, application=application, volunteer=volunteer, event=event,
                             roles_can_apply=roles_can_apply)

    return OkResponse()


@router.post("/resolve")
def resolve_volunteer(
        db: Session = Depends(get_db),
        organizator: Organizer = Depends(get_current_user),
        *,
        answer: Resolve
):
    application = db.query(EventVolunteer).filter(
        EventVolunteer.id == answer.application_id).first()  # type:EventVolunteer

    if application is None:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Заявки с данным id не существует")

    event = db.query(Event).filter(Event.id == application.event_id).first()  # type:Event
    if event is None:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Мероприятие указанной в заявке не существует")

    event_org = None

    for event_organization in organizator.events:
        if event_organization.event.id == event.id:
            event_org = event_organization.event.id
            break
    if event_org is None:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Вы пытаетесь получить доступ к чужому мероприятию"
                            )

    application.participation_status = answer.answer
    db.add(application)
    db.commit()
    db.refresh(application)
    return OkResponse()
