from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, URL
import os
import db
import datetime
app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html', games=db.games.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
