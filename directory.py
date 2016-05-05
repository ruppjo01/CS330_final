from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from wtforms import Form, BooleanField, TextField, validators, SubmitField, RadioField, SelectField
from flask_wtf import Form

app = Flask(__name__)
app.debug = True
app.secret_key = 'development key'

Bootstrap(app)

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
            return render_template('results.html')
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
