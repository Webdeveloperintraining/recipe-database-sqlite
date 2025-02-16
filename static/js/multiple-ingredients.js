const plusBtn = document.getElementById('plus');
const ingredients = document.querySelector('.ingredients');

let counter = 1

// This code adds as many inputs for adding ingredients as needed
plusBtn.addEventListener('click', () => {
    // this creates the container and the inputs for capturing the ingredients amounts
    let divM = document.createElement('div');
    let labelM = document.createElement('label');
    labelM.setAttribute('for', `amount${counter}`);
    labelM.textContent = 'Amount:';
    let inputM = document.createElement('input');
    inputM.setAttribute('type', 'text');
    inputM.setAttribute('name', `amount${counter}`);
    inputM.setAttribute('id', `amount${counter}`);
    
    divM.appendChild(labelM);
    divM.appendChild(inputM);

    ingredients.appendChild(divM);
    
    // this creates the container and the inputs for capturing the ingredients names
    let divI = document.createElement('div');
    let labelI = document.createElement('label');
    labelI.setAttribute('for', `ingredient${counter}`);
    labelI.textContent = 'Ingredient';
    let inputI = document.createElement('input');
    inputI.setAttribute('type', 'text'); 
    inputI.setAttribute('name', `ingredient${counter}`);
    inputI.setAttribute('id', `ingredient${counter}`); 

    divI.appendChild(labelI);
    divI.appendChild(inputI);

    ingredients.appendChild(divI);
    
   counter++;
});


const form=  document.getElementById('handlingForm');
const hiddenInputIngredients = document.getElementById('ingredients');
const hiddenInputAmounts = document.getElementById('amounts');

form.addEventListener("submit", (event) => {
    event.preventDefault();

    const ingredients = document.querySelectorAll('[name^="ingredient"]');
    let ingredientNames = []

    ingredients.forEach( (ingredient) =>{
        if(ingredient.value !== ""){
        ingredientNames.push(ingredient.value.trim());
        }
    });

    const amounts = document.querySelectorAll('[name^="amount"]');
    let amountQuantities = []
    
    amounts.forEach( (amount)=>{
        if(amount.value !== ""){
        amountQuantities.push(amount.value.trim());
        }
    });

    hiddenInputIngredients.value = JSON.stringify(ingredientNames)
    hiddenInputAmounts.value = JSON.stringify(amountQuantities)

    console.log(ingredientNames);
    console.log(amountQuantities);

    form.submit();
});





