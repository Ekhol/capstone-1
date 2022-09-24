# Back-Pocket Cocktails
## A Resource for Bartenders and Cocktail Enthusiasts

### Note: This app is designed for mobile devices.
### https://back-pocket-cocktails.herokuapp.com/

Back-Pocket Cocktails is a resource for bartenders on the job in order to have an efficient means of storing personal cocktail recipes, finding public recipes, and accessing them on the fly. It is designed to be used on the job when you need to find a recipe but can't spend time weeding through searches or unorganized shared folders.

Test account:

- Username: testing
- Password: testing

## Code:

All of the work so far has been entirely in Python and HTML using Flask, WTForms, SQLAlchemy, and Jinja2. A postgres server is the basis for the user back-end while the CDB API is much of the basis for users that are not logged in. Bootstrap is used for the CSS in-line of the HTML so there are no separate CSS files. 

## Preliminary API Selection:

API selected: https://www.thecocktaildb.com/api.php

Database Selection:

- CocktailDB (CDB) API will be the backbone of the public access, while the postgres database will store user information and the private cocktails. 

## User Flow:

### Public View

Public view will be the data accessible by users who are not logged in or do not have an account. It will provide the information pulled from the cocktaildb as well as data from drinks that authorized users have deemed public. 

- Homepage: displays one CDB drink using their random API method. The NavBar displays limited options when not logged in: Home, User Recipes, CDB Recipes, and Login. Users are able to view all CDB recipes through a name search function within the CDB Recipes tab, as well as all public user recipes through the User Recipes tab and search.
  
  - User Recipes: displays all public user recipes in order of creation. There is a link to a search function that searches approximate names of user recipes using the '.ilike' SQLAlchemy operator.
  - CDB Recipes: returns a search form that uses approximate searching provided by the API search by name function.
  - Login: takes user to the login form with an option to register for an account.

- When viewing recipe details, the cards display a photograph (or default image), the name of the recipe, ingredients, glass type, instructions, and whether or not it is alcoholic.

### Authorized User View

Authorized user view will be accessible by users who have created an account and are logged in. The NavBar is updated to remove the Login button and add an Account route, Pinned route, and Log out.

- Homepage: functions the same as the public view aside from the updated NavBar.
  - Account: displays account details of the user currently logged in with optional profile picture, bio, list of user-submitted recipes with options to make public/private or delete, and links to edit user details/log out/delete user.
  - Pinned: displays recipes pinned by the user.
  - Log out: logs the user out and returns them to the homepage.
- Recipe detail pages display the option to pin another user recipe when a user is logged in.
- When logged in, users are able to submit recipes that default to private, which can then be made public from the Account page. 
- Pinned cocktails can be private if they were submitted by the user who pinned them.

## Further Goals:

- Stronger authentication for the users.
- Add .gif of user interactions in the readme.
- Folders for pinned cocktails that can be shared among users (current/past menus, etc.).
- Adjusting design for various screen sizes.
- Split database tables across multiple files.
- Ongoing: make it look pretty! Implement JS for front end user experience.

## Recent Changes:

- 9/24/2022 - Updated readme with further goals, created safeguards against deleting the test user account.
- 9/23/2022 - Added some unit testing for the models, divided some of the python into different route files.
- 9/16/2022 - Fixed a handful of typos, updated the requirements.txt, and deployed it using heroku.
