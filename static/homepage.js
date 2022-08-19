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

function HTMLCocktail(cocktail) {
    return `<li class="list-unstyled d-flex justify-content-center">
    <div class="card" style="width: 18rem;">
    <img class="card-img-top" src="${cocktail.pic}" alt="Card image cap">
        <div class="card-body">
         <h5 class="card-title">${cocktail.name}</h5>
            <a href="/recipes/cdb/${cocktail.id}" class="btn btn-primary">More Details</a>
        </div>
    </div>
    </li>`;
};

async function displayCocktail() {
    dispCocktail = {};

    await getRandomCocktail();
    let HTMLAppend = HTMLCocktail(dispCocktail);

    $("#card-container").append(HTMLAppend);
    console.log("appended");
};

displayCocktail();