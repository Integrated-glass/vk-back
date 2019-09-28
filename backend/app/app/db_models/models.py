import enum
import math

from sqlalchemy import Table, Column, ForeignKey,\
    Date, DateTime, Time, DECIMAL, Text, Enum, Boolean,\
    Integer, String,\
    CheckConstraint
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Organizer(Base):
    __tablename__ = 'organizers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    company = Column(String, nullable=False)
    position = Column(String, nullable=False)
    social_link = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    # invited_by = relationship("Invite")  # , uselist=False, back_populates="invitee", foreign_keys='[invites.id]')

    invites = relationship("Invite", back_populates='issued_by')

    projects = relationship("OrganizerProject", back_populates="organizer")
    events = relationship("OrganizerEvent", back_populates="organizer")


class Invite(Base):
    __tablename__ = 'invites'

    id = Column(Integer, primary_key=True)
    issue_date = Column(DateTime, nullable=False)
    key = Column(String, nullable=False)

    # invitee_id = Column(Integer, ForeignKey('organizers.id'), nullable=True)
    # invitee = relationship("Organizer", back_populates='invited_by', foreign_keys=[invitee_id])

    issued_by_id = Column(Integer, ForeignKey('organizers.id'), nullable=False)
    issued_by = relationship('Organizer', back_populates='invites', foreign_keys=[issued_by_id])


class Partner(Base):
    __tablename__ = 'partners'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    phone = Column(String(length=20), nullable=True)
    link = Column(String, nullable=False)


class QR_data(Base):
    __tablename__ = 'qr_data'

    id = Column(Integer, primary_key=True)
    salt = Column(String, nullable=False)

    event_volunteer_id = Column(Integer, ForeignKey("events_volunteers.id"), nullable=False)
    event_volunteer = relationship("EventVolunteer", back_populates="qr_data", uselist=False)


volunteer_tag = Table(
    'volunteer_tags', Base.metadata,
    Column("volunteer_id", Integer, ForeignKey('volunteers.id'), nullable=False),
    Column('tag_id', Integer, ForeignKey('tags.id'), nullable=False),
)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    volunteers = relationship('Volunteer', secondary=volunteer_tag, back_populates="interests")


class VolunteerLanguageAssociation(Base):
    __tablename__ = 'volunteer_language_associations'

    proficiency = Column(Integer, nullable=False)
    proficiency_check = CheckConstraint('proficiency >= 1 AND proficiency <= 6')
    volunteer_id = Column(Integer, ForeignKey('volunteers.id'), primary_key=True)
    volunteer = relationship('Volunteer', back_populates="languages")

    language_id = Column(Integer, ForeignKey('languages.id'), primary_key=True)
    language = relationship("Language", back_populates='volunteers')


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    volunteers = relationship("VolunteerLanguageAssociation", back_populates='language')


class FoodPreferences(enum.Enum):
    vegetarian = "Vegetarian",
    vegan = 'Vegan',
    halal = 'Halal',
    kosher = 'Kosher',
    nut_allergy = 'Nut Allergy'


class ClothSize(enum.Enum):
    XS = 'XS'
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


class Volunteer(Base):
    __tablename__ = 'volunteers'

    id = Column(Integer, primary_key=True)
    volunteer_id = Column(String, nullable=False, unique=True) #
    vk_id = Column(Integer, nullable=False, unique=True) #
    name = Column(String, nullable=False) #
    surname = Column(String, nullable=False) #
    date_of_birth = Column(Date, nullable=True) #
    karma = Column(DECIMAL, default=0)

    interests = relationship('Tag', secondary=volunteer_tag, back_populates='volunteers')
    # additional from presentation
    email = Column(String, nullable=False, unique=True) #
    phone = Column(String(length=20)) #
    work = Column(String) #
    # специальность по диплому
    food_preferences = Column(Enum(FoodPreferences), nullable=True) ###
    volunteering_experience = Column(Text, nullable=True) #
    interested_in_projects = Column(Text, nullable=True) ## *
    children_work_experience = Column(Text, nullable=True) ## *
    ## additional skills *
    ## why to work with us *
    expectations = Column(Text, nullable=True) ##
    medical_contradictions = Column(Text, nullable=True) ###
    cloth_size = Column(Enum(ClothSize), nullable=False) ### *
    accept_news = Column(Boolean, nullable=False) ##

    ### save photo

    languages = relationship("VolunteerLanguageAssociation", back_populates="volunteer") #
    known_by_id = Column(Integer, ForeignKey("information_sources.id"))
    known_by = relationship("InformationSource", back_populates='volunteers') ## *

    events = relationship("EventVolunteer", back_populates="volunteer")


