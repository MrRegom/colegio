/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Website: https://themesbrand.com/
Contact: themesbrand@gmail.com
File: customer list Init Js File
*/

const perPage = 10;
var editList = false;

const checkAll = document.getElementById("checkAll");
if (checkAll) {
    checkAll.addEventListener("click", handleCheckAll);
}

function handleCheckAll() {
    const checkboxes = document.querySelectorAll('.form-check-all input[type="checkbox"]');
    const checkedCount = document.querySelectorAll('.form-check-all input[type="checkbox"]:checked').length;
    const isChecked = this.checked;

    checkboxes.forEach((checkbox) => {
        checkbox.checked = isChecked;
        updateRowStyle(checkbox);
    });

    updateRemoveActionsVisibility(checkedCount);
}

function updateRowStyle(checkbox) {
    const row = checkbox.closest("tr");
    if (checkbox.checked)
        row.classList.add("table-active");
    else
        row.classList.remove("table-active");
}

function updateRemoveActionsVisibility(checkedCount) {
    const removeActions = document.getElementById("remove-actions");
    if (checkedCount > 0)
        removeActions.classList.add("d-none");
    else
        removeActions.classList.remove("d-none");
}

//customerList Table
var options = {
    valueNames: [
        "id",
        "name",
        "company_name",
        "membership",
        "email_id",
        "phone",
        "date",
        "tags"
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
const customerList = new List("customerList", options).on("updated", (list) => {
    if (list.matchingItems.length === 0)
        document.getElementsByClassName("noresult")[0].style.display = "block";
    else
        document.getElementsByClassName("noresult")[0].style.display = "none";

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

    if (list.matchingItems.length <= 1)
        paginationElem.style.display = "none";
    else
        paginationElem.style.display = "flex";

    if (list.matchingItems.length > 0)
        document.getElementsByClassName("noresult")[0].style.display = "none";
    else
        document.getElementsByClassName("noresult")[0].style.display = "block";

    if (list.matchingItems.length == perPage) {
        document.querySelector(".pagination.listjs-pagination").firstElementChild.children[0].click()
    }
    const totalRecordsElement = customerList.listContainer.querySelector(".total-records");
    const showingElement = customerList.listContainer.querySelector(".showing");

    if (totalRecordsElement) totalRecordsElement.innerHTML = customerList.items.length;
    if (showingElement) showingElement.innerHTML = customerList.visibleItems.length;

});

const xhttp = new XMLHttpRequest();
xhttp.onload = function () {
    var json_records = JSON.parse(this.responseText);
    Array.from(json_records).forEach(function (element) {
        var tags = element.tags;
        var tagHtml = '<div class="d-flex gap-1">';
        Array.from(tags).forEach((tag, index) => {
            tagHtml += '<span class="badge bg-light text-body">' + tag + '</span>'
        })
        tagHtml += '</div>';
        customerList.add({
            id: `<a href="apps-customers-overview.html" class="fw-medium link-primary">#TB${element.id}</a>`,
            name: '<div class="d-flex align-items-center gap-2">\
                    <div class="flex-shrink-0">\
                        <img src="'+ element.customer[0].img + '" alt="" class="avatar-xxs rounded-circle">\
                    </div>\
                    <a href="apps-customers-overview.html" class="text-reset"><h6 class="mb-0 flex-grow-1 text-reset contactname">'+ element.customer[0].name + '</h6></a>\
                </div>',
            company_name: element.company_name,
            membership: isMembership(element.membership).outerHTML,
            email_id: element.email,
            phone: element.phone,
            date: element.create_date,
            tags: tagHtml,
        });
        customerList.sort('id', { order: "desc" });
        ischeckboxcheck();
        refreshCallbacks();
    });
    customerList.remove("id", `<a href="apps-customers-overview.html" class="fw-medium link-primary">#TB01</a>`);
}

xhttp.open("GET", "/static/json/customer-list.json");
xhttp.send();


// customer image
document.querySelector("#customer-image-input").addEventListener("change", function () {
    var preview = document.querySelector("#customer-img");
    var file = document.querySelector("#customer-image-input").files[0];
    var reader = new FileReader();
    reader.addEventListener("load", function () {
        preview.src = reader.result;
    }, false);
    if (file) {
        reader.readAsDataURL(file);
    }
});


var idField = document.getElementById("id-field");
var customerImg = document.getElementById("customer-img");
var customerNameField = document.getElementById("customername-field");
var company_nameField = document.getElementById("company_name-field");
var membershipField = document.getElementById("membership-field");
var tagInputField = document.getElementById("taginput-choices");
var email_idField = document.getElementById("email_id-field");
var phoneField = document.getElementById("phone-field")

var removeBtns = document.getElementsByClassName("remove-item-btn");
var editBtns = document.getElementsByClassName("edit-item-btn");


var membershipVal = new Choices(membershipField, {
    searchEnabled: false
});

var tagInputVal = new Choices(tagInputField, {
    removeItemButton: true,
});

function isMembership(val) {
    const badge = document.createElement("span");

    switch (val) {
        case "Golden":
            badge.classList.add("badge", "bg-warning");
            badge.textContent = val;
            break;
        case "Sliver":
            badge.classList.add("badge", "bg-info");
            badge.textContent = val;
            break;
        case "Basic":
            badge.classList.add("badge", "bg-secondary");
            badge.textContent = val;
            break;
        default:
            badge.classList.add("badge", "bg-info");
            badge.textContent = val;
            break;
    }

    return badge;
}

// tablelist-form
var count = 14;
var itemId
// date & time
var dateValue = new Date().toUTCString().slice(5, 16);

// tablelist form submit event
var forms = document.querySelectorAll('.tablelist-form')
Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        var errorMsg = document.getElementById("alert-error-msg");
        errorMsg.classList.remove("d-none");

        setTimeout(() => errorMsg.classList.add("d-none"), 2000);

        // Define an array with all the required input fields and their corresponding error messages
        const requiredFields = [
            { input: customerNameField, error: "Please enter a customer name." },
            { input: company_nameField, error: "Please enter a company name." },
            { input: membershipField, error: "Please select a select membership." },
            { input: email_idField, error: "Please enter a email address." },
            { input: phoneField, error: "Please enter a phone no." },
            { input: tagInputField, error: "Please select a tags." }
        ];

        let allFieldsValid = true;

        // Check each required input field to see if it has a value
        requiredFields.forEach(function (field) {
            if (allFieldsValid && field.input.value.trim() === "") {
                // The field is empty, so show the error message and mark allFieldsValid as false
                errorMsg.innerHTML = field.error;
                field.input.classList.add("is-invalid");
                allFieldsValid = false;
            } else {
                // The field has a value, so remove the error message and mark the field as valid
                field.input.classList.remove("is-invalid");
            }
        });

        var tagInputFieldValue = tagInputVal.getValue(true);
        var tagHtmlValue = '';
        Array.from(tagInputFieldValue).forEach((tag, index) => {
            tagHtmlValue += '<span class="badge bg-light text-body">' + tag + '</span>'
        })

        if (!editList && allFieldsValid) {
            customerList.add({
                id: `<a href="apps-customers-overview.html" class="fw-medium link-primary">#TB${count}</a>`,
                name: '<div class="d-flex align-items-center gap-2">\
                    <div class="flex-shrink-0">\
                        <img src="'+ customerImg.src + '" alt="" class="avatar-xxs rounded-circle">\
                    </div>\
                    <a href="apps-customers-overview.html" class="text-reset"><h6 class="mb-0 flex-grow-1 text-reset contactname">'+ customerNameField.value + '</h6></a>\
                </div>',
                company_name: company_nameField.value,
                membership: isMembership(membershipField.value).outerHTML,
                email_id: email_idField.value,
                phone: phoneField.value,
                date: dateValue,
                tags: tagHtmlValue,
            })
            customerList.sort('id', { order: "desc" });
            document.getElementById("alert-error-msg").classList.add("d-none");
            document.getElementById("close-modal").click();
            count++;
            clearFields();
            refreshCallbacks();
            Swal.fire({
                position: 'center',
                icon: 'success',
                title: 'Customer details inserted successfully!',
                showConfirmButton: false,
                timer: 2000,
                showCloseButton: true
            });
        } else if (editList && allFieldsValid) {
            var editValues = customerList.get({
                id: idField.value,
            });

            Array.from(editValues).forEach(function (x) {
                var isId = new DOMParser().parseFromString(x._values.id, "text/html");
                var selectedId = isId.body.firstElementChild.innerHTML;

                if (selectedId == itemId) {
                    x.values({
                        id: `<a href="apps-customers-overview.html" class="fw-medium link-primary">#TB${idField.value}</a>`,
                        name: '<div class="d-flex align-items-center gap-2">\
                            <div class="flex-shrink-0">\
                                <img src="'+ customerImg.src + '" alt="" class="avatar-xxs rounded-circle">\
                            </div>\
                            <a href="apps-customers-overview.html" class="text-reset"><h6 class="mb-0 flex-grow-1 text-reset contactname">'+ customerNameField.value + '</h6></a>\
                        </div>',
                        company_name: company_nameField.value,
                        membership: isMembership(membershipField.value).outerHTML,
                        email_id: email_idField.value,
                        phone: phoneField.value,
                        date: dateValue,
                        tags: tagHtmlValue,
                    });
                }
            });
            document.getElementById("alert-error-msg").classList.add("d-none");
            document.getElementById("close-modal").click();
            clearFields();
            Swal.fire({
                position: 'center',
                icon: 'success',
                title: 'Customer details updated successfully!',
                showConfirmButton: false,
                timer: 2000,
                showCloseButton: true
            });
        }
        return true;
    });
});


