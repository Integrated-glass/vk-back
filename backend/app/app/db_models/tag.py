from app.db.base_class import Base
from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, String, func, Date
from sqlalchemy.orm import backref, relationship

from .volunteer_tag import volunteer_tag


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    volunteers = relationship('volunteers', secondary=volunteer_tag, back_populates="interests")
