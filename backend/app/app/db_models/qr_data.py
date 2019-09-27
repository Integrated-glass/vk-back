from app.db.base_class import Base
from sqlalchemy import Column, DECIMAL, ForeignKey, Integer, String, func, Date
from sqlalchemy.orm import backref, relationship


class QR_data(Base):
    __tablename__='qrs_data'

    id = Column(Integer, primary_key=True)
    salt = Column(String, nullable=False)