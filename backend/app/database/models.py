from sqlalchemy import Column,Integer,String ,DateTime,ForeignKey
from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import UniqueConstraint
from sqlalchemy import Boolean

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        nullable=False,
        default="STUDENT"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    created_events = relationship(
        "Event",
        back_populates="creator"
    )

    registrations = relationship(
        "Registration",
        back_populates="user"
    )

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    capacity = Column(Integer)


    creator_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    event_date = Column(
        DateTime,
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="ACTIVE"
    )

    registration_open = Column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    creator = relationship(
        "User",
        back_populates="created_events"
    )

    registrations = relationship(
        "Registration",
        back_populates="event"
    )

class Registration(Base):
    __tablename__ = "registrations"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "event_id",
            name="unique_registration"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="CONFIRMED"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="registrations"
    )

    event = relationship(
        "Event",
        back_populates="registrations"
    )