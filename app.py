from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, URL
import os
import db
import datetime
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

class GameData:
    def __init__(self, title, release_date, developer, publisher, genre, game_description, trailer, wikipedia, front_cover, back_cover):
        self.title = title
        self.release_date = release_date
        self.developer = developer
        self.publisher = publisher
        self.genre = genre
        self.game_description = game_description
        self.trailer = trailer
        self.wikipedia = wikipedia
        self.front_cover = front_cover
        self.back_cover = back_cover

class GameDataForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    release_date = DateField('Release Date', validators=[DataRequired()])
    developer = SelectMultipleField(
        u'Developer', choices=[('core', 'Core'), ('square', 'Square')])
    publisher = SelectMultipleField(u'Publisher', choices=[(
        'eidos', 'Eidos'), ('sony', 'Sony Computer Entertainment')])
    genre = SelectMultipleField(u'Genre', choices=[(
        'action', 'Action'), ('adventure', 'Adventure'), ('rpg', 'Role Playing Game')])
    game_description = TextAreaField(
        'Game Description', validators=[DataRequired()])
    trailer = StringField('Trailer', validators=[URL()])
    wikipedia = StringField('Wikipedia', validators=[URL()])
    front_cover = StringField('Front Cover', validators=[URL()])
    back_cover = StringField('Back Cover', validators=[URL()])


@app.route("/")
def home():
    return render_template('home.html', games=db.games.find())


@app.route("/add-game/")
def add_game():
    form = GameDataForm()
    return render_template('add-game.html', form=form)


@app.route("/update-game-data/", methods=('GET', 'POST'))
def update_game_data():
    form = GameDataForm()
    if form.validate_on_submit():
        return redirect("/")

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
