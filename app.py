from flask import Flask, render_template, redirect, request, flash
from bson import ObjectId
from collections import namedtuple
from flask_mongoengine import MongoEngine
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, BooleanField, IntegerField, PasswordField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, URL
from flask_user import login_required, UserManager, UserMixin, current_user
import os
import db
import datetime
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
# Flask-User settings
# Shown in and email templates and page footers
app.config['USER_APP_NAME'] = "Playcrate"
app.config['USER_ENABLE_EMAIL'] = False      # Disable email authentication
app.config['USER_ENABLE_USERNAME'] = True    # Enable username authentication
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = False    # Simplify register form


app.config['MONGODB_SETTINGS'] = {
    'db': 'playcrate',
    'host': os.environ.get('MONGODB_URI')
}

# Setup Flask-MongoEngine
db = MongoEngine(app)

# User Document
class Users(db.Document, UserMixin):
    active = db.BooleanField(default=True)
    username = db.StringField(default='')
    password = db.StringField()
    roles = db.ListField(db.StringField(), default=[])
    collection = db.ListField(db.StringField(), default=[])
    playcrate = db.ListField(db.StringField(), default=[])


# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, Users)


class Games(db.Document):
    title = db.StringField(default='')
    release_date = db.DateField()
    developer = db.ListField(db.StringField(), default=[])
    publisher = db.ListField(db.StringField(), default=[])
    genre = db.ListField(db.StringField(), default=[])
    game_description = db.StringField(default='')
    trailer = db.StringField(default='')
    wikipedia = db.StringField(default='')
    front_cover = db.StringField(default='')
    back_cover = db.StringField(default='')
    is_saved_in_db = db.BooleanField(default=False)


class Developers(db.Document):
    name = db.StringField(default='')


class Publishers(db.Document):
    name = db.StringField(default='')


class Genres(db.Document):
    name = db.StringField(default='')


class GameDataForm(FlaskForm):
    id = StringField()
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
    is_saved_in_db = BooleanField('Existing Data', default=False)


@ app.route("/")
def home():
    return render_template('home.html', games=Games.objects)


@ app.route("/add-game/", methods=('GET', 'POST'))
@login_required
def add_game():
    form = GameDataForm()
    if request.method == 'GET':
        # Update form with developer,publisher and genre choices from DB
        update_form_choices(form)
        return render_template('add-game.html', form=form, current_user=current_user)
    else:
        update_form_choices(form)
        print(form.is_saved_in_db.data)
        if form.is_saved_in_db.data == True:
            print("Editing Existing Data")
            add_game_data(form)
            return redirect("/")
        else:
            form.is_saved_in_db.data = False
            for game in Games.objects:
                if form.title.data == game['title']:
                    print("Game Already Exists In DB")
                    title_exists_in_db = True

            if(form.is_saved_in_db.data == False):
                add_game_data(form)
                return redirect("/")
            else:
                return render_template('add-game.html', form=form, is_saved_in_db=form.is_saved_in_db.data)


