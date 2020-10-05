Access main [READEME](https://github.com/Kieran-Murray-Code/CI-MS2-Gridcannon/blob/master/README.md) file.

### Manual Testing
-  **Coverflow(Slider)**
	-  On mobile, swiping left and right slides to the next or previous game.
	- On Desktop clicking and dragging in the slider area allows the user to pull the coverflow left and right and move to the game they want to view.
	- The game title and release date update when the slide is changed to a new game.
	- The rotate icon appears on the slide that the users stop on to show the user that the game cover can be flipped over.
	- Clicking/Tapping on the selected game will rotate the cover to reveal the UI options.
	- Clicking/Tapping on any game that is not the selected game does not cause the cover to rotate.
	- When a game is rotated to the back cover UI the slide can not be changed.

-  **Text Search**
	-  Searching for the game title or one of the words in the game title will return all games whose title's match the search term.
	- Searching for a developer name will return all games that were made by that developer.
	- Searching for a publisher name will return all games that were published by that publisher.
	- Searching for a genre will return all games that are in that genre.

-  **Tag Search**
	- When viewing game information, all developer, publisher and genres can be clicked on to search for that keyword.

- **View Game**
	- When browsing games in the coverflow, flip the cover around to the back cover UI and select View to go the selected game's page which displays all the game's information.

 - **Add A Game To A User Collection**
	  - With a user signed in, from the back cover UI on the Browse page select Add to collection, the game will be added to the user's collection and the page will change to view the user's collection.

 - **Remove A Game From A User Collection**
	  - With a user signed in, from the back cover UI on the Browse page of the  My Collection page select Remove from the collection, the game will be removed from the user's collection and the page will change to view the users' collection.

  - **Add A Game To A User Playcrate**
	  - With a user signed in, from the back cover UI on the My Collection page select Add to playcrate, the game will be added to the users playcrate and the page will change to view the users playcrate.

  - **Remove A Game From A User Playcrate**
	  - With a user signed in, from the back cover UI on the  My Collection page or My Playcrate page select Remove from playcrate, the game will be removed from the users playcrate and the page will change to view the users playcrate.

  - **Add A Game To A User Trophies**
	  - With a user signed in, from the back cover UI on the My Collection page select Add to trophies, the game will be added to the user's trophies and the page will change to view the user's trophies.

  - **Remove A Game From A User Trophies**
	  - With a user signed in, from the back cover UI on the  My Collection page or My Trophies page select Remove from trophies, the game will be removed from the user's trophies and the page will change to view the user's trophies.

- **Add A Game Form**
	- 
- **Edit A Game**
		- From the the back cover UI on the Browse or View Game pages select Edit, this will bring up the add game form with all the fields pre populated with the data that already exists in the database for that game.

- **Delete A Game**
	- From the back cover UI on the View Game page if the user is the user that added the game to the database click on the delete button, a modal will appear to confirm the delete and warn them that the action can not be undone.
	- From the back cover UI on the View Game page if the user is not the the user that added the game to the database the then delete option will not appear.

 - **Collection Status Icons**
	 - With a user logged in, the relevant icons show up below a game to indicate if a game is in the users collection, playcrate or trophies.

- **Login Required**
	- With a user logged out, trying to Access the Add Games, Edit Game or My Account pages will result in the Sign In page being displayed.

- **Sign In From**
	- Entering any combination of invalid username or password will result in the in error and no user will be logged in.
	- Clicking on the New here? Register will bring up Sign Up form.

- **Sign Up Form**
	- If the password and the confirm password field do not match an error will occur and the user will not be created.
	- Entering a username of a user that already exists will result in error and the user will not be created, the user is told the username is already in use and is asked to choose a new one.
	- Entering a username that is less than 3 characters will result in error and the user will not be created.
	- Entering a password that is less than 6 characters, that doesn't have at least one number and a least one uppercase and one lowercase letter will result in error and the user will not be created.
	- Clicking on the Already registered? Sign in. will bring up the Sign In form.

### Testing User Stories
- **As a fan and enthusiast of Playstation 1 games, I want to help contribute a database of knowledge on the games of this system so that others may discover and learn and become like-minded fans.**
	- Using the Add Game form I am able to add new games to the database that don't already exist.
	- I can edit and update wrong or incomplete information on games that are already in the database.

- **As someone new to the Playstation 1 games I would like to discover what games the platform has to offer.**
	- Using the Browse page and can scroll through the games that exist in the database and look for games that interest me.
	- When I see a game that I'm interested in I can view more information on the game on it's page.

- **As a collector of Playstation 1 games, I would like a way to organise and visualise my collection.**
	- I can create a user profile, then search or browse for games that I have in my collection and then add them to my collection on my profile.
	- I can go to my collection in my account and quickly browse though my collection using the nice coverflow inferface. This allows my to easily see if I have a game in my collection or find out more information about those games.
	- When a game is my collection the collection icon will appear below it when it is the selected game in the coverflow interface, so I can see if a game is in my collection when browsing or searching without having to go to my collection page.

- **As a player with a big collection of games, I would like to make a play queue of games so I can easily decide what to play next.**
	- Once I have added my games to my collection on my account I can add a game to my playcrate, I can then browse through my playcrate using the coverflow inferface to help decide which game to play next.
	- - When a game is my playcrate the playcrate icon will appear below it when it is the selected game in the coverflow interface, so I can see if a game is in my playcrate when browsing or searching without having to go to my playcrate page.

- **As a completionist, I would like to keep track of all the games in my collection that I have completed.**
	- Once I have added my games to my collection on my account I can add a game that I have completed to my trophies, I can then browse through my playcrate using the coverflow interface to see my achievements and know what games I have completed.
	- When a game is my trophies the trophy icon will appear below it when it is the selected game in the coverflow interface, so I can see if a game is in my trophies when browsing or searching without having to go to my trophies page.

### HTML & CSS Validation

#### HTML
The HTML was put through through [https://validator.w3.org/](https://validator.w3.org/).

The following errors were found and fixed.
 - Empty ID tags
 - Hrefs on divs
 - Attribute  `,`  not allowed on element  [`a`]  at this point.
 - For attribute `href` on element [`a`]: Illegal character in path segment: space is not allowed
-  Empty heading (Ingored as the heading is populated by Javascript)
 - `=` in an unquoted attribute value
 - Attribute  `placeholder`  not allowed on element  [`label`](https://html.spec.whatwg.org/multipage/#the-label-element)  at this point.
#### CSS

  

The following errors were found when running were found when running my **CSS** through [https://jigsaw.w3.org/css-validator/validator](https://jigsaw.w3.org/css-validator/validator)

No errors were found.