from flask import Flask, render_template, redirect, request, flash
from bson import ObjectId
from collections import namedtuple
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, TextAreaField, BooleanField, IntegerField, PasswordField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, URL
from flask_user import login_required, UserManager, UserMixin, current_user
import os
import datetime
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# Flask-User settings
app.config['USER_APP_NAME'] = "Playcrate"
app.config['USER_ENABLE_EMAIL'] = False      # Disable email authentication
app.config['USER_ENABLE_USERNAME'] = True    # Enable username authentication
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = True

app.config['MONGODB_SETTINGS'] = {
    'db': 'playcrate',
    'host': os.environ.get('MONGODB_URI')
}
# Setup Flask-MongoEngine
db = MongoEngine(app)



# Define Flask_Mongoengine documents.


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
    is_saved_in_db = db.BooleanField(default=False)
    added_to_the_db_by = db.StringField(default='')
    last_edited_by = db.StringField(default='')

    meta = {'indexes': [
        {'fields': ['$title', "$developer", '$publisher', '$genre'],
         'default_language': 'english',
         }
    ]}


class Developers(db.Document):
    name = db.StringField(default='')


class Publishers(db.Document):
    name = db.StringField(default='')


class Genres(db.Document):
    name = db.StringField(default='')

# Flask_User Document


class Users(db.Document, UserMixin):
    active = db.BooleanField(default=True)
    username = db.StringField(default='')
    password = db.StringField()
    roles = db.ListField(db.StringField(), default=[])
    collection = db.ListField(db.StringField(), default=[])
    playcrate = db.ListField(db.StringField(), default=[])
    trophies = db.ListField(db.StringField(), default=[])

# Flask_WTF Forms Setup


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
    is_saved_in_db = BooleanField('Existing Data', default=False)


class SearchDatabaseForm(FlaskForm):
    search_box = StringField('Search', validators=[
                             DataRequired()], render_kw={"placeholder": "Search for Games..."})


# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, Users)

@ app.route("/")
def home():
    search_form = SearchDatabaseForm()
    return render_template('home.html', games=Games.objects, search_form=search_form)


@app.route("/browse/")
def browse():
    search_form = SearchDatabaseForm()
    if current_user.is_active:
        user = current_user
    else:
        user = []
    return render_template('browse.html', games=Games.objects, search_form=search_form, user=user, browsing="main")


@ app.route("/add-game/", methods=('GET', 'POST'))
@login_required
def add_game():
    form = GameDataForm()
    search_form = SearchDatabaseForm()
    if request.method == 'GET':
        # Update form with developer,publisher and genre choices from DB
        update_form_choices(form)
        return render_template('add-game.html', search_form=search_form, form=form, current_user=current_user)
    else:
        update_form_choices(form)
        if form.is_saved_in_db.data == True:
            # Editing an existing game, update game and redirect to view that game.
            add_game_data(form)
            return redirect("/games/"+form.title.data)
        else:  # new entry
            # Check if the new game title is the same as an already existing title in the DB
            for game in Games.objects:
                if form.title.data == game['title']:
                    # Title already exists, return to the form with a warning.
                    return render_template('add-game.html', form=form, title_already_exists=True)

            # No titles match the new entry so add it to the db and redirect to view the game.
            add_game_data(form)
            return redirect("/games/"+form.title.data)


def add_game_data(form):
    form = GameDataForm()
    if request.method == 'POST':
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
                is_saved_in_db=True,
                added_to_the_db_by=current_user.username
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
                                                      is_saved_in_db=True, last_edited_by=current_user.username)
            else:
                game_doc.save()


@ app.route('/games/<game_name>/')
def view_game(game_name):
    search_form = SearchDatabaseForm()
    game_to_view = {}
    for game in Games.objects:
        if game["title"] == game_name:
            game_to_view = game
    if len(game_to_view['trailer']) > 0:
        # Convert Youtube url to an embed
        trailer_url = game_to_view['trailer']
        # &modestbranding=1&autohide=1&showinfo=0&controls=0
        game_to_view['trailer'] = trailer_url.replace("watch?v=", "embed/")
        game_to_view['trailer'] += "?rel=0"

    return render_template('view-game.html', search_form=search_form, game=game_to_view, current_user=current_user)