document.getElementById("showModal").addEventListener("show.bs.modal", function (e) {
    if (e.relatedTarget.classList.contains("edit-item-btn")) {
        document.getElementById("exampleModalLabel").innerHTML = "Edit Customer";
        document.getElementById("showModal").querySelector(".modal-footer").style.display = "block";
        document.getElementById("add-btn").innerHTML = "Update";
    } else if (e.relatedTarget.classList.contains("add-btn")) {
        document.getElementById("exampleModalLabel").innerHTML = "Add Customer";
        document.getElementById("showModal").querySelector(".modal-footer").style.display = "block";
        document.getElementById("add-btn").innerHTML = "Add Customer";
    } else {
        document.getElementById("exampleModalLabel").innerHTML = "List product";
        document.getElementById("showModal").querySelector(".modal-footer").style.display = "none";
    }
});


function ischeckboxcheck() {
    Array.from(document.getElementsByName("chk_child")).forEach(function (checkbox) {
        checkbox.addEventListener("change", function (event) {
            var closestRow = event.target.closest("tr");
            console.log(closestRow)
            if (checkbox.checked) {
                closestRow.classList.add("table-active");
            } else {
                closestRow.classList.remove("table-active");
            }

            var checkedCount = document.querySelectorAll('[name="chk_child"]:checked').length;
            var removeActions = document.getElementById("remove-actions");
            if (closestRow.classList.contains("table-active")) {
                removeActions.classList.toggle("d-none", checkedCount <= 0);
            } else {
                removeActions.classList.toggle("d-none", checkedCount <= 0);
            }
        });
    });
}

