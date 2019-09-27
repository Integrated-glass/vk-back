from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table, Date, DECIMAL
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Organizer(Base):
  __tablename__ = 'organizers'

class Partner(Base):
  __tablename__ = 'partners'

class QR_data(Base):
  __tablename__ = 'qrs_data'

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

  volunteers = relationship('volunteers', secondary=volunteer_tag, back_populates="interests")

class Volunteer(Base):
  __tablename__ = 'volunteers'
  id = Column(Integer, primary_key=True)
  volunteer_id = Column(String, nullable=False, unique=True)
  vk_id = Column(Integer, nullable=False, unique=True)
  name = Column(String, nullable=False)
  surname = Column(String, nullable=False)
  date_of_birth = Column(Date, nullable=True)
  karma = Column(DECIMAL)

  interests = relationship('tags', secondary=volunteer_tag, backref='volunteers')

