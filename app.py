from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField , SelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, URL
import os
import db
import datetime
app = Flask(__name__)

class GameDataForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    release_date = DateField('Release Date', validators=[DataRequired()])
    developer = StringField('Developer', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    genre = SelectMultipleField(u'Genre', choices=[('action', 'Action'), ('adventure', 'Adventure'), ('rpg', 'Role Playing Game')])
    game_description = StringField(
        'Game Description', validators=[DataRequired()])
    trailer = StringField('Trailer', validators=[URL()])
    wikipedia = StringField('Wikipedia', validators=[URL()])
    front_cover = StringField('Front Cover', validators=[URL()])
    back_cover = StringField('Back Cover', validators=[URL()])

@app.route("/")
def home():
    return render_template('home.html', games=db.games.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
