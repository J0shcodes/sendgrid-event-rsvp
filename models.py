from app import db
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# Events model

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)

# RSVP model

class RSVP(db.Model):
    __tablename__ = 'rsvps'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False) # 'yes', 'no', or 'maybe'
