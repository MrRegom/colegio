/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: crypto-transaction Init Js File
*/

//transactionList Table
var perPage = 10;

var options = {
    valueNames: [
        "transactionId",
        "date",
        "from",
        "to",
        "coin",
        "amount",
        "status"
    ],
    page: perPage,
    pagination: true,
    plugins: [
        ListPagination({
            left: 2,
            right: 2,
        }),
    ],
};

// Init list
var transactionList = new List("transactionList", options).on("updated", function (list) {
    if (document.getElementsByClassName("noresult") && document.getElementsByClassName("noresult")[0]) {
        list.matchingItems.length == 0 ?
            (document.getElementsByClassName("noresult")[0].style.display = "block") :
            (document.getElementsByClassName("noresult")[0].style.display = "none");

        if (list.matchingItems.length > 0) {
            document.getElementsByClassName("noresult")[0].style.display = "none";
        } else {
            document.getElementsByClassName("noresult")[0].style.display = "block";
        }
    }

    var isFirst = list.i == 1;
    var isLast = list.i > list.matchingItems.length - list.page;
    document.querySelector(".pagination-prev.disabled") ?
        document.querySelector(".pagination-prev.disabled").classList.remove("disabled") : "";
    document.querySelector(".pagination-next.disabled") ?
        document.querySelector(".pagination-next.disabled").classList.remove("disabled") : "";

    if (isFirst) {
        document.querySelector(".pagination-prev").classList.add("disabled");
    }
    if (isLast) {
        document.querySelector(".pagination-next").classList.add("disabled");
    }
    if (list.matchingItems.length <= perPage) {
        document.querySelector("#pagination-element").style.display = "none";
    } else {
        document.querySelector("#pagination-element").style.display = "flex";
    }

    if (list.matchingItems.length == perPage) {
        document.querySelector(".pagination.listjs-pagination").firstElementChild.children[0].click()
    }
});

document.querySelector(".pagination-next").addEventListener("click", function () {
    document.querySelector(".pagination.listjs-pagination") ?
        document.querySelector(".pagination.listjs-pagination").querySelector(".active") && document.querySelector(".pagination.listjs-pagination").querySelector(".active").nextElementSibling != null ?
            document.querySelector(".pagination.listjs-pagination").querySelector(".active").nextElementSibling.children[0].click() : "" : "";
});

document.querySelector(".pagination-prev").addEventListener("click", function () {
    document.querySelector(".pagination.listjs-pagination") ?
        document.querySelector(".pagination.listjs-pagination").querySelector(".active") && document.querySelector(".pagination.listjs-pagination").querySelector(".active").previousSibling != null ?
            document.querySelector(".pagination.listjs-pagination").querySelector(".active").previousSibling.children[0].click() : "" : "";
});