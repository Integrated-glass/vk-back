from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.db_models.models import Partner, EventPartnerAssociation, Event
from app.models.models import PartnerCreate


def get(db_session: Session, *, user_id: int) -> Optional[Partner]:
    return db_session.query(Partner).filter(Partner.id == user_id)


def create(db_session: Session, *, partner_in: PartnerCreate):
    partner = Partner(**dict(partner_in))
    db_session.add(partner)
    db_session.commit()
    db_session.refresh(partner)
    return partner


def link(
        db_session: Session,
        *,
        event: Event,
        partner: Partner
):
    association = EventPartnerAssociation()
    association.partner = partner
    event.partners.append(association)

    db_session.add(association)
    db_session.add(event)
    db_session.commit()
    db_session.refresh(association)
    db_session.refresh(event)

