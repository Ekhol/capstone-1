# Back-Pocket Cocktails
## A Resource for Bartenders and Cocktail Enthusiasts

# Note: This app is designed for mobile devices.
## https://back-pocket-cocktails.herokuapp.com/search


## Preliminary API Selection:

API selected: https://www.thecocktaildb.com/api.php

Database Selection:

- Static/Public selection will be through the cocktaildb API, while there will also be a private database for users with accounts.

- The static database will be provided by the cocktaildb, while the private selection will allow users to upload recipes and information that are accessible to levels that they select: public, authorized, and authored.

- Public recipes will be accessible in the same way as the cocktaildb recipes.

- Private recipes will remain private until publicized. ie. giving access to bartenders at a specific restaurant where they need the current and past recipes. This collection is not available to public users.

- Authored recipes are only affiliated with the creator. This is the trial stage of the drink, giving the author a chance to log trials before committing them to public consumption. They are directly tied to the author/user and need to be committed to an authorized recipe collection before they can be seen by others.

## User Flow:

### Public View

Public view will be the data accessible by users who are not logged in or do not have an account. It will provide the information pulled from the cocktaildb as well as data from drinks that authorized users have deemed public. 

PULLS data from cocktaildb API and the original database and displays them in two different fields:

- Database cocktails
- User-submitted cocktails

Begins with the homepage displaying a random cocktail pulled from the CocktailDB API. 

### Authorized User View

Authorized user view will be accessible by users who have created an account and are logged in. Beyond accessing the classic cocktail and public user-submitted list, they will have access to individualized folders where they can pin cocktails for easy access and a field to upload their own drinks. 


Stretch Goals

- Stronger authentication
- Public sourcing of images - cocktaildb has a collection of pictures for each drink and, although I admire their work, I think it could be personalized.
- Community forum - a place to brainstorm and test cocktail recipes in a supportive space.
- Design - I don't want it to look too terrible.
