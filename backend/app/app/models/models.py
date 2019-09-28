from pydantic import BaseModel, EmailStr, UrlStr, constr
from datetime import date
from typing import Optional, List
from app.db_models.models import FoodPreferences, ClothSize, phone_number_regex

PhoneStr = constr(regex=phone_number_regex)


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
    phone_number: PhoneStr
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
    phone_number: PhoneStr
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


# Volunteer
class VolunteerForm(Base):
    vk_id: int
    name: str
    surname: str
    date_of_birth: Optional[date]
    photo: UrlStr


class VolunteerFormResponse(VolunteerForm):
    login_id: int


class VolunteerForm1(Base):
    vk_id: int
    volunteer_id: str
    name: str
    surname: str
    date_of_birth: date
    email: EmailStr
    phone_number: PhoneStr
    volunteering_experience: str
    speciality: str
    languages: List[int]


class VolunteerForm2(Base):
    vk_id: int
    interested_in_projects: str
    children_work_experience: str
    additional_skills: str
    reasons_to_work: str
    expectations: Optional[str]
    accept_news: Optional[bool] = True
    known_by_id: int


class VolunteerForm3(Base):
    vk_id: int
    food_preferences: Optional[FoodPreferences]
    medical_contradictions: Optional[str]
    cloth_size: ClothSize
