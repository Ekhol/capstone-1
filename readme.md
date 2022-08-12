# Back-Pocket Cocktails
## A Resource for Bartenders and Cocktail Enthusiasts

## Preliminary API Selection and Schema Design:

API selected: https://www.thecocktaildb.com/api.php

Database Selection:

- Static/Public selection will be through the cocktaildb API, while there will also be a private database for users with accounts.

- The static database will be provided by the cocktaildb, while the private selection will allow users to upload recipes and information that are accessible to levels that they select: public, authorized, and authored.

- Public recipes will be accessible in the same way as the cocktaildb recipes.

- Authorized recipes will be private unless permission is granted to another user and the authorized recipes will be contained in a specific collection. ie. giving access to bartenders at a specific restaurant where they need the current and past recipes. This collection is not available to public users.

- Authored recipes are only affiliated with the creator. This is the trial stage of the drink, giving the author a chance to log trials before committing them to public consumption. They are directly tied to the author/user and need to be committed to an authorized recipe collection before they can be seen by others.

Schema Plan

- Sourcing from the cocktaildb is to provide a public/non-authorized access to recipes. It is the foundation of the application.
  
- There will be no committing to the cockatildb source.
  
- The second database will be created as a user database. It provides users a place to submit, store, and publish recipes in a way that they can choose how many people can view it.

- The second database will be the more 'fluid' of the two, allowing for permanent changes by the users through posting, editing, and deleting of recipes.

Stretch Goals

- Stronger authentication
- Public sourcing of images - cocktaildb has a collection of pictures for each drink and, although I admire their work, I think it could be personalized.
- Community forum - a place to brainstorm and test cocktail recipes in a supportive space.
- Design - I don't want it to look too terrible.