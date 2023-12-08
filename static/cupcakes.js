"use strict";

const $cupcakeDisplay = $("#cupcake_data_list");
const $cupcakeForm = $("#cupcake_data_form");
const $flavorInput = $("#flavor_input");
const $sizeInput = $("#size_input");
const $ratingInput = $("#rating_input");
const $imageInput = $("#image_input");


// 1) Fetch cupcake list (Fetch API)
// 2) Loop through and add it to cupcake display

getAndDisplayCupcakes();


// 3) On form submit (event listener), make POST request (Fetch) and update list

async function getCupcakeData(){
  const response = await fetch("/api/cupcakes", {method: "GET"})

  const responseObj = await response.json();
  console.log("responseObj = ", responseObj);
  console.log("responseObj.cupcakes = ", responseObj.cupcakes);

  return responseObj.cupcakes;
}

function clearAndDisplayCupcakes(cupcakes){
  $cupcakeDisplay.empty();
  for (let cupcake of cupcakes)
  {
    $cupcakeDisplay.append($(`<li>
    <p>Cupcake flavor: ${cupcake.flavor}</p>
    <p>Cupcake rating: ${cupcake.rating}</p>
    <p>Cupcake size: ${cupcake.size}</p>
    <img src="${cupcake.image_url}">
    </li>`));
  }
}

async function formSubmission(evt){
  evt.preventDefault();

  const inputs = {
    "flavor": $flavorInput.val(),
    "size": $sizeInput.val(),
    "rating": $ratingInput.val(),
    "image_url": $imageInput.val(),
  };

  const response = await fetch("/api/cupcakes", {
    method: "POST",
    body: JSON.stringify(inputs),
    headers: {
      "Content-Type": "application/json"
    }
  });

  getAndDisplayCupcakes();
  $flavorInput.val("");
  $sizeInput.val("");
  $ratingInput.val(0);
  $imageInput.val("");


}

$cupcakeForm.on("submit", formSubmission);

async function getAndDisplayCupcakes(){
  const cupcakes = await getCupcakeData();
  clearAndDisplayCupcakes(cupcakes);
}