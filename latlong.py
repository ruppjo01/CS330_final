from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, TextField, validators, SubmitField, RadioField, SelectField
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from apiclient.discovery import build
from wtforms_sqlalchemy.orm import model_form

from geopy.geocoders import Nominatim 

geolocator = Nominatim() 

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
app.secret_key = 'development key'

Bootstrap(app)

class hometown(db.Model):
    __tablename__ = 'hometown'
    name_id = db.Column(db.Integer, db.ForeignKey('names.name_id'), primary_key=True)
    town_name = db.Column(db.String)
    state_id = db.Column(db.Integer)

class states(db.Model):
    __tablename__ = 'states'
    state_id = db.Column(db.Integer, db.ForeignKey('hometown.state_id'), primary_key=True)
    state_name = db.Column(db.String)

class hometown2(db.Model):
  __tablename__ = 'hometown2'
  name_id = db.Column(db.Integer, primary_key=True)
  town_name = db.Column(db.String)
  state_id = db.Column(db.Integer)
  latitude = db.Column(db.Float)
  longitude = db.Column(db.Float)

thedata = db.session.query(hometown).join(states).add_columns(hometown.town_name, states.state_name, hometown.name_id, states.state_id)

for therow in thedata: 
  address = str(therow.town_name) + ", " + str(therow.state_name)
  location = geolocator.geocode(address)
  print(location.latitude, location.longitude)
  newstudent = hometown2(name_id=therow.name_id, town_name=therow.town_name, state_id = therow.state_id, latitude = location.latitude, longitude = location.longitude)
  db.session.add(newstudent)

db.session.commit() 