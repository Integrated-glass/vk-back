from app.db.base_class import Base
from sqlalchemy import Table, Column, DECIMAL, ForeignKey, Integer, String, func, Date
from sqlalchemy.orm import backref, relationship

volunteer_tag = Table('volunteer_tags', Base.metadata,
                      Column("volunteer_id", Integer, ForeignKey('volunteers.id')),
                      Column('tag_id', Integer, ForeignKey('tags.id')),
                      )
