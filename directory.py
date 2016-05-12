from flask import Flask, render_template, request, flash, jsonify
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, TextField, validators, SubmitField, RadioField, SelectField
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
app.secret_key = 'development key'



Bootstrap(app)



class names(db.Model):
    __tablename__ = 'names'
    name_id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String)
    last = db.Column(db.String)

class states(db.Model):
    __tablename__ = 'states'
    state_id = db.Column(db.Integer, db.ForeignKey('hometown.state_id'), primary_key=True)
    state_name = db.Column(db.String)

class hometown(db.Model):
    __tablename__ = 'hometown'
    name_id = db.Column(db.Integer, db.ForeignKey('names.name_id'), primary_key=True)
    town_name = db.Column(db.String)
    state_id = db.Column(db.Integer)

class studies(db.Model):
    __tablename__ = 'studies'
    db.ForeignKey('person.id')
    name_id = db.Column(db.Integer, db.ForeignKey('names.name_id'), primary_key=True)
    major = db.Column(db.String)
    minor = db.Column(db.String)
    major2 = db.Column(db.String)

class classes(db.Model):
    __tablename__ = 'classes'
    name_id = db.Column(db.Integer, db.ForeignKey('names.name_id'), primary_key=True)
    standing = db.Column(db.String)

class contact(db.Model):
    __tablename__ = 'contact'
    name_id = db.Column(db.Integer, db.ForeignKey('names.name_id'), primary_key=True,)
    building = db.Column(db.String)
    room = db.Column(db.Integer)
    spo = db.Column(db.Integer)



class StudentSearch(Form):
    options = RadioField('Search By',[validators.DataRequired()],choices=[('Name','Name'),('Major','Major'),('Minor','Minor'),('Res','Luther Residence'),('Hometown','Hometown'),('State','Home State')])
    field = TextField([validators.DataRequired()])

    submit = SubmitField('Search')

class hometown2(db.Model):
  __tablename__ = 'hometown2'
  name_id = db.Column(db.Integer, db.ForeignKey('names.name_id'), primary_key=True)
  town_name = db.Column(db.String)
  state_id = db.Column(db.Integer)
  latitude = db.Column(db.Float)
  longitude = db.Column(db.Float)


@app.route('/', methods=['GET','POST'])
def directory():
    form = StudentSearch()

    if request.method == 'POST':
        if form.validate() == False:
            flash('At least one parameter must be given')
            return render_template('index.html', form = form)
        else:
            options = form.options.data
            if form.options.data == 'Name':
                name = form.field.data.split()
                first_name = name[0]
                if len(name) == 2:
                    last_name = name[1]

                    results = db.session.query(names).filter_by(first = first_name).filter_by(last = last_name)
                else:
                    results = db.session.query(names).filter((names.first == first_name) | (names.last == first_name))
                info = results.join(hometown).add_columns(names.first, names.last, hometown.town_name).join(classes).join(states).join(contact).join(studies)\
                    .add_columns(names.name_id, hometown.town_name, hometown.state_id, classes.standing, states.state_id, states.state_name, contact.building, contact.room, studies.major, studies.minor, studies.major2)
               
                
            elif form.options.data == 'Res':
                housing = form.field.data.split()
                building = housing[0]
                if len(housing) == 2:
                    room = housing[1]
                    results = db.session.query(contact).filter_by(building = building).filter_by(room = room)
                else:
                    results = db.session.query(contact).filter_by(building = building)

                info = results.join(names).add_columns(names.first, names.last, contact.building, contact.room)

            elif form.options.data == 'Major':
                major = form.field.data
                results = db.session.query(studies).filter((studies.major == major) | (studies.major2 == major))
                info = results.join(names).join(classes).add_columns(classes.standing, names.first, names.last, studies.major, studies.major2)

            elif form.options.data == 'Minor':
                minor = form.field.data
                results = db.session.query(studies).filter_by(minor = minor)
                info = results.join(names).add_columns(names.first, names.last, studies.minor)

            elif form.options.data == 'Hometown':
                town = form.field.data
                results = db.session.query(hometown).filter_by(town_name = town)
                info = results.join(names).join(states).join(classes).add_columns(classes.standing, names.first, names.last, hometown.town_name, states.state_name)

            elif form.options.data == 'State':
                state = form.field.data
                results = db.session.query(states).filter_by(state_name = state)

                info = results.join(hometown).join(names).add_columns(names.first, names.last, hometown.town_name, states.state_name)

            print("THIS IS THE INFO", info)
            return render_template('results.html', info = info, option = options)

    elif request.method == 'GET':
        return render_template('index.html', form = form)

@app.route('/student_map')
def map():
    return render_template('map.html')

@app.route('/markers')
def mapinit():
    data = db.session.query(hometown2).join(names).add_columns(names.first, names.last, hometown2.latitude, hometown2.longitude)
    json_list = []

    for row in data:
        first = row.first
        last = row.last
        lat = row.latitude
        lon = row.longitude
        json_list.append(dict(first = first, last = last, lat= lat, lon = lon))
    
    #print(json_list)

    return jsonify(json_obj=json_list)

@app.route('/pictures')
def pictures():
    return render_template('pictures.html')

if __name__ == '__main__':
    app.run()
