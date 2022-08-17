async function getRandomCocktail() {
    const response = await axios.get("http://www.thecocktaildb.com/api/json/v1/1/random.php");
    let drink = response.data;
    let drinkName = drink.strDrink;
    let drinkPic = drink.strDrinkThumb;
    let drinkId = drink.idDrink;

    return { drinkName, drinkPic, drinkId };
};

async function displayCocktail() {

    // START HERE NEXT TIME //
}

