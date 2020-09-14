from flask import Flask, render_template, redirect, request
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


developer_choices = [('core', 'Core'), ('square', 'Square')]


class GameDataForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    release_date = DateField('Release Date', validators=[DataRequired()])
    developer = SelectMultipleField(
        u'Developer', choices=developer_choices)
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


@app.route("/add-game-data/", methods=('GET', 'POST'))
def add_game_data():
    form = GameDataForm()

    if request.method == 'POST':
        new_developer = form.developer.data
        form.developer.choices.append(new_developer)

        if form.validate:
            title = form.title.data
            release_date = datetime.datetime.combine(
                form.release_date.data, datetime.time.min)
            developer = form.developer.data
            publisher = form.publisher.data
            genre = form.genre.data
            game_description = form.game_description.data
            trailer = form.trailer.data
            wikipedia = form.wikipedia.data
            front_cover = form.front_cover.data
            back_cover = form.back_cover.data

            game_data = {'title': title,
                         'release_date': release_date,
                         'developer': developer,
                         'publisher': publisher,
                         'genre': genre,
                         'game_description': game_description,
                         'trailer': trailer,
                         'wikipedia': wikipedia,
                         'front_cover': front_cover,
                         'back_cover': back_cover}

            db.games.insert_one(game_data)
            return redirect("/")
    return redirect("/")


@app.route("/update-game-data/", methods=('GET', 'POST'))
def update_game_data():
    form = GameDataForm()
    if form.validate_on_submit():
        # db.games.find_one_and_update({'title': form.title.data},
        #                               {"$set": {
        #                                   'title': form.title.data,
        #                                   'release_date': datetime.datetime.combine(
        #                                       form.release_date.data, datetime.time.min),
        #                                   'game_description': form.game_description.data,
        #                                   'front_cover': form.front_cover.data,
        #                                   'back_cover': form.back_cover.data,
        #                               }})
        return redirect("/")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
