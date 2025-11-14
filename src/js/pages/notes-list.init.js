/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.com
File: notes list init js
*/

var url = "/static/json/";
var allNotesList = '';
var currentPage = 1;
var itemsPerPage = 8;

var prevButton = document.getElementById('page-prev');
var nextButton = document.getElementById('page-next');

// ckeditor
var ckClassicEditor = document.getElementById("ckeditor-classic")
var editorData;
if (ckClassicEditor) {
    ClassicEditor
        .create(ckClassicEditor)
        .then(function (editor) {
            // Get the current value of the editor
            editorData = editor;
            editor.ui.view.editable.element.style.height = '200px';
            document.getElementById('addNewNote').addEventListener('hidden.bs.modal', event => {
                editor.setData('');
            });

            editItem(editor);
        })
        .catch(function (error) {
            console.error(error);
        });
}

//notes list by json
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
getJSON("notes-list.json", function (err, data) {
    if (err !== null) {
        console.log("Something went wrong: " + err);
    } else {
        allNotesList = data;
        loadNotesData(allNotesList, currentPage);
        paginationEvents();
        sortElementsById();
    }
});


var noteTitleInput = document.getElementById("noteTitle-input");
var categoryInput = document.getElementById("category-input");
var noteAuthor = document.getElementById("noteAuthor-input");
var categoryVal = new Choices(categoryInput, {
    searchEnabled: false
});

// notes ico list data
function loadNotesData(datas, page) {
    pageEvent(datas);
    var pages = Math.ceil(datas.length / itemsPerPage);
    if (page < 1) page = 1;
    if (page > pages) page = pages;

    document.querySelector("#notes-list").innerHTML = '';

    if (datas.length > 0) {
        for (var i = (page - 1) * itemsPerPage; i < (page * itemsPerPage) && (i < datas.length); i++) {
            var lockNotes = datas[i].lock != undefined ? "<i class='bi bi-lock'></i>" : "";

            document.querySelector("#notes-list").innerHTML += '<div class="col-xl-3 col-lg-4 col-sm-6">\
        <div class="card card-height-100">\
            <div class="card-body d-flex flex-column">\
                <div class="d-flex align-items-center gap-2 mb-3">\
                    '+ isCategory(datas[i].category) + '\
                    <div class="flex-shrink-0 text-muted">\
                        '+ lockNotes + '\
                    </div>\
                </div>\
                <h5 class="card-title">'+ datas[i].title + '</h5>\
                <div class="text-muted">'+ datas[i].description + '</div> \
                <div class="d-flex align-items-center gap-2 mt-auto">\
                    <img src="'+ datas[i].author[0].img + '" alt="" class="avatar-xs rounded-circle">\
                    <div class="flex-grow-1">\
                        <a href="#!"><h6 class="mb-1 fs-sm">'+ datas[i].author[0].name + '</h6></a>\
                        <p class="text-muted fs-xs fw-normal mb-0">'+ datas[i].date + '</p>\
                    </div>\
                    <div class="flex-shrink-0">\
                        <div class="dropdown">\
                            <button class="btn btn-subtle-secondary btn-sm dropdown" type="button" data-bs-toggle="dropdown" aria-expanded="false">\
                                <i class="ri-more-fill align-middle"></i>\
                            </button>\
                            <ul class="dropdown-menu dropdown-menu-end">\
                                <li><a class="dropdown-item view-item-btn" href="javascript:void(0);"><i class="ri-eye-fill align-bottom me-2 text-muted"></i> View</a></li>\
                                <li><a class="dropdown-item edit-item-btn" data-edit-id="'+ datas[i].id + '" data-bs-toggle="modal" href="#addNewNote"><i class="ri-pencil-fill align-bottom me-2 text-muted"></i> Edit</a></li>\
                                <li><a class="dropdown-item remove-item-btn" data-remove-id="'+ datas[i].id + '" data-bs-toggle="modal" href="#removeNotesModal"><i class="ri-delete-bin-fill align-bottom me-2 text-muted"></i> Delete</a></li>\
                            </ul>\
                        </div>\
                    </div>\
                </div>\
            </div>\
        </div>\
    </div>';
        }
    }

    selectedPage();
    currentPage == 1 ? prevButton.parentNode.classList.add('disabled') : prevButton.parentNode.classList.remove('disabled');
    currentPage == pages ? nextButton.parentNode.classList.add('disabled') : nextButton.parentNode.classList.remove('disabled');
    //  });
    editItem();
    removeItem();
}


