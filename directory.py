from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, TextField, validators, SubmitField, RadioField, SelectField
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy

from wtforms_sqlalchemy.orm import model_form

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

class StudentSearch(Form):
    options = RadioField('Search By',[validators.DataRequired()],choices=[('Name','Name'),('Major','Major'),('Minor','Minor'),('Res','Luther Residence'),('Hometown','Hometown'),('State','Home State')])
    field = TextField([validators.DataRequired()])

    submit = SubmitField('Search')

@app.route('/', methods=['GET','POST'])
def directory():
    form = StudentSearch()

    if request.method == 'POST':
        if form.validate() == False:
            flash('At least one parameter must be given')
            return render_template('index.html', form = form)
        else:
            if form.options.data == 'Name':
                name = form.field.data.split()
                first_name = name[0]
                last_name = name[1]
                info = db.session.query(names).filter_by(first = first_name).filter_by(last = last_name)
                results = []
                for i in info:
                    results.append(i)


            return render_template('results.html', info = results)
    elif request.method == 'GET':
        return render_template('index.html', form = form)



@app.route('/student_map')
def map():
    return render_template('map.html')

@app.route('/pictures')
def pictures():
    return render_template('pictures.html')

if __name__ == '__main__':
    app.run()
