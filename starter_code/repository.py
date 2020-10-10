from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ARRAY, ForeignKey
db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(ARRAY(String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.String(120))
    description = db.Column(db.String(500))
    
class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    email = db.Column(db.String)
    genres = db.Column(ARRAY(String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    website =  db.Column(db.String(500))
    seeking_venue = db.Column(db.String(120))
    description = db.Column(db.String(500))

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column( db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    venue_id = db.Column( db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    time = db.Column(db.DateTime)

