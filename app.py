from flask import Flask, render_template, redirect, request
from bson import ObjectId
from collections import namedtuple
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, BooleanField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, URL
import os
import db
import datetime
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


class GameData:
    def __init__(self, doc_id, title, release_date, developer, publisher, genre, game_description, trailer, wikipedia, front_cover, back_cover,data_exists_in_db):
        self.doc_id = doc_id
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
        self.data_exists_in_db = data_exists_in_db


class GameDataForm(FlaskForm):
    doc_id = StringField()
    title = StringField('Title', validators=[DataRequired()])
    release_date = DateField('Release Date', validators=[DataRequired()])
    developer = SelectMultipleField(
        u'Developer', choices=[])
    publisher = SelectMultipleField(u'Publisher', choices=[])
    genre = SelectMultipleField(u'Genre', choices=[])
    game_description = TextAreaField(
        'Game Description', validators=[DataRequired()])
    trailer = StringField('Trailer', validators=[URL()])
    wikipedia = StringField('Wikipedia', validators=[URL()])
    front_cover = StringField('Front Cover', validators=[URL()])
    back_cover = StringField('Back Cover', validators=[URL()])
    data_exists_in_db = BooleanField('Existing Data', default=False)


@ app.route("/")
def home():
    return render_template('home.html', games=db.games.find())


@ app.route("/add-game/")
def add_game():
    form = GameDataForm()
    if request.method == 'GET':
        # Update form with developer,publisher and genre choices from DB
        update_form_choices(form)
    return render_template('add-game.html', form=form)

@ app.route("/add-game-data/", methods=('GET', 'POST'))
def add_game_data():
    form = GameDataForm()

    if request.method == 'POST':
        # Check if the game title already exists in the DB, if it already exists it can not be added to the DB,
        # return to the form

        # Check if the developer, publisher and genre submitted are new and not already in the relevant lists in the DB.
        # If they're new then add them to the corresponding lists in the DB and update the possible choices in the form for validation.
        submitted_developers = form.developer.data
        # Find all the developer names in the DB and add to a list so the can be compared to the form submitted developers
        developers_in_db = []
        for developer in db.developers.find():
            developers_in_db.append(developer['name'])
        # Find the differences between the developers in the DB and the
        # submitted developers, the differences are returned, these are the new
        # user created developers that need to added to the DB for future entries.
        new_developers = difference_between_string_lists(
            submitted_developers, developers_in_db)
        # Create a document for the new developers and insert it into the DB.
        for new_developer in new_developers:
            developer_doc = {'name': new_developer}
            db.developers.insert_one(developer_doc)
        # Append the form choices with the new user created developers for form validation.
        form.developer.choices.append(new_developers)

        # Update Publishers
        submitted_publishers = form.publisher.data
        publishers_in_db = []
        for publisher in db.publishers.find():
            publishers_in_db.append(publisher['name'])
        new_publishers = difference_between_string_lists(
            submitted_publishers, publishers_in_db)
        for new_publisher in new_publishers:
            publisher_doc = {'name': new_publisher}
            db.publishers.insert_one(publisher_doc)
        form.publisher.choices.append(new_publishers)

        # Update Genres
        submitted_genres = form.genre.data
        genres_in_db = []
        for genre in db.genres.find():
            genres_in_db.append(genre['name'])
        new_genres = difference_between_string_lists(
            submitted_genres, genres_in_db)
        for new_genre in new_genres:
            genre_doc = {'name': new_genre}
            db.genres.insert_one(genre_doc)
        form.genre.choices.append(new_genres)
        if form.validate:
            doc_id = form.doc_id.data
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
                         'back_cover': back_cover, }
            # Check if the submitted form is data edited from an existing game in the DB if it is then update the
            # data for that game if not then add the new game to the DB
            if form.data_exists_in_db.data == True:
                    print("Updating Existing Data")
                    query = {"_id" : ObjectId(doc_id) }
                    db.games.replace_one(query, game_data)
            else:
                print("Adding New Data")
                db.games.insert_one(game_data)
            
            return redirect("/")
    return redirect("/")


@ app.route('/games/<game_name>')
def view_game(game_name):
    game_to_view = {}
    for game in db.games.find():
        if game["title"] == game_name:
            game_to_view = game

    return render_template('view-game.html', game=game_to_view)


@ app.route('/edit-game/<game_title>')
def edit_game(game_title):
    game_data_in_db = {}
    for game in db.games.find():
        if game["title"] == game_title:
            game_data_in_db = game
    game_data = GameData(
        doc_id=game_data_in_db['_id'],
        title=game_data_in_db['title'],
        release_date=game_data_in_db['release_date'],
        developer=game_data_in_db['developer'],
        publisher=game_data_in_db['publisher'],
        genre = game_data_in_db['genre'],
        game_description=game_data_in_db['game_description'],
        trailer=game_data_in_db['trailer'],
        wikipedia=game_data_in_db['wikipedia'],
        front_cover=game_data_in_db['front_cover'],
        back_cover=game_data_in_db['back_cover'],
        data_exists_in_db = True
    )
    form = GameDataForm(obj=game_data)
    update_form_choices(form)
    return render_template("add-game.html", form=form)


@app.route('/delete/<game_id>')
def delete_game(game_id):
    db.games.remove({'_id': ObjectId(game_id)})
    return redirect('/')

def update_form_choices(form):
        for developer in db.developers.find():
            form.developer.choices.append(
                (developer['name'], developer['name']))
        for publisher in db.publishers.find():
            form.publisher.choices.append(
                (publisher['name'], publisher['name']))
        for genre in db.genres.find():
            form.genre.choices.append((genre['name'], genre['name']))

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


def difference_between_string_lists(list_01, list_02):
    return list(set(list_01) - set(list_02))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