function isCategory(val) {
    switch (val) {
        case "Management":
            return (
                '<div class="flex-grow-1 text-danger"><i class="bi bi-circle align-baseline me-1 fs-xs"></i>' + val + '</div>'
            );
        case "Skills":
            return (
                '<div class="flex-grow-1 text-success"><i class="bi bi-circle align-baseline me-1 fs-xs"></i>' + val + '</div>'
            );
        case "Ideas":
            return (
                '<div class="flex-grow-1 text-warning"><i class="bi bi-circle align-baseline me-1 fs-xs"></i>' + val + '</div>'
            );
        case "Prototyping":
            return (
                '<div class="flex-grow-1 text-primary"><i class="bi bi-circle align-baseline me-1 fs-xs"></i>' + val + '</div>'
            );
        case "Global":
            return (
                '<div class="flex-grow-1 text-secondary"><i class="bi bi-circle align-baseline me-1 fs-xs"></i>' + val + '</div>'
            );
        case "Development":
            return (
                '<div class="flex-grow-1 text-info"><i class="bi bi-circle align-baseline me-1 fs-xs"></i>' + val + '</div>'
            );
        case "UI UX Design":
            return (
                '<div class="flex-grow-1 text-success"><i class="bi bi-circle align-baseline me-1 fs-xs"></i>' + val + '</div>'
            );
    }
}
// create-nots 
var forms = document.querySelectorAll('.create-form')
var cnt = 11;
Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener('submit', function (event) {
        var action = document.getElementById("action").value;
        var id = document.getElementById("id").value;
        event.preventDefault();
        if (action == "edit") {
            allNotesList = allNotesList.map(function (item) {
                if (item.id == id) {
                    editList = true;
                    item.author[0].name = noteAuthor.value;
                    item.title = noteTitleInput.value;
                    item.category = categoryInput.value;
                    item.description = editorData.getData();
                }
                document.getElementById("notesModal-close").click()
                document.getElementById("action").value = "add";
                document.getElementById("addNewNoteLabel").innerHTML = "Add Notes";
                document.getElementById("addNew").innerHTML = "Save";
                loadNotesData(allNotesList, currentPage);
                return item;
            });

        } else {
            var errorMsg = document.getElementById("alert-error-msg");
            errorMsg.classList.remove("d-none");

            setTimeout(() => errorMsg.classList.add("d-none"), 2000);

            if (noteTitleInput.value == "") {
                text = "Please enter a note title";
                errorMsg.innerHTML = text;
                return false;
            } else if (categoryInput.value == "") {
                text = "Please select a category";
                errorMsg.innerHTML = text;
                return false;
            }
            document.getElementById("alert-error-msg").classList.add("d-none");
            document.getElementById("notesModal-close").click();

            var dateValue = new Date().toUTCString().slice(5, 16);

            var lockNotes = "<i class='bi bi-lock'></i>";
            document.querySelector("#notes-list").innerHTML += '<div class="col-xl-3 col-lg-4 col-sm-6">\
        <div class="card card-height-100">\
            <div class="card-body d-flex flex-column">\
                <div class="d-flex align-items-center gap-2 mb-3">\
                    '+ isCategory(categoryInput.value) + '\
                    <div class="flex-shrink-0 text-muted">\
                        '+ lockNotes + '\
                    </div>\
                </div>\
                <h5 class="card-title">'+ noteTitleInput.value + '</h5>\
                <div class="text-muted">'+ editorData.getData() + '</div> \
                <div class="d-flex align-items-center gap-2 mt-auto">\
                    <img src="/static/images/users/avatar-3.jpg" alt="" class="avatar-xs rounded-circle">\
                    <div class="flex-grow-1">\
                        <a href="#!"><h6 class="mb-1 fs-sm">'+ noteAuthor.value + '</h6></a>\
                        <p class="text-muted fs-xs fw-normal mb-0">'+ dateValue + '</p>\
                    </div>\
                    <div class="flex-shrink-0">\
                        <div class="dropdown">\
                            <button class="btn btn-subtle-secondary btn-sm dropdown" type="button" data-bs-toggle="dropdown" aria-expanded="false">\
                                <i class="ri-more-fill align-middle"></i>\
                            </button>\
                            <ul class="dropdown-menu dropdown-menu-end">\
                                <li><a class="dropdown-item view-item-btn" href="javascript:void(0);"><i class="ri-eye-fill align-bottom me-2 text-muted"></i> View</a></li>\
                                <li><a class="dropdown-item edit-item-btn" data-edit-id="'+ cnt + '" data-bs-toggle="modal" href="#addNewNote"><i class="ri-pencil-fill align-bottom me-2 text-muted"></i> Edit</a></li>\
                                <li><a class="dropdown-item remove-item-btn" data-remove-id="'+ cnt + '" data-bs-toggle="modal" href="#removeNotesModal"><i class="ri-delete-bin-fill align-bottom me-2 text-muted"></i> Delete</a></li>\
                            </ul>\
                        </div>\
                    </div>\
                </div>\
            </div>\
        </div>\
    </div>';
            allNotesList.unshift({
                id: cnt,
                category: categoryInput.value,
                title: noteTitleInput.value,
                description: editorData.getData(),
                author: [{
                    img: "/static/images/users/avatar-3.jpg",
                    name: noteAuthor.value,
                }],
                date: dateValue,
                lock: false,
            });
            cnt++;
            loadNotesData(allNotesList, currentPage);
            return true;
        }
    });

});

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

