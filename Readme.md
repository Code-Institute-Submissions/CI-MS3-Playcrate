# [PLAYCRATE](https://playcrate.herokuapp.com/)

This is an assignment project for [https://codeinstitute.net/](https://codeinstitute.net/). The project aims to create a mobile-friendly database and collection management app for Playstation 1 games.

Playcrate is community-driven Playstation 1 (PS1) games database and collection management app. Users can add games in the database to their collection to keep track of what games they own. If the game doesn’t exist in the database already users can add the game to the database for others to see and use. Users can also add games to their Playcrate which is their play queue of games they wish to play as well they can add games to their Trophy crate to keep a record of what games they’ve completed. Games can be edited and updated by all users so as well as contributing new games to the database users can help refine other users entries.

## Table of Contents


1.  [UX](#ux)
	*  [Design Choices](#design-choices)
	*  [User Stories](#user-stories)
2.  [Features](#features)
3.  [Wireframes](#wireframes)
4.  [Schema Design](#schema-design)
5.  [Technologies Used](#technologies-used)
	*  [Languages](#languages)
	*  [Libraries](#libraries)
	*  [Tools](#tools)
5.  [Deployment](#deployment)
6.  [Testing](#testing)
7.  [Disclaimer](#disclaimer)


## UX:
### Design choices
Though PS1 databases already exist like [Psxdatacenter](https://psxdatacenter.com/pal_list.html) , [Gamesdatabase.org](https://www.gamesdatabase.org/all_system_games-sony_playstation) , they don’t make browsing for and discovering games visually appealing or mobile friendly. 
<div  align="center">  <img  src="https://i.imgur.com/DdPue9N.jpg"></div>
<div  align="center">  <img  src="https://i.imgur.com/EJ4aVdD.jpg"></div>

[Launchbox](https://gamesdb.launchbox-app.com/platforms/games/47), is much more visually appealing but still doesn’t capture the experience that I was looking for which is the feeling of browsing through a game store shelf or storage box full games, flicking from cover to cover until some box art grabs your attention. 

<div  align="center">  <img  src="https://i.imgur.com/xAayTj3.jpg"></div>

I thought a coverflow UI similar to iTunes would best capture this experience and would also make the site more mobile and touchscreen-friendly.


<div  align="center">  <img  src="https://colly.com/images/uploads/coverflow.jpg"></div>

With the UI style decided I found the [Slider](https://swiperjs.com/) plugin to use a achieve a touch-friendly coverflow. With coverflow being the main focus I decided to keep the UI buttons hidden on the back of the game cover so that the game cover box art is what the user is focusing on when browsing. When the user finds a game that they are interested in they can tap/click on the game cover to rotate it and reveal the options.




### User Stories
1. As a fan and enthusiast of Playstation 1 games, I want to help contribute a database of knowledge on the games of this system so that others may discover and learn and become like-minded fans.
2. As someone new to the Playstation 1 games I would like to discover what games the platform has to offer.
3. As a collector of Playstation 1 games, I would like a way to organise and visualise my collection.
4. As a player with a big collection of games, I would like to make a play queue of games so I can easily decide what to play next.
5. As a completionist, I would like to keep track of all the games in my collection that I have completed.

## Features:
### Implemented
- Create a user account.
- Log in to a user account.
- Add a game to the database.
- Edit and existing game in the database.
- Delete a game from the database.(A user can only delete games that they have added).
- Search for games using text search, with results for a game title, developer name, publisher name or genre.
- Search for games by clicking on tags.
-  Browse all games in the database.
- Browse a user's collection.
- Browse a user's playcrate.
- Browser a user's trophies.
- Add/Remove games to/from a user's collection.
- Add/Remove games to/from a user's playcrate.
- Add/Remove games to/from a user's trophy collection.
- Add new Developers, Publishers and Genres to the database using dynamic option creation and parsing in the add game form.
  - Users are presented with a dropdown multiselect of all the options already in the database, if the option isn't already in the database users can simply type in the new option and press enter. When the form is submitted any new options are added to the database and will show up in the multiselect dropdown the next time the add game form is used.

## Wireframes
Below are wireframes for the site developed in [FluidUI](https://www.fluidui.com/)
-  [Home Page](https://github.com/Kieran-Murray-Code/CI-MS3-Playcrate/blob/master/wireframes/Home-Desktop.JPG)
-  [Browse Page](https://github.com/Kieran-Murray-Code/CI-MS3-Playcrate/blob/master/wireframes/Browse-Desktop.JPG)
-  [Sign Up / Sign In Page](https://github.com/Kieran-Murray-Code/CI-MS3-Playcrate/blob/master/wireframes/Sign-In-Sign-Up-Desktop.JPG)
-   [Add Game Page](https://github.com/Kieran-Murray-Code/CI-MS3-Playcrate/blob/master/wireframes/Add-Game-Desktop.JPG)
-  [View Game Page](https://github.com/Kieran-Murray-Code/CI-MS3-Playcrate/blob/master/wireframes/View-Game-Dektop.JPG)

## Schema Design
#### Games Document
| Name    | Database key | Data Type | Function |
| --- | --- | --- | --- |
|ID | _id | ObjectId | 
|Title | title | String | 
| Release Date | release_date | Date |
| Developer | developer | Array | Stores an array of developer names as Strings
| Publisher | publisher | Array | Stores an array of publishers names as Strings
| Genre | genre | Array | Stores an array of genres as Strings
| Game Description | game_description | String |
| Trailer | trailer | String | URL for the game trailer on Youtube
| Wikipedia | Wikipedia | String |
| Front Cover Image | front_cover | String | URL for the image to be used at the cover art for the game
| Added To The Database By | added_to_the_db_by | String |
| Last Edited By | last_edited_by | String |

#### Users Document
| Name    | Database key | Data Type | Function
| --- | --- | --- | --- |
|ID | _id | ObjectId |
|Username | username | String |
| Password | password | String |
| Collection | collection | Array | Stores the _id numbers of the games in the user's collection
| Playcrate | playcrate | Array | Stores the _id numbers of the games in the users playcrate
| Trophies | trophies | Array | Stores the _id numbers of the games in the user's trophies

#### Developers Document
| Name    | Database key | Data Type |
| --- | ---- | --- |
|ID | _id | ObjectId |
|Name | name | String |

#### Publishers Document
| Name    | Database key | Data Type |
| --- | ---- | --- |
|ID | _id | ObjectId |
|Name | name | String |

#### Genres Document
| Name    | Database key | Data Type |
| --- | ---- | --- |
|ID | _id | ObjectId |
|Name | name | String |

## Technologies Used
### Languages
- [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
- [CSS3](https://developer.mozilla.org/en-US/docs/Archive/CSS3)
- [Javascript](https://www.javascript.com/)
- [Python](https://www.python.org/)
- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)

### Libraries
- [jQuery](https://jquery.com/)
- [Select2](https://select2.org/) - The project uses Select2 for dynamic option creation in multiselect dropdowns.
- [SwiperJS](https://swiperjs.com/) - The project uses Swiper for the coverflow used to browse the games.

### Frameworks
- [Bootstrap 4](https://getbootstrap.com/) - The project used the **Bootstrap 4** for a responsive grid system.
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
	- [Flask_WTF](https://flask-wtf.readthedocs.io/en/stable/) 
	- [Flask_User](https://flask-user.readthedocs.io/en/latest/)
	- [Flask_Mongoengine](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/)

### Platforms
- [MongoDB](https://www.mongodb.com/)
- [GitHub](https://github.com/)
- [Heroku](https://www.heroku.com)

### Tools
-  [Visual Studio Code](https://code.visualstudio.com/) - The project used the **Visual Studio** IDE to develop the website linked with **Github** for version control.
- [Fontawesome](https://fontawesome.com/)
-  [Autoprefixer CSS](https://autoprefixer.github.io/) - The project used the **Autoprefixer CSS** to ensure CSS compatibility with all browsers.
-  [HTML Validator](https://validator.w3.org/) - The project used the **HTML Validator** to validate and find errors in the HTML.
-  [CSS Validator](https://jigsaw.w3.org/css-validator/) -The project used the **CSS Validator** to validate and find errors in the CSS.

## Deployment
#### To deploy a live version of this site using Github the following steps are needed

#### To Deploy to Heroku
1. Generate a requirements.txt using `pip freeze > requirements.txt`
2. Create a new file named Procfile with no file extension, add `web: python app.py` to the file and save.
3. Push the commit and push the requirements.txt and Procfile to the GitHub.
4. In the [Heroku Dashboard](https://dashboard.heroku.com/apps) click on New > Create New App.
5. Give the app a name and select region.
6. Click Create app.
7. Once created in Deploy > Deployment Method select GitHub and connect to the app GitHub repo.
8. In Settings > Config Vars > Reveal Config Vars add PORT, IP, MONGODB_URI, SECRET_KEY and give them their needed values.
9. In Deploy > Manual Deploy select the master branch and click on the Deploy Branch button.

#### To deploy a local version the following steps are required.
1. Git can clone a repository using `$ git clone` https://github.com/User/Repository-To-Clone
2. Use the above command in Git Bash in your IDE such as Visual Studio Code
3. To get the URL for cloning this repository go to [Playcrate Repo](https://github.com/Kieran-Murray-Code/CI-MS3-Playcrate)
4. Click on the Clone or Download button.
5. Copy the link from Clone with the HTTPS section.
6. Use the command in step 1 in Git Bash, add the correct URL and hit enter.
7. You now have a local copy of the repository.
8. Setup a virtual environment with your IDE, eg `python -m venv .venv` in Vs Code.
9. Install required modules using the requirements.txt. using `pip install -r requirements.txt`.
10. Create a .env file and add the following variables to it, PORT, IP, MONGODB_URI, SECRET_KEY and give them their needed values.
11.  Run the app with `python3 app.py`

## Testing
Testing documented is a separate [TESTS](https://github.com/Kieran-Murray-Code/CI-MS3-Playcrate/blob/master/Tests.md) file.

## Disclaimer
This webiste was built for educational purposes only.