class InformationSource(Base):
    __tablename__ = 'information_sources'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    volunteers = relationship("Volunteer", back_populates='known_by')


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    name = Column(String, nullable=False)

    max_people = Column(Integer, nullable=False)

    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    event = relationship("Event", back_populates="roles")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    can_apply = Column(Boolean, nullable=False, default=True)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    project = relationship("Project", back_populates="events")

    organizers = relationship("OrganizerEvent", back_populates="event")
    volunteers = relationship("EventVolunteer", back_populates="event")

    @staticmethod
    def calculate_base_karma(context: DefaultExecutionContext):
        return math.ceil(context.get_current_parameters()["importance"] * 0.1)

    importance = Column(Integer, CheckConstraint('importance >= 0 and importance <= 100'), nullable=False)
    base_karma_to_pay = Column(Integer, nullable=False, default=calculate_base_karma, onupdate=calculate_base_karma)

    roles = relationship("Role", back_populates="event")

    schedule_records = relationship("EventSchedule", back_populates="event")


class EventSchedule(Base):
    __tablename__ = "event_schedule"

    id = Column(Integer, primary_key=True)

    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    event = relationship("Event", back_populates="schedule_records")

    date = Column(Date, nullable=False)
    time_begin = Column(Time, nullable=False)
    time_end = Column(Time, nullable=False)

    description = Column(String, nullable=False)


class OrganizerEvent(Base):
    __tablename__ = "organizers_events"

    id = Column(Integer, primary_key=True)

    organizer_id = Column(Integer, ForeignKey("organizers.id"), nullable=False)
    organizer = relationship("Organizer", back_populates="events")

    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    event = relationship("Event", back_populates="organizers")

    todos = relationship("TODO", back_populates="organizer_event")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    organizers = relationship("OrganizerProject", back_populates="project")
    events = relationship("Event", back_populates="project")


class OrganizerProject(Base):
    __tablename__ = "organizers_projects"

    id = Column(Integer, primary_key=True)

    organizer_id = Column(Integer, ForeignKey("organizers.id"), nullable=False)
    organizer = relationship("Organizer", back_populates="projects")

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="organizers")


class ParticipationStatus(enum.Enum):
    APPROVED = "approved"
    WAITING = "waiting"
    KICKED = "kicked"
    DECLINED = "declined"
    PLANNED = "planned"


class EventVolunteer(Base):
    __tablename__ = "events_volunteers"

    id = Column(Integer, primary_key=True)

    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    event = relationship("Event", back_populates="volunteers")

    volunteer_id = Column(Integer, ForeignKey("volunteers.id"), nullable=False)
    volunteer = relationship("Volunteer", back_populates="events")

    qr_data = relationship("QR_data", back_populates="event_volunteer", uselist=False)

    karma_to_pay = Column(Integer, nullable=False)
    need_paper_certificate = Column(Boolean, nullable=False)
    motivation = Column(String, nullable=False)
    comment = Column(String, nullable=True)
    participation_status = Column(Enum(ParticipationStatus), nullable=False)

    actual_role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    preferable_role1_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    preferable_role2_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    preferable_role3_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    actual_role = relationship("Role", foreign_keys=[actual_role_id])
    preferable_role1 = relationship("Role", foreign_keys=[preferable_role1_id])
    preferable_role2 = relationship("Role", foreign_keys=[preferable_role2_id])
    preferable_role3 = relationship("Role", foreign_keys=[preferable_role3_id])


class TODO(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    is_done = Column(Boolean, default=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=True)

    organizer_event_id = Column(Integer, ForeignKey('organizers_events.id'))
    organizer_event = relationship("OrganizerEvent", back_populates='todos')
