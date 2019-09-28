from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.db_models.models import Organizer
from app.models.models import OrganizerCreate, OrganizerUpdate


# def apply