let dispCocktail = {};

async function getRandomCocktail() {
    const response = await axios.get("https://cors-anywhere.herokuapp.com/http://www.thecocktaildb.com/api/json/v1/1/random.php");
    let drink = response.data
    let drinkData = drink.drinks[0];
    let name = drinkData.strDrink;
    let pic = drinkData.strDrinkThumb;
    let id = drinkData.idDrink;
    dispCocktail = { name: name, pic: pic, id: id }
    console.log(dispCocktail)
    return dispCocktail;
};