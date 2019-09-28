from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.db_models.models import Organizer
from app.models.models import OrganizerCreate, OrganizerUpdate


def get(db_session: Session, *, user_id: int) -> Optional[Organizer]:
    return db_session.query(Organizer).filter(Organizer.id == user_id).first()


def get_by_email(db_session: Session, *, email: str) -> Optional[Organizer]:
    return db_session.query(Organizer).filter(Organizer.email == email).first()


def authenticate(db_session: Session, *, email: str, password: str) -> Optional[Organizer]:
    user = get_by_email(db_session, email=email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def get_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[Organizer]]:
    return db_session.query(Organizer).offset(skip).limit(limit).all()


def create(db_session: Session, *, user_in: OrganizerCreate) -> Organizer:
    data = dict(user_in)
    data['password_hash'] = get_password_hash(data['password'])
    del data['password']
    user = Organizer(
        **data
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def update(db_session: Session, *, user: Organizer, user_in: OrganizerUpdate) -> Organizer:
    user_data = jsonable_encoder(user)
    update_data = user_in.dict(skip_defaults=True)
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])
    if user_in.password:
        passwordhash = get_password_hash(user_in.password)
        user.hashed_password = passwordhash
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
