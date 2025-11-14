/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: crypto-marketplace Init Js File
*/

//transactionList Table
var perPage = 10;

var options = {
    valueNames: [
        "id",
        "Name",
        "Price",
        "onehour",
        "oneday",
        "oneweek",
        "Market_Cap",
        "Volume_one_day",
        "action",

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

const MarketplaceCoin = new List("transactionList", options).on("updated", (list) => {
    if (list.matchingItems.length === 0) {
        document.getElementsByClassName("noresult")[0].style.display = "block";
    } else {
        document.getElementsByClassName("noresult")[0].style.display = "none";
    }
    const isFirst = list.i === 1;
    const isLast = list.i > list.matchingItems.length - list.page;
    // make the Prev and Next buttons disabled on first and last pages accordingly
    const prevBtn = document.querySelector(".pagination-prev.disabled");
    const nextBtn = document.querySelector(".pagination-next.disabled");

    if (prevBtn)
        prevBtn.classList.remove("disabled");

    if (nextBtn)
        nextBtn.classList.remove("disabled");

    if (isFirst)
        document.querySelector(".pagination-prev").classList.add("disabled");

    if (isLast)
        document.querySelector(".pagination-next").classList.add("disabled");

    const paginationElem = document.getElementById("pagination-element");

    if (list.matchingItems.length < 1) {
        paginationElem.style.display = "none";
    }
    else
        paginationElem.style.display = "flex";

    if (list.matchingItems.length > 0) {

        document.getElementsByClassName("noresult")[0].style.display = "none";
    }
    else {
        document.getElementsByClassName("noresult")[0].style.display = "block";
    }

    const totalRecordsElement = MarketplaceCoin.listContainer.querySelector(".total-records");
    const showingElement = MarketplaceCoin.listContainer.querySelector(".showing");

    if (totalRecordsElement) totalRecordsElement.innerHTML = MarketplaceCoin.items.length;
    if (showingElement) showingElement.innerHTML = MarketplaceCoin.visibleItems.length;
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
// global var

var idField = document.getElementById("id-field");
var coinnameField = document.getElementById("coinname-field");
var cointageField = document.getElementById("cointage-field");
var coinpriceField = document.getElementById("coinprice-field");
var cryptoList = [
    {
        "id": "1",
        "Tage": "BTC",
        "Name": "Bitcoin",
        "img": "btc.svg",
        "Price": "$26,807.45",
        "onehour": "0.16%",
        "oneday": "-1.83%",
        "oneweek": "-0.18%",
        "Market_Cap": "$519,613,016,809",
        "Volume_one_day": "$12,492,715,725"
    },
    {
        "id": "2",
        "Tage": "ETh",
        "Name": "Ethereum",
        "img": "eth.svg",
        "Price": "$1,818.98",
        "onehour": "0.12%",
        "oneday": "-2.02%",
        "oneweek": "0.61%",
        "Market_Cap": "$218,755,466,290",
        "Volume_one_day": "$5,880,391,745"
    },
    {
        "id": "3",
        "Tage": "USDT",
        "Name": "Tether",
        "img": "usdt.svg",
        "Price": "$0.9999",
        "onehour": "0.01%",
        "oneday": "-0.02%",
        "oneweek": "-0.02%",
        "Market_Cap": "$83,020,592,698",
        "Volume_one_day": "$20,074,570,094"
    },
    {
        "id": "4",
        "Tage": "SOL",
        "Name": "Solana",
        "img": "sol.svg",
        "Price": "$19.52",
        "onehour": "-0.15%",
        "oneday": "1.43%",
        "oneweek": "-5.51%",
        "Market_Cap": "$7,733,266,613",
        "Volume_one_day": "$239,223,676"
    },
    {
        "id": "5",
        "Tage": "LTC",
        "Name": "Litecoin",
        "img": "ltc.svg",
        "Price": "$86.72",
        "onehour": "0.25%",
        "oneday": "-5.57%",
        "oneweek": "-6.27%",
        "Market_Cap": "$6,329,627,132",
        "Volume_one_day": "$589,392,797"
    },
    {
        "id": "6",
        "Tage": "TRX",
        "Name": "TRON",
        "img": "trx.svg",
        "Price": "$0.07711",
        "onehour": "-0.59%",
        "oneday": "-1.24%",
        "oneweek": "9.03%",
        "Market_Cap": "$6,964,078,550",
        "Volume_one_day": "$213,515,833"
    },
    {
        "id": "7",
        "Tage": "AAVE",
        "Name": "Aave",
        "img": "aave.svg",
        "Price": "$64.09",
        "onehour": "0.04%",
        "oneday": "-2.22%",
        "oneweek": "2.25%",
        "Market_Cap": "$922,658,515",
        "Volume_one_day": "$29,377,273"
    },
    {
        "id": "8",
        "Tage": "DASH",
        "Name": "Dash",
        "img": "dash.svg",
        "Price": "$42.03",
        "onehour": "0.18%",
        "oneday": "-4.76%",
        "oneweek": "-6.73%",
        "Market_Cap": "$474,405,043",
        "Volume_one_day": "$50,392,655"
    },
    {
        "id": "9",
        "Tage": "DCR",
        "Name": "Decred",
        "img": "dcr.svg",
        "Price": "$16.52",
        "onehour": "0.84%",
        "oneday": "-1.65%",
        "oneweek": "-5.25%",
        "Market_Cap": "$247,283,803",
        "Volume_one_day": "$980,916"
    },
    {
        "id": "10",
        "Tage": "ZEN",
        "Name": "Horizen",
        "img": "zen.svg",
        "Price": "$8.61",
        "onehour": "-0.01%",
        "oneday": "-1.58%",
        "oneweek": "1.94%",
        "Market_Cap": "$118,061,115",
        "Volume_one_day": "$4,535,690"
    },
    {
        "id": "11",
        "Tage": "GAS",
        "Name": "Gas",
        "img": "gas.svg",
        "Price": "$2.82",
        "onehour": "-0.05%",
        "oneday": "-0.17%",
        "oneweek": "3.17%",
        "Market_Cap": "$28,546,843",
        "Volume_one_day": "$10,548,431"
    }
]


function loadFileData(datas) {
    var itemId = 1;
    MarketplaceCoin.remove('id', itemId);

    Array.from(datas).forEach(function (element, index) {
        MarketplaceCoin.add({
            id: element.id,
            Tage: element.Tage,
            Name: '<a href="apps-crypto-coin-overview.html"class="d-flex gap-2 align-items-center">\
            <img src="/static/images/svg/crypto-icons/'+ element.img + '"alt="" class="avatar-xxs">\
            <h6 class="mb-0 Name">Bitcoin <span class="badge bg-light text-body fw-normal Tage">'+ element.Tage + '</span>\</h6>\</a>',
            Price: element.Price,
            onehour: element.onehour,
            oneday: element.oneday,
            oneweek: element.oneweek,
            Market_Cap: element.Market_Cap,
            Volume_one_day: element.Volume_one_day,

        });
        MarketplaceCoin.sort('id', { order: "desc" });
    });
    console.log("MarketplaceCoin", MarketplaceCoin)
}
setTimeout(() => {
    loadFileData(cryptoList);
}, 0);

var count = 12;
var forms = document.querySelectorAll('.tablelist-form')

Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        // Define an array with all the required input fields and their corresponding error messages
        const requiredFields = [
            { input: coinnameField, error: "Please enter a coin name." },
            { input: cointageField, error: "Please enter a coin tage." },
            { input: coinpriceField, error: "Please enter a coin price." },
        ];
        let allFieldsValid = true;
        // Check each required input field to see if it has a value
        requiredFields.forEach(function (field) {
            if (allFieldsValid && field.input.value.trim() === "") {
                // The field is empty, so show the error message and mark allFieldsValid as false
                field.input.classList.add("is-invalid");
                allFieldsValid = false;
            } else {
                // The field has a value, so remove the error message and mark the field as valid
                field.input.classList.remove("is-invalid");
            }
        });
        MarketplaceCoin.add({
            id: count,
            Name: '<a href="apps-crypto-coin-overview.html"class="d-flex gap-2 align-items-center">\
            <img src="/static/images/svg/crypto-icons/aave.svg"alt="" class="avatar-xxs">\
            <h6 class="mb-0 Name">'+ coinnameField.value + ' <span class="badge bg-light text-body fw-normal Tage">' + cointageField.value + '</span>\</h6>\</a>',
            Price: "$" + coinpriceField.value,
            onehour: "-",
            oneday: "-",
            oneweek: "-",
            Market_Cap: "-",
            Volume_one_day: "-",

        })
        MarketplaceCoin.sort('id', { order: "desc" });
        // document.getElementById("alert-error-msg").classList.add("d-none");
        document.getElementById("close-modal").click();
        count++;
        clearFields();
        // refreshCallbacks();
        Swal.fire({
            position: 'center',
            icon: 'success',
            title: 'File name inserted successfully!',
            showConfirmButton: false,
            timer: 2000,
            showCloseButton: true
        });
        // } else
        if (editList && allFieldsValid) {
            var editValues = MarketplaceCoin.get({
                id: idField.value,
            });
            Array.from(editValues).forEach(function (x) {
                var isId = new DOMParser().parseFromString(x._values.id, "text/html");
                var selectedId = isId.body.innerHTML;
                if (selectedId == itemId) {
                    x.values({
                        id: `<a href="#" class="fw-medium link-primary">${idField.value}</a>`,
                        document_name: filenameField.value,
                    });
                }
            });
            // document.getElementById("alert-error-msg").classList.add("d-none");
            document.getElementById("close-modal").click();
            clearFields();
            Swal.fire({
                position: 'center',
                icon: 'success',
                title: 'File name updated successfully!',
                showConfirmButton: false,
                timer: 2000,
                showCloseButton: true
            });
        }
        return true;
    });
});

function clearFields() {
    editList = false;
    idField.value = "";
    coinnameField.value = "";
    cointageField.value = "";
    coinpriceField.value = "";
}