function refreshCallbacks() {
    // editBtns
    if (editBtns) {
        Array.from(editBtns).forEach(function (btn) {
            btn.addEventListener("click", function (e) {

                e.target.closest("tr").children[1].innerText;
                itemId = e.target.closest("tr").children[1].innerText;
                var itemValues = customerList.get({
                    id: itemId,
                });
                console.log(itemId, itemValues)

                Array.from(itemValues).forEach(function (x) {
                    var isId = new DOMParser().parseFromString(x._values.id, "text/html");
                    var selectedId = isId.body.firstElementChild.innerHTML;
                    if (selectedId == itemId) {
                        var tagBadge = new DOMParser().parseFromString(x._values.tags, "text/html").body.querySelectorAll("span.badge");

                        editList = true;
                        idField.value = selectedId;
                        customerImg.src = new DOMParser().parseFromString(x._values.name, "text/html").body.querySelector("img").src;
                        customerNameField.value = new DOMParser().parseFromString(x._values.name, "text/html").body.querySelector(".contactname").innerHTML;
                        company_nameField.value = x._values.company_name;
                        email_idField.value = x._values.email_id;
                        phoneField.value = x._values.phone;

                        // membershipVal
                        if (membershipVal) membershipVal.destroy();
                        membershipVal = new Choices(membershipField, {
                            removeItemButton: true,
                        });
                        membershipVal.setChoiceByValue(new DOMParser().parseFromString(x._values.membership, "text/html").body.querySelector("span.badge").innerHTML);

                        if (tagBadge) {
                            // tagInputVal
                            if (tagInputVal) tagInputVal.destroy();
                            tagInputVal = new Choices(tagInputField, {
                                removeItemButton: true,
                            });
                            Array.from(tagBadge).forEach((item) => {
                                tagInputVal.setChoiceByValue(item.innerHTML);
                            })
                        }
                    }
                });
            });
        });
    };


    // removeBtns
    if (removeBtns) {
        Array.from(removeBtns).forEach(function (btn) {
            btn.addEventListener("click", function (e) {
                e.target.closest("tr").children[1].innerText;
                var removeitemId = e.target.closest("tr").children[1].innerText;
                console.log("delete", removeitemId)
                var itemValues = customerList.get({
                    id: removeitemId,
                });

                Array.from(itemValues).forEach(function (x) {
                    deleteid = new DOMParser().parseFromString(x._values.id, "text/html");

                    var isElem = deleteid.body.firstElementChild;
                    var isdeleteid = deleteid.body.firstElementChild.innerHTML;

                    if (isdeleteid == removeitemId) {
                        document.getElementById("delete-record").addEventListener("click", function () {
                            customerList.remove("id", isElem.outerHTML);
                            document.getElementById("deleteRecord-close").click();
                        });
                    }
                });
            });
        });
    }
}