def add_game_data(form):
    form = GameDataForm()

    if request.method == 'POST':
        # Check if the game title already exists in the DB, if it already exists it can not be added to the DB,
        # return to the form

        # Check if the developer, publisher and genre submitted are new and not already in the relevant lists in the DB.
        # If they're new then add them to the corresponding lists in the DB and update the possible choices in the form for validation.
        submitted_developers = form.developer.data
        # Find all the developer names in the DB and add to a list so the can be compared to the form submitted developers
        developers_in_db = []
        for developer in Developers.objects:
            developers_in_db.append(developer['name'])
        # Find the differences between the developers in the DB and the
        # submitted developers, the differences are returned, these are the new
        # user created developers that need to added to the DB for future entries.
        new_developers = difference_between_string_lists(
            submitted_developers, developers_in_db)
        # Create a document for the new developers and insert it into the DB.
        for new_developer in new_developers:
            developer_doc = Developers(name=new_developer)
            developer_doc.save()
        # Append the form choices with the new user created developers for form validation.
        form.developer.choices.append(new_developers)

        # Update Publishers
        submitted_publishers = form.publisher.data
        publishers_in_db = []
        for publisher in Publishers.objects:
            publishers_in_db.append(publisher['name'])
        new_publishers = difference_between_string_lists(
            submitted_publishers, publishers_in_db)
        for new_publisher in new_publishers:
            publisher_doc = Publishers(name=new_publisher)
            publisher_doc.save()
        form.publisher.choices.append(new_publishers)

        # Update Genres
        submitted_genres = form.genre.data
        genres_in_db = []
        for genre in Genres.objects:
            genres_in_db.append(genre['name'])
        new_genres = difference_between_string_lists(
            submitted_genres, genres_in_db)
        for new_genre in new_genres:
            genre_doc = Genres(name=new_genre)
            genre_doc.save()
        form.genre.choices.append(new_genres)

        if form.validate:
            game_doc = Games(
                title=form.title.data,
                release_date=form.release_date.data,
                developer=form.developer.data,
                publisher=form.publisher.data,
                genre=form.genre.data,
                game_description=form.game_description.data,
                trailer=form.trailer.data,
                wikipedia=form.wikipedia.data,
                front_cover=form.front_cover.data,
                back_cover=form.back_cover.data,
                is_saved_in_db=True
            )

            # Check if the submitted form is data edited from an existing game in the DB if it is then update the
            # data for that game if not then add the new game to the DB
            if form.is_saved_in_db.data == True:                
                Games.objects(id=form.id.data).update(title=form.title.data,
                                 release_date=form.release_date.data,
                                 developer=form.developer.data,
                                 publisher=form.publisher.data,
                                 genre=form.genre.data,
                                 game_description=form.game_description.data,
                                 trailer=form.trailer.data,
                                 wikipedia=form.wikipedia.data,
                                 front_cover=form.front_cover.data,
                                 back_cover=form.back_cover.data,
                                 is_saved_in_db=True)
            else:
                print("Adding New Data")
                game_doc.save()


@ app.route('/games/<game_name>/')
def view_game(game_name):
    game_to_view = {}
    for game in Games.objects:
        if game["title"] == game_name:
            game_to_view = game
    # Convert Youtube url to an embed
    trailer_url = game_to_view['trailer']
    # &modestbranding=1&autohide=1&showinfo=0&controls=0
    game_to_view['trailer'] = trailer_url.replace("watch?v=", "embed/")
    game_to_view['trailer'] += "?rel=0"
    return render_template('view-game.html', game=game_to_view)


@ app.route('/edit-game/<game_title>/')
@login_required
def edit_game(game_title):
    game_data_in_db = {}
    for game in Games.objects:
        if game["title"] == game_title:
            game_data_in_db = game
    print(game_data_in_db.id)
    form = GameDataForm(obj=game_data_in_db)  # obj=game_data
    update_form_choices(form)
    return render_template("add-game.html", form=form)


@app.route('/delete/<game_title>/')
def delete_game(game_title):
    Games.objects(title=game_title).delete()
    return redirect('/')

@app.route('/my-account/')
@login_required
def my_account():
    user_collection_game_ids = current_user.collection
    user_collection_games = {}
    for id in user_collection_game_ids:
        user_collection_games[id] = Games.objects(id=id)
        print(user_collection_games[id][0]['title'])
    
    return render_template('my-account.html', user_collection_games=user_collection_games, user_collection_game_ids=user_collection_game_ids)

@app.route('/add-game-to-collection/<game_id>')
def add_game_to_collection(game_id):
        Users.objects(id=current_user.id).update(push__collection=game_id)
        return redirect('/')

@app.route('/remove-game-from-collection/<game_id>')
def remove_game_from_collection(game_id):
        Users.objects(id=current_user.id).update(pull__collection=game_id)
        return redirect('/')

@app.route('/add-game-to-playcrate/<game_id>')
def add_game_to_playcrate(game_id):
        Users.objects(id=current_user.id).update(push__playcrate=game_id)
        return redirect('/')

@app.route('/remove-game-from-playcrate/<game_id>')
def remove_game_from_playcrate(game_id):
        Users.objects(id=current_user.id).update(pull__playcrate=game_id)
        return redirect('/')

def update_form_choices(form):
    for developer in Developers.objects:
        form.developer.choices.append(
            (developer['name'], developer['name']))
    for publisher in Publishers.objects:
        form.publisher.choices.append(
            (publisher['name'], publisher['name']))
    for genre in Genres.objects:
        form.genre.choices.append((genre['name'], genre['name']))


# https://stackoverflow.com/questions/3462143/get-difference-between-two-lists
def difference_between_string_lists(list_01, list_02):
    return list(set(list_01) - set(list_02))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
