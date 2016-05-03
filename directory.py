from flask import Flask, render_template
from flask_bootstrap import Bootstrap
#comment
app = Flask(__name__)
app.debug = True

Bootstrap(app)

@app.route('/')
def directory():
    return render_template('index.html')

@app.route('/student_map')
def map():
    return render_template('map.html')

@app.route('/pictures')
def pictures():
    return render_template('pictures.html')

if __name__ == '__main__':
    app.run()
