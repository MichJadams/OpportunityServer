from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database.schemas import ApplicationStatus

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    opportunities = relationship("Opportunity", back_populates="user")


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    role_description = Column(String)
    notes = Column(String)
    title = Column(String)
    date_applied = Column(DateTime)
    application_status = Column(Enum(ApplicationStatus) )
    user_name = Column(String, ForeignKey("users.name"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    user = relationship("User", back_populates="opportunities")