// pageEvent
function pageEvent(data) {
    if (data.length == 0) {
        document.getElementById("pagination-element").style.display = "none";
    } else {
        document.getElementById("pagination-element").style.display = "flex";
    }

    var pageNumber = document.getElementById('page-num');
    pageNumber.innerHTML = "";
    var dataPageNum = Math.ceil(data.length / itemsPerPage)
    // for each page
    for (var i = 1; i < dataPageNum + 1; i++) {
        pageNumber.innerHTML += "<div class='page-item'><a class='page-link clickPageNumber' href='javascript:void(0);'>" + i + "</a></div>";
    }
}

// paginationEvents
function paginationEvents() {
    var numPages = function numPages() {
        return Math.ceil(allNotesList.length / itemsPerPage);
    };

    function clickPage() {
        document.addEventListener('click', function (e) {
            if (e.target.nodeName == "A" && e.target.classList.contains("clickPageNumber")) {
                currentPage = e.target.textContent;
                loadNotesData(allNotesList, currentPage);
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
            loadNotesData(allNotesList, currentPage);
        }
    });

    nextButton.addEventListener('click', function () {
        if (currentPage < numPages()) {
            currentPage++;
            loadNotesData(allNotesList, currentPage);
        }
    });

    pageNumbers();
    clickPage();
    selectedPage();
}


function fetchIdFromObj(member) {
    return parseInt(member.id);
}

function findNextId() {
    if (allNotesList.length === 0) {
        return 0;
    }
    var lastElementId = fetchIdFromObj(allNotesList[allNotesList.length - 1]),
        firstElementId = fetchIdFromObj(allNotesList[0]);
    return (firstElementId >= lastElementId) ? (firstElementId + 1) : (lastElementId + 1);
}

function sortElementsById() {
    var manyallNotesList = allNotesList.sort(function (a, b) {
        var x = fetchIdFromObj(a);
        var y = fetchIdFromObj(b);

        if (x > y) {
            return -1;
        }
        if (x < y) {
            return 1;
        }
        return 0;
    })

    loadNotesData(manyallNotesList, currentPage);
}

// editItem
function editItem() {
    var getEditid = 0;
    var dateValue = new Date().toUTCString().slice(5, 16);
    Array.from(document.querySelectorAll(".edit-item-btn")).forEach(function (elem) {
        elem.addEventListener('click', function (event) {
            getEditid = elem.getAttribute('data-edit-id');
            allNotesList = allNotesList.map(function (item) {
                if (item.id == getEditid) {
                    editList = true;
                    document.getElementById("addNewNoteLabel").innerHTML = "Edit Notes";
                    document.getElementById("noteAuthor-input").value = item.author[0].name;
                    document.getElementById("noteTitle-input").value = item.title;
                    document.getElementById("category-input").value = item.category;
                    document.getElementById("ckeditor-classic").value = editorData.setData(item.description);
                    document.getElementById("addNew").innerHTML = "Update";
                    document.getElementById("action").value = "edit";
                    document.getElementById("id").value = getEditid;
                }
                return item;
            });
        });
    });
};


// removeItem
function removeItem() {
    var getid = 0;
    Array.from(document.querySelectorAll(".remove-item-btn")).forEach(function (item) {
        item.addEventListener('click', function (event) {
            document.getElementById("remove-notes").addEventListener("click", function () {
                getid = item.getAttribute('data-remove-id');
                function arrayRemove(arr, value) {

                    return arr.filter(function (ele) {
                        return ele.id != value;
                    });
                }
                var filtered = arrayRemove(allNotesList, getid);
                allNotesList = filtered;
                document.getElementById("close-removeNotesModal").click();
                loadNotesData(allNotesList, 1);
            });
        });
    });
}

// clearFields
function clearFields() {
    document.getElementById("id-field").value = "";
    document.getElementById("addNewNoteLabel").innerHTML = "Create Note";
    document.getElementById("addNew").innerHTML = "Add notes";
    noteTitleInput.value = "";
    categoryInput.value = "";
    noteAuthor.value = "";

    // membershipVal
    if (categoryVal) categoryVal.destroy();
    categoryVal = new Choices(categoryInput, {
        searchEnabled: false
    });
}

document.getElementById('addNewNote').addEventListener('hidden.bs.modal', event => {
    clearFields();
});