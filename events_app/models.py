"""Create database models to represent tables."""
from events_app import db
from sqlalchemy.orm import backref
import enum

class EventType(enum.Enum):
    PARTY = 1
    STUDY = 2
    NETWORKING = 3
    MISC = 4

# TODO: Create a model called `Guest` with the following fields:
# - id: primary key
# - name: String column
# - email: String column
# - phone: String column
# - events_attending: relationship to "Event" table with a secondary table

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    events_attending = db.relationship('Event', secondary='guest_events', back_populates="guests")
    events_hosting = db.relationship('Event', secondary='events_created', back_populates="created_by")

# TODO: Create a model called `Event` with the following fields:
# - id: primary key
# - title: String column
# - description: String column
# - date_and_time: DateTime column
# - guests: relationship to "Guest" table with a secondary table

# STRETCH CHALLENGE: Add a field `event_type` as an Enum column that denotes the
# type of event (Party, Study, Networking, etc)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    date_and_time = db.Column(db.DateTime(timezone=True))
    guests = db.relationship('Guest', secondary = 'guest_events', back_populates="events_attending")
    created_by = db.relationship('Guest', secondary= 'events_created', back_populates="events_hosting")
    event_type = db.Column(db.Enum(EventType), default=EventType.MISC)

# TODO: Create a table `guest_event_table` with the following columns:
# - event_id: Integer column (foreign key)
# - guest_id: Integer column (foreign key)

guest_event_table = db.Table('guest_events',
    db.Column('guest_id', db.Integer, db.ForeignKey('guest.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

guest_event_created_table = db.Table('events_created',
    db.Column('guest_id', db.Integer, db.ForeignKey('guest.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)