/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.com
File: Profile init js
*/

//transactionsList Table
var options = new List('transactionsList', {
    valueNames: [
        "date",
        "transactions",
        "coinName",
        "type",
        "products",
        "amount",
        "status"
    ],
    page: 5,
    pagination: true
});


// customer image
document.querySelector("#profile-img-file-input").addEventListener("change", function () {
    var preview = document.querySelector("#profile-img");
    var file = document.querySelector("#profile-img-file-input").files[0];
    var reader = new FileReader();
    reader.addEventListener("load",function () {
        preview.src = reader.result;
    },false);
    if (file) {
        reader.readAsDataURL(file);
    }
});