from app.db.base_class import Base
from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, String, func, Date
from sqlalchemy.orm import backref, relationship


class Partner(Base):
    __tablename__ = 'partners'


