from pydantic import BaseModel, EmailStr, UrlStr, constr, PositiveInt, conint
from datetime import date, datetime
from typing import Optional, List
from app.db_models.models import FoodPreferences, ClothSize, phone_number_regex, ParticipationStatus

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
    id: PositiveInt
    name: str
    surname: str
    email: EmailStr
    company: str
    phone_number: PhoneStr
    social_link: UrlStr
    position: str


# Additional properties stored in DB
class OrganizerInDB(Base):
    name: str
    surname: str
    email: EmailStr
    company: str
    phone_number: PhoneStr
    social_link: UrlStr
    position: str


# Token
class Token(Base):
    access_token: str
    token_type: str


class TokenPayload(Base):
    user_id: PositiveInt = None


# Volunteer
class VolunteerForm(Base):
    vk_id: PositiveInt
    name: str
    surname: str
    date_of_birth: Optional[str]
    photo: UrlStr


class VolunteerFormResponse(Base):
    name: Optional[str]
    surname: Optional[str]
    date_of_birth: Optional[date]
    login_id: Optional[PositiveInt]
    photo: Optional[UrlStr]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    login_id: Optional[int]
    volunteer_id: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[PhoneStr]
    volunteering_experience: Optional[str]
    speciality: Optional[str]
    languages: Optional[List[int]]
    interested_in_projects: Optional[str]
    children_work_experience: Optional[str]
    additional_skills: Optional[str]
    reasons_to_work: Optional[str]
    expectations: Optional[str]
    accept_news: Optional[bool]
    known_by_id: Optional[int]
    food_preferences: Optional[str]
    medical_contradictions: Optional[str]
    cloth_size: Optional[str]


class VolunteerPatch(Base):
    login_id: Optional[int]
    volunteer_id: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[PhoneStr]
    volunteering_experience: Optional[str]
    speciality: Optional[str]
    languages: Optional[List[int]]
    interested_in_projects: Optional[str]
    children_work_experience: Optional[str]
    additional_skills: Optional[str]
    reasons_to_work: Optional[str]
    expectations: Optional[str]
    accept_news: Optional[bool]
    known_by_id: Optional[int]
    food_preferences: Optional[str]
    medical_contradictions: Optional[str]
    cloth_size: Optional[str]


# EventApplication
class EventApplication(Base):
    event_id: PositiveInt
    vk_id: PositiveInt
    need_paper_certificate: bool
    motivation: constr(min_length=5)
    comment: Optional[str]
    preferable_role1_id: Optional[PositiveInt]
    preferable_role2_id: Optional[PositiveInt]
    preferable_role3_id: Optional[PositiveInt]


class EventCreate(Base):
    name: str
    description: str
    start_datetime: datetime
    end_datetime: datetime
    can_apply: Optional[bool] = True
    age_restriction: Optional[PositiveInt] = 0
    importance: conint(ge=0, le=100)


# Partner
class PartnerCreate(Base):
    name: str
    description: Optional[str]
    phone_number: Optional[PhoneStr]
    link: UrlStr


class OkResponse(Base):
    ok: bool = True


class Resolve(Base):
    application_id: int
    answer: str
