from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table, Date, DECIMAL, Text, DateTime
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


class Invite(Base):
    __tablename__ = 'invites'

    id = Column(Integer, primary_key=True)
    issue_date = Column(DateTime, nullable=False)
    key = Column(String, nullable=False)
    activated = Column(Boolean, default=False)

    invitor_id = Column(Integer, ForeignKey('organizers.id'))
    invitor = relationship("Organizer", back_populates='invited_by')

    issued_by_id = Column(Integer, ForeignKey('organizers.id'))
    issued_by = relationship('Organizer', back_populates='invites')


class Partner(Base):
    __tablename__ = 'partners'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    phone = Column(String(length=10), nullable=True)
    link = Column(String, nullable=False)


class QR_data(Base):
    __tablename__ = 'qr_data'

    id = Column(Integer, primary_key=True)
    salt = Column(String, nullable=False)


volunteer_tag = Table(
    'volunteer_tags', Base.metadata,
    Column("volunteer_id", Integer, ForeignKey('volunteers.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    volunteers = relationship('Volunteer', secondary=volunteer_tag, back_populates="interests")


class Volunteer(Base):
    __tablename__ = 'volunteers'
    id = Column(Integer, primary_key=True)
    volunteer_id = Column(String, nullable=False, unique=True)
    vk_id = Column(Integer, nullable=False, unique=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    karma = Column(DECIMAL)

    interests = relationship('Tag', secondary=volunteer_tag, backref='volunteers')


class Role(Base):
    id = Column(Integer, primary_key=True)

    description = Column(String, nullable=False)
    name = Column(String, nullable=False)
