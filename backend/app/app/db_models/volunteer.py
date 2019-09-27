from app.db.base_class import Base
from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, String, func, Date
from sqlalchemy.orm import backref, relationship
from .volunteer_tag import volunteer_tag


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
