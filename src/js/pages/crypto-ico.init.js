/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.comom
File: Crypto ico Init Js File
*/

var url = "/static/json/";
var allIcoList = '';
var currentPage = 1;
var itemsPerPage = 16;

var prevButton = document.getElementById('page-prev');
var nextButton = document.getElementById('page-next');

//ico list by json
var getJSON = function (jsonurl, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url + jsonurl, true);
    xhr.responseType = "json";
    xhr.onload = function () {
        var status = xhr.status;
        if (status === 200) {
            callback(null, xhr.response);
        } else {
            callback(status, xhr.response);
        }
    };
    xhr.send();
};

// get json
getJSON("ico-list.json", function (err, data) {
    if (err !== null) {
        console.log("Something went wrong: " + err);
    } else {
        allIcoList = data;
        loadIcoData(allIcoList, currentPage);
    }
});


// load ico list data
function loadIcoData(datas, page) {
    var pages = Math.ceil(datas.length / itemsPerPage)
    if (page < 1) page = 1
    if (page > pages) page = pages;
    document.querySelector("#ico-list").innerHTML = '';

    for (var i = (page - 1) * itemsPerPage; i < (page * itemsPerPage) && i < datas.length; i++) {
        if (datas[i]) {
            // Array.from(datas).forEach(function (listData, index) {
            var leftDayElem = "";
            if (datas[i].day_left) {
                leftDayElem = '<div class="flex-shrink-0 text-end">\
                <p class="text-primary fw-semibold fs-md mb-1">'+ datas[i].day_left.percentage + '</p>\
                <p class="text-muted mb-0">'+ datas[i].day_left.days + '</p>\
            </div>';
            } else {
                leftDayElem = "";
            }

            var tokenElem = "";
            if (datas[i].token.current) {
                tokenElem = '<span class="text-primary">' + datas[i].token.current + '</span>/ '
            } else {
                tokenElem = "";
            }

            document.querySelector("#ico-list").innerHTML += '<div class="col-xl-3 col-lg-4 col-sm-6">\
        <div class="card">\
            <div class="card-body">\
                <div class="d-flex gap-2 mb-4">\
                    <img src="'+ datas[i].crypto.logoImg + '" alt="" class="avatar-xs">\
                    <div class="flex-grow-1">\
                        <a href="apps-crypto-coin-overview.html" class="stretched-link"><h6 class="fs-md mb-1">'+ datas[i].crypto.name + '</h6></a>\
                        <p class="text-muted mb-0">'+ datas[i].category + '</p>\
                    </div>\
                    <div>'+ isStatus(datas[i].status) + '</div>\
                </div>\
                <div class="d-flex gap-2">\
                    <div class="flex-grow-1">\
                        <p class="text-muted fw-semibold fs-md mb-1">'+ tokenElem + datas[i].token.price + '</p>\
                        <p class="text-muted mb-0">Token</p>\
                    </div>\
                    '+ leftDayElem + '\
                </div>\
            </div>\
        </div>\
    </div>';
        };
    }

    paginationEvents();
    currentPage == 1 ? prevButton.parentNode.classList.add('disabled') : prevButton.parentNode.classList.remove('disabled');
    currentPage == pages ? nextButton.parentNode.classList.add('disabled') : nextButton.parentNode.classList.remove('disabled');
}

function isStatus(val) {
    switch (val) {
        case "Active":
            return (
                '<span class="badge bg-success-subtle text-success">' + val + "</span>"
            );
        case "Upcoming":
            return (
                '<span class="badge bg-warning-subtle text-warning">' + val + "</span>"
            );
        case "Ended":
            return (
                '<span class="badge bg-danger-subtle text-danger">' + val + "</span>"
            );
    }
}

function selectedPage() {
    var pagenumLink = document.getElementById('page-num').getElementsByClassName('clickPageNumber');
    for (var i = 0; i < pagenumLink.length; i++) {
        if (i == currentPage - 1) {
            pagenumLink[i].parentNode.classList.add("active");
        } else {
            pagenumLink[i].parentNode.classList.remove("active");
        }
    }
};

// paginationEvents
function paginationEvents() {
    var numPages = function numPages() {
        return Math.ceil(allIcoList.length / itemsPerPage);
    };

    function clickPage() {
        document.addEventListener('click', function (e) {
            if (e.target.nodeName == "A" && e.target.classList.contains("clickPageNumber")) {
                currentPage = e.target.textContent;
                loadIcoData(allIcoList, currentPage);
            }
        });
    };

    function pageNumbers() {
        var pageNumber = document.getElementById('page-num');
        pageNumber.innerHTML = "";
        // for each page
        for (var i = 1; i < numPages() + 1; i++) {
            pageNumber.innerHTML += "<div class='page-item'><a class='page-link clickPageNumber' href='javascript:void(0);'>" + i + "</a></div>";
        }
    }

    prevButton.addEventListener('click', function () {
        if (currentPage > 1) {
            currentPage--;
            loadIcoData(allIcoList, currentPage);
        }
    });

    nextButton.addEventListener('click', function () {
        if (currentPage < numPages()) {
            currentPage++;
            loadIcoData(allIcoList, currentPage);
        }
    });

    pageNumbers();
    clickPage();
    selectedPage();
}
