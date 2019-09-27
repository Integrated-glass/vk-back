import enum

from sqlalchemy import Boolean, Column, Integer, String, \
    ForeignKey, Table, Date, DECIMAL, Text, DateTime, Enum, CheckConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Organizer(Base):
    __tablename__ = 'organizers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    bio = Column(Text, nullable=True)
    company = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

    invited_by = relationship("Invite", uselist=False, back_populates="invitor")

    invites = relationship("Invite", back_populates='issued_by')

    projects = relationship("OrganizerProject", back_populates="organizer")
    events = relationship("OrganizerEvent", back_populates="organizer")


class Invite(Base):
    __tablename__ = 'invites'

    id = Column(Integer, primary_key=True)
    issue_date = Column(DateTime, nullable=False)
    key = Column(String, nullable=False)
    activated = Column(Boolean, default=False)

    invitor_id = Column(Integer, ForeignKey('organizers.id'), nullable=True)
    invitor = relationship("Organizer", back_populates='invited_by', foreign_keys=[invitor_id])

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
    volunteer_id = Column(String, nullable=False, unique=True)
    vk_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    karma = Column(DECIMAL, default=0)

    interests = relationship('Tag', secondary=volunteer_tag, back_populates='volunteers')
    # additional from presentation
    email = Column(String, nullable=False, unique=True)
    phone = Column(String(length=20))
    work = Column(String)
    food_preferences = Column(Enum(FoodPreferences), nullable=True)
    volunteering_experience = Column(Text, nullable=True)
    interested_in_projects = Column(Text, nullable=True)
    children_work_experience = Column(Text, nullable=True)
    expectations = Column(Text, nullable=True)
    medical_contradictions = Column(Text, nullable=True)
    cloth_size = Column(Enum(ClothSize), nullable=False)
    accept_news = Column(Boolean, nullable=False)

    languages = relationship("VolunteerLanguageAssociation", back_populates="volunteer")
    known_by_id = Column(Integer, ForeignKey("information_sources.id"))
    known_by = relationship("InformationSource", back_populates='volunteers')


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


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    base_karma_to_pay = Column(Integer, nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    project = relationship("Project", back_populates="events")

    organizers = relationship("OrganizerEvent", back_populates="event")


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
    organizer = relationship("Organizer", back_populates="events")

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="organizers")


class TODO(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    is_done = Column(Boolean, default=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=True)

    organizer_event_id = Column(Integer, ForeignKey('organizers_events.id'))
    organizer_event = relationship("OrganizerEvent", back_populates='todos')
