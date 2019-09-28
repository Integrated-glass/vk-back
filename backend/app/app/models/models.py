from pydantic import BaseModel, EmailStr, UrlStr, constr
from datetime import date
from typing import Optional, List

PhoneNumber = constr(regex=r'^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$')


# Base
class Base(BaseModel):
    class Config:
        orm_mode = True


# Organizer
# Shared properties
class OrganizerBase(Base):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    name: str
    surname: str


class OrganizerBaseInDB(OrganizerBase):
    id: int = None


# Properties to receive via API on creation
class OrganizerCreate(Base):
    name: str
    surname: str
    email: EmailStr
    password: str
    company: str
    phone_number: PhoneNumber
    social_link: UrlStr
    position: str


# Properties to receive via API on update
class OrganizerUpdate(OrganizerBaseInDB):
    password: Optional[str] = None


# Additional properties to return via API
class Organizer(Base):
    id: int
    name: str
    surname: str
    email: EmailStr
    company: str
    phone_number: PhoneNumber
    social_link: UrlStr
    position: str


# Additional properties stored in DB
class OrganizerInDB(OrganizerBaseInDB):
    hashed_password: str


# Token
class Token(Base):
    access_token: str
    token_type: str


class TokenPayload(Base):
    user_id: int = None
