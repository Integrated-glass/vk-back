from typing import Optional
from .base import Base


# Shared properties
class OrganizerBase(Base):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None


class OrganizerBaseInDB(OrganizerBase):
    id: int = None


# Properties to receive via API on creation
class OrganizerCreate(OrganizerBaseInDB):
    email: str
    password: str


# Properties to receive via API on update
class OrganizerUpdate(OrganizerBaseInDB):
    password: Optional[str] = None


# Additional properties to return via API
class Organizer(OrganizerBaseInDB):
    pass


# Additional properties stored in DB
class OrganizerInDB(OrganizerBaseInDB):
    hashed_password: str
