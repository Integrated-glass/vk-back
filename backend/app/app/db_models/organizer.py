from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Organizer(Base):
    __tablename__ = 'organizers'
    pass