function clearFields() {
    editList = false;
    idField.value = "";
    customerImg.src = "/static/images/users/user-dummy-img.jpg";
    document.getElementById("customer-image-input").value = "";
    customerNameField.value = "";
    company_nameField.value = "";
    membershipField.value = "";
    email_idField.value = "";
    phoneField.value = "";
    tagInputField.value = "";

    // membershipVal
    if (membershipVal) membershipVal.destroy();
    membershipVal = new Choices(membershipField, {
        searchEnabled: false
    });

    // tagInputVal
    if (tagInputVal) tagInputVal.destroy();
    tagInputVal = new Choices(tagInputField, {
        removeItemButton: true,
    });
}


document.getElementById("showModal").addEventListener("hidden.bs.modal", function () {
    clearFields();
});


function deleteMultiple() {
    const ids_array = [];
    var items = document.getElementsByName('chk_child');
    for (i = 0; i < items.length; i++) {
        if (items[i].checked == true) {
            var trNode = items[i].parentNode.parentNode.parentNode;
            var id = trNode.querySelector("td a").innerHTML;
            ids_array.push(id);
        }
    }
    if (typeof ids_array !== 'undefined' && ids_array.length > 0) {
        Swal.fire({
            title: "Are you sure?",
            text: "You won't be able to revert this!",
            icon: "warning",
            showCancelButton: true,
            customClass: {
                confirmButton: 'btn btn-primary w-xs me-2 mt-2',
                cancelButton: 'btn btn-danger w-xs mt-2',
            },
            confirmButtonText: "Yes, delete it!",
            buttonsStyling: false,
            showCloseButton: true
        }).then(function (result) {
            if (result.value) {
                for (i = 0; i < ids_array.length; i++) {
                    customerList.remove("id", `<a href="apps-customers-overview.html" class="fw-medium link-primary">${ids_array[i]}</a>`);
                }
                document.getElementById("remove-actions").classList.add("d-none");
                document.getElementById("checkAll").checked = false;
                Swal.fire({
                    title: 'Deleted!',
                    text: 'Your data has been deleted.',
                    icon: 'success',
                    customClass: {
                        confirmButton: 'btn btn-info w-xs mt-2',
                    },
                    buttonsStyling: false
                });
            }
        });
    } else {
        Swal.fire({
            title: 'Please select at least one checkbox',
            customClass: {
                confirmButton: 'btn btn-info',
            },
            buttonsStyling: false,
            showCloseButton: true
        });
    }
}

document.querySelector(".pagination-next").addEventListener("click", function () {
    document.querySelector(".pagination.listjs-pagination") ?
        document.querySelector(".pagination.listjs-pagination").querySelector(".active") && document.querySelector(".pagination.listjs-pagination").querySelector(".active").nextElementSibling != null ?
            document.querySelector(".pagination.listjs-pagination").querySelector(".active").nextElementSibling.children[0].click() : "" : "";
    refreshCallbacks();
    ischeckboxcheck();
});

document.querySelector(".pagination-prev").addEventListener("click", function () {
    document.querySelector(".pagination.listjs-pagination") ?
        document.querySelector(".pagination.listjs-pagination").querySelector(".active") && document.querySelector(".pagination.listjs-pagination").querySelector(".active").previousSibling != null ?
            document.querySelector(".pagination.listjs-pagination").querySelector(".active").previousSibling.children[0].click() : "" : "";
    refreshCallbacks();
    ischeckboxcheck();
});
