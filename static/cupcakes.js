"use strict";

const $cupcakeDisplay = $("#cupcake_data_list");
const $cupcakeForm = $("#cupcake_data_form");


// 1) Fetch cupcake list (Fetch API)
// 2) Loop through and add it to cupcake display

getCupcakeData();


// 3) On form submit (event listener), make POST request (Fetch) and update list

async function getCupcakeData(){
  const response = await fetch("/api/cupcakes", {method: "GET"})

  const responseObj = await response.json();
  console.log("responseObj = ", responseObj);
  console.log("responseObj.cupcakes = ", responseObj.cupcakes);

  const cupcakes = responseObj.cupcakes;

  for (let cupcake of cupcakes)
  {
    $cupcakeDisplay.append($("<li>Cupcake</li>"));
  }

}