@ app.route('/edit-game/<game_title>/')
@login_required
def edit_game(game_title):
    game_data_in_db = {}
    for game in Games.objects:
        if game["title"] == game_title:
            game_data_in_db = game
    print(game_data_in_db.id)
    form = GameDataForm(obj=game_data_in_db)
    update_form_choices(form)
    return render_template("add-game.html", form=form)


@app.route('/delete/<game_title>/')
def delete_game(game_title):
    Games.objects(title=game_title).delete()
    return redirect('/')


@app.route('/view-collection/')
@login_required
def view_collection():
    user_collection_all_games = get_user_collection(current_user.collection)
    if current_user.is_active:
        user = current_user
    else:
        user = []
    search_form = SearchDatabaseForm()
    return render_template('browse.html', search_form=search_form, games=user_collection_all_games, user=user, browsing="collection")


@app.route('/view-playcrate/')
@login_required
def view_playcrate():
    search_form = SearchDatabaseForm()
    user_collection_playcrate = get_user_collection(current_user.playcrate)
    if current_user.is_active:
        user = current_user
    else:
        user = []
    search_form = SearchDatabaseForm()
    return render_template('browse.html', search_form=search_form, games=user_collection_playcrate, user=user, browsing="playcrate")


@app.route('/view-trophies/')
@login_required
def view_trophies():
    user_collection_trophies = get_user_collection(current_user.trophies)
    if current_user.is_active:
        user = current_user
    else:
        user = []
    search_form = SearchDatabaseForm()
    return render_template('browse.html', search_form=search_form, games=user_collection_trophies, user=user, browsing="trophies")


def get_user_collection(game_ids):
    user_collection_all_games = []
    for id in game_ids:
        if(Games.objects(id=id)):
            user_game = Games.objects(id=id).first()
            user_collection_all_games.append(user_game)
        else:
            remove_game_from_collection(id)
            del user_collection_game_ids[id]
    return user_collection_all_games


@app.route('/add-game-to-collection/<game_id>')
@login_required
def add_game_to_collection(game_id):
    # Prevent duplicate ids being added to the user collection
    for id in current_user.collection:
        if id == game_id:
            return redirect('/view-collection/')

    Users.objects(id=current_user.id).update(push__collection=game_id)
    return redirect('/view-collection/')


@app.route('/remove-game-from-collection/<game_id>')
@login_required
def remove_game_from_collection(game_id):
    Users.objects(id=current_user.id).update(pull__collection=game_id)
    Users.objects(id=current_user.id).update(pull__playcrate=game_id)
    Users.objects(id=current_user.id).update(pull__trophies=game_id)
    return redirect('/view-collection')


@app.route('/add-game-to-playcrate/<game_id>')
@login_required
def add_game_to_playcrate(game_id):
    for id in current_user.playcrate:
        if id == game_id:
            return redirect('/view-playcrate/')
    Users.objects(id=current_user.id).update(push__playcrate=game_id)
    return redirect('/view-playcrate/')


@app.route('/remove-game-from-playcrate/<game_id>')
@login_required
def remove_game_from_playcrate(game_id):
    Users.objects(id=current_user.id).update(pull__playcrate=game_id)
    return redirect('/view-playcrate/')


@app.route('/add-game-to-trophies/<game_id>')
@login_required
def add_game_to_trophies(game_id):
    # Prevent duplicate ids being added to the user trophies
    for id in current_user.trophies:
        if id == game_id:
            return redirect('/view-trophies/')

    Users.objects(id=current_user.id).update(push__trophies=game_id)
    return redirect('/view-trophies/')


@app.route('/remove-game-from-trophies/<game_id>')
@login_required
def remove_game_from_trophies(game_id):
    Users.objects(id=current_user.id).update(pull__trophies=game_id)
    return redirect('/view-trophies/')


@app.route('/search-db/', methods=['POST'])
def search_db():
    search_form = SearchDatabaseForm()
    search_results = Games.objects.search_text(form.search_box.data).all()
    if current_user.is_active:
        user = current_user
    else:
        user = []
    return render_template('browse.html', games=search_results, search_form=search_form, user=user, browsing="search", search_term=form.search_box.data)


@app.route('/tag-search/<keyword>', methods=['GET', 'POST'])
def search_db_keyword(keyword):
    search_form = SearchDatabaseForm()
    search_results = Games.objects.search_text(keyword).all()
    if current_user.is_active:
        user = current_user
    else:
        user = []
    return render_template('browse.html', games=search_results, search_form=search_form, user=user, browsing="search", search_term=keyword)


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
            port=int(os.environ.get('PORT')))
