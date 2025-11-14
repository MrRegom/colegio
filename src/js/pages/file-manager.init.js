/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.com
File: file-manager init Js File
*/

// get colors array from the string
function getChartColorsArray(chartId) {
    const chartElement = document.getElementById(chartId);
    if (chartElement) {
        const colors = chartElement.dataset.colors;
        if (colors) {
            const parsedColors = JSON.parse(colors);
            const mappedColors = parsedColors.map((value) => {
                const newValue = value.replace(/\s/g, "");
                if (!newValue.includes(",")) {
                    const color = getComputedStyle(document.documentElement).getPropertyValue(newValue);
                    return color || newValue;
                } else {
                    const val = value.split(",");
                    if (val.length === 2) {
                        const rgbaColor = `rgba(${getComputedStyle(document.documentElement).getPropertyValue(val[0])}, ${val[1]})`;
                        return rgbaColor;
                    } else {
                        return newValue;
                    }
                }
            });
            return mappedColors;
        } else {
            console.warn(`data-colors attribute not found on: ${chartId}`);
        }
    }
}

var chartDonutBasicChart = "";

function loadCharts() {
    // Simple Donut Charts
    var chartDonutBasicColors = "";
    chartDonutBasicColors = getChartColorsArray("simple_dount_chart");
    if (chartDonutBasicColors) {
        var options = {
            series: [44, 55, 41, 17, 15],
            chart: {
                height: 350,
                type: 'donut',
            },
            plotOptions: {
                donut: {
                    size: '30%',
                }
            },
            labels: ["Images", "Documents", "Media Files", "Videos", "Others"],
            legend: {
                position: 'bottom'
            },
            dataLabels: {
                dropShadow: {
                    enabled: false,
                }
            },
            colors: chartDonutBasicColors
        };

        if (chartDonutBasicChart != "")
            chartDonutBasicChart.destroy();
        chartDonutBasicChart = new ApexCharts(document.querySelector("#simple_dount_chart"), options);
        chartDonutBasicChart.render();
    }

}
window.addEventListener("resize", function () {
    setTimeout(() => {
        loadCharts();
    }, 250);
});
loadCharts();

//allFiles Table
var options = {
    valueNames: [
        "docs_type",
        "document_name",
        "size",
        "file_item",
        "date"
    ],
    page: 8,
    pagination: true
};


// sortable-dropdown
var sortableDropdown = document.querySelectorAll('.sortable-dropdown');
if (sortableDropdown) {
    sortableDropdown.forEach(function (elem) {
        elem.querySelectorAll('.dropdown-menu .dropdown-item').forEach(function (item) {
            item.addEventListener('click', function () {
                var getHtml = item.innerHTML;
                elem.querySelector('.dropdown-title').innerHTML = getHtml;
            });
        });
    });
}

function windowResize() {
    var windowSize = document.documentElement.clientWidth;
    if (windowSize < 1400) {
        document.body.classList.remove("file-detail-show");
    } else {
        document.body.classList.add("file-detail-show");
    }
}

windowResize();
window.addEventListener("resize", windowResize);

//recentFiles Table
var options = {
    valueNames: [
        "docs_type",
        "document_name",
        "size",
        "file_item",
        "date"
    ],
    page: 7,
    pagination: true,
    pagination: {
        item: '<li><a class="page" href="#!"></a></li>'
    }
};

// Init list
var recentFiles = new List("recentFiles", options).on("updated", function (list) {
    list.matchingItems.length == 0 ?
        (document.getElementsByClassName("noresult")[0].style.display = "block") :
        (document.getElementsByClassName("noresult")[0].style.display = "none");

    if (list.matchingItems.length > 0) {
        document.getElementsByClassName("noresult")[0].style.display = "none";
    } else {
        document.getElementsByClassName("noresult")[0].style.display = "block";
    }
});
var editFlag = false;
function editFolderList() {
    Array.from(document.querySelectorAll(".folder-card")).forEach(function (item) {
        Array.from(item.querySelectorAll(".edit-folder-list")).forEach(function (subitem) {
            subitem.addEventListener('click', function (event) {

                var editid = item.querySelector(".card").getAttribute('id');
                var getEditid = editid.split("-")[1];
                var checkid = item.querySelector(".form-check .form-check-input").getAttribute('id')
                var getCheckid = checkid.split("_")[1];

                if (getEditid == getCheckid) {
                    editFlag = true;
                    document.getElementById("addNewFolder").innerHTML = "Save";
                    document.getElementById("createFolderModalLabel").innerHTML = "Folder Rename";
                    document.getElementById("folderid-input").value = 'folder-' + getEditid;
                    document.getElementById("foldername-input").value = item.querySelector(".folder-name").innerHTML;
                }
            });
        });
    });
};
var createFolderForms = document.querySelectorAll('.createfolder-form')
Array.prototype.slice.call(createFolderForms).forEach(function (form) {
    form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        } else {
            event.preventDefault();
            var folderName = document.getElementById("foldername-input").value;
            var uniqueid = Math.floor(Math.random() * 100);
            // program to get a random item from an array
            function getRandomItem(colorclass) {
                // get random index value
                const randomIndex = Math.floor(Math.random() * colorclass.length);
                // get random item
                const item = colorclass[randomIndex];
                return item;
            }
            var colorclass = [
                { bgcolor: "bg-danger-subtle", iconclass: "danger" },
                { bgcolor: "bg-info-subtle", iconclass: "info" },
                { bgcolor: "bg-primary-subtle", iconclass: "primary" },
                { bgcolor: "bg-secondary-subtle", iconclass: "secondary" },
            ];
            var currentitems = getRandomItem(colorclass)
            folderlisthtml =
                '<div class="col-lg-3 col-sm-6 folder-card">\
            <div class="card p-2 text-center card-animate">\
                <div class="card-body py-4 rounded-1 d-flex mb-1 '+ currentitems.bgcolor + '">\
                    <div class="avatar-md mx-auto my-3">\
                    <div class="avatar-title  bg-opacity-10 text-'+ currentitems.iconclass + ' fs-3 rounded-circle bg-' + currentitems.iconclass + '">\
                            <i class="bi bi-folder"></i>\
                        </div>\
                    </div> \
                    </div>\
                    <a href="#!" class="stretched-link">\
                                <h5 class="fs-md mb-2 pt-3">'+ folderName + '</h5>\
                            </a>\
            </div>\
        </div>';
            if (folderName !== "" && !editFlag) {
                var folderListdata = document.getElementById("folderlist-data");
                folderListdata.insertAdjacentHTML("afterbegin", folderlisthtml);
                var addFolderClose = document.getElementById("addFolderBtn-close");
                addFolderClose.click();
                editFolderList();
            } else if (folderName !== "" && editFlag) {
                var getEditid = 0;
                getEditid = document.getElementById("folderid-input").value;
                document.getElementById(getEditid).querySelector('.folder-name').innerHTML = folderName
                var addFolderClose = document.getElementById("addFolderBtn-close");
                addFolderClose.click();
                editFlag = false;
                document.getElementById("addNewFolder").innerHTML = "Add Folder";
                document.getElementById("createFolderModalLabel").innerHTML = "Create Folder";
                document.getElementById("folderid-input").value = "";
                document.getElementById("foldername-input").value = "";
            }
            document.getElementById("folderid-input").value = "";
            document.getElementById("foldername-input").value = "";
        }
        form.classList.add('was-validated');
    }, false)
});
Array.from(document.querySelectorAll(".create-folder-modal")).forEach(function (elem) {
    elem.addEventListener('click', function (event) {
        document.getElementById("addNewFolder").innerHTML = "Add Folder";
        document.getElementById("createFolderModalLabel").innerHTML = "Create Folder";
        document.getElementById("folderid-input").value = "";
        document.getElementById("foldername-input").value = "";
        document.getElementById("createfolder-form").classList.remove("was-validated");
    });
});

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
var idField = document.getElementById("id-field");
var filenameField = document.getElementById("filename-field");
var fileitemField = document.getElementById("fileitem-field");
var filesizeField = document.getElementById("filesize-field");
var filedateField = document.getElementById("filedate-field");
var removeBtns = document.getElementsByClassName("remove-item-btn");
var editBtns = document.getElementsByClassName("edit-item-btn");
var editList = false;
// File manager option
const perPage = 10;
var options = {
    valueNames: [
        "id",
        "docs_type",
        "document_name",
        "file_item",
        "size",
        "date",
    ],
    page: perPage,
    pagination: true,
    plugins: [
        ListPagination({
            left: 1,
            right: 1,
        }),
    ],
};

var FileManegerList = [
    {
        "id": "99",
        "Type": "svg",
        "Name": "home Pattern Wave.svg",
        "File_Item": "03",
        "Size": "3.87 MB",
        "date": "19 Dec, 2022"
    },
    {
        "id": "92",
        "Type": "scss",
        "Name": "_variables.scss",
        "File_Item": "013",
        "Size": "0.234 KB",
        "date": "03 April, 2023"
    },
    {
        "id": "98",
        "Type": "zip",
        "Name": "Creating judia admin websites.css",
        "File_Item": "015",
        "Size": "0.234 KB",
        "date": "03 April, 2023"
    },
    {
        "id": "1",
        "Type": "scss",
        "Name": "Figma design system tutorial.scss",
        "File_Item": "03",
        "Size": "7.95 MB",
        "date": "27 May, 2023"
    },
    {
        "id": "2",
        "Type": "test",
        "Name": "Project Documents.test",
        "File_Item": "24",
        "Size": "2.5 MB",
        "date": "15 Feb, 2023"
    },
    {
        "id": "3",
        "Type": "psd",
        "Name": "Judia Design Kit.psd",
        "File_Item": "148",
        "Size": "234.87 MB",
        "date": "29 Jan, 2023"
    },
    {
        "id": "4",
        "Type": "mp4",
        "Name": "Velzon Docs Video.mp4",
        "File_Item": "19",
        "Size": "149.33 MB",
        "date": "12 Nov, 2022"
    },
    {
        "id": "5",
        "Type": "gif",
        "Name": "Offline Pages.gif",
        "File_Item": "02",
        "Size": "0.987 MB",
        "date": "12 Nov, 2022"
    },
    {
        "id": "6",
        "Type": "svg",
        "Name": "home Pattern Wave.svg",
        "File_Item": "03",
        "Size": "3.87 MB",
        "date": "19 Dec, 2022"
    },
    {
        "id": "7",
        "Type": "scss",
        "Name": "_variables.scss",
        "File_Item": "013",
        "Size": "0.234 KB",
        "date": "03 April, 2023"
    },
    {
        "id": "8",
        "Type": "zip",
        "Name": "Creating judia admin websites.css",
        "File_Item": "015",
        "Size": "0.234 KB",
        "date": "03 April, 2023"
    },
]

// File manager Init list
const FileManeger = new List("FileManegerList", options).on("updated", (list) => {
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
    const totalRecordsElement = FileManeger.listContainer.querySelector(".total-records");
    const showingElement = FileManeger.listContainer.querySelector(".showing");

    if (totalRecordsElement) totalRecordsElement.innerHTML = FileManeger.items.length;
    if (showingElement) showingElement.innerHTML = FileManeger.visibleItems.length;
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

function isStatus(val) {
    switch (val) {
        case "scss":
            return (
                '<i class="bi bi-file-earmark-word text-info-emphasis fs-4"></i>'
            );
        case "test":
            return (
                '<i class="bi bi-filetype-pdf text-danger-emphasis fs-4"></i>'
            );
        case "psd":
            return (
                '<i class="bi bi-filetype-psd text-primary-emphasis fs-4"></i>'
            );
        case "mp4":
            return (
                '<i class="bi bi-filetype-mp4 text-warning-emphasis fs-4"></i>'
            );
        case "gif":
            return (
                '<i class="bi bi-filetype-gif text-success-emphasis fs-4"></i>'
            );
        case "scss":
            return (
                '<i class="bi bi-filetype-scss text-danger fs-4"></i>'
            );
        case "svg":
            return (
                '<i class="bi bi-filetype-svg text-secondary-emphasis fs-4"></i>'
            );
        case "zip":
            return (
                '<i class="bi bi-file-text align-bottom text-secondary fs-4"></i>'
            );
        default:
            return (
                '<i class="bi bi-file-earmark-text text-info-emphasis fs-4"></i>'
            );
    }
}

function loadFileData(datas) {
    document.querySelector("#file-list").innerHTML = '';
    var cnt = 0;
    Array.from(datas).forEach(function (element, index) {
        cnt++;
        var fileIconElm
        if (element.Name.includes(".")) {
            var fileIcon = element.Type;
        }
        fileIconElm = isStatus(fileIcon)
        FileManeger.add({
            id: element.id,
            docs_type: isStatus(element.Type),
            document_name: element.Name,
            file_item: element.File_Item,
            size: element.Size,
            date: element.date,
        });
        FileManeger.sort('id', { order: "desc" });
        refreshCallbacks();
        ischeckboxcheck();
        FileManeger.remove("id", `<a href="#" class="fw-medium link-primary">#TB01</a>`);
    });
}

loadFileData(FileManegerList);

function ischeckboxcheck() {
    Array.from(document.getElementsByName("chk_child")).forEach(function (checkbox) {
        checkbox.addEventListener("change", function (event) {
            var closestRow = event.target.closest("tr");
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
                var itemValues = FileManeger.get({
                    id: itemId,
                });
                Array.from(itemValues).forEach(function (x) {
                    var isId = new DOMParser().parseFromString(x._values.id, "text/html");
                    var selectedId = isId.body.innerHTML;
                    if (selectedId == itemId) {
                        editList = true;
                        idField.value = selectedId;
                        filenameField.value = x._values.document_name
                        fileitemField.value = x._values.file_item
                        filesizeField.value = x._values.size
                        filedateField.value = x._values.date
                        document.getElementById("addNewFile").innerHTML = "Update";
                        document.getElementById("createFileModalLabel").innerHTML = "Edit File";
                        document.getElementById("createfile-form").classList.remove("was-validated");
                    }
                });
            });
        });
    };
    document.getElementById("createFileModal").addEventListener("show.bs.modal", function (e) {
        if (e.relatedTarget.classList.contains("edit-item-btn")) {
            document.getElementById("createFileModalLabel").innerHTML = "Edit File";
            document.getElementById("addNewFile").innerHTML = "Update";
        } else if (e.relatedTarget.classList.contains("createFile-modal")) {
            document.getElementById("createFileModalLabel").innerHTML = "Add File";
            document.getElementById("addNewFile").innerHTML = "Add";
        } else {
            document.getElementById("exampleModalLabel").innerHTML = "List Customer";
        }
    });
    // removeBtns
    if (removeBtns) {
        Array.from(removeBtns).forEach(function (btn) {
            btn.addEventListener("click", function (e) {
                e.target.closest("tr").children[1].innerText;
                var removeitemId = e.target.closest("tr").querySelector("td.id").innerHTML;
                var itemValues = FileManeger.get({
                    id: removeitemId,
                });
                Array.from(itemValues).forEach(function (x) {
                    deleteid = new DOMParser().parseFromString(x._values.id, "text/html");
                    var isElem = deleteid.body.innerText;
                    var isdeleteid = deleteid.body.innerHTML;
                    if (isdeleteid == removeitemId) {
                        document.getElementById("delete-record").addEventListener("click", function () {
                            FileManeger.remove("id", removeitemId);
                            document.getElementById("deleteRecord-close").click();
                        });
                    }
                });
            });
        });
    }
}
// tablelist-form
var count = 10;
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
            { input: filenameField, error: "Please enter a file name." },
            { input: fileitemField, error: "Please enter a item name." },
            { input: filesizeField, error: "Please enter a size name." },
            { input: filedateField, error: "Please enter a date name." },
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
        // date & time
        if (!editList && allFieldsValid) {
            let fileType, fileName = filenameField.value;
            if (fileName.includes(".")) {
                fileType = fileName.split(".")[1]
            }
            FileManeger.add({
                id: count,
                docs_type: isStatus(fileType),
                document_name: filenameField.value,
                file_item: fileitemField.value,
                size: filesizeField.value + ' kb',
                date: filedateField.value,

            })
            FileManeger.sort('id', { order: "desc" });
            // document.getElementById("alert-error-msg").classList.add("d-none");
            document.getElementById("close-modal").click();
            count++;
            refreshCallbacks();
            clearFields();
            Swal.fire({
                position: 'center',
                icon: 'success',
                title: 'File name inserted successfully!',
                showConfirmButton: false,
                timer: 2000,
                showCloseButton: true
            });
        } else if (editList && allFieldsValid) {
            var editValues = FileManeger.get({
                id: idField.value,
            });
            Array.from(editValues).forEach(function (x) {
                var isId = new DOMParser().parseFromString(x._values.id, "text/html");
                var selectedId = isId.body.innerHTML;
                if (selectedId == itemId) {
                    x.values({
                        id: `<a href="#" class="fw-medium link-primary">${idField.value}</a>`,
                        document_name: filenameField.value,
                        file_item: fileitemField.value,
                        size: filesizeField.value + ' kb',
                        date: filedateField.value,
                    });
                }
            });
            editList = false;
            document.getElementById("close-modal").click();
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
    filenameField.value = "";
    fileitemField.value = "";
    filesizeField.value = "";
    filedateField.value = "";
}
function deleteMultiple() {
    const ids_array = [];
    var items = document.getElementsByName('chk_child');
    for (i = 0; i < items.length; i++) {
        if (items[i].checked == true) {
            var trNode = items[i].parentNode.parentNode.parentNode;
            var id = trNode.querySelector("td.id").innerText;
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
                cancelButton: 'btn btn-danger w-xs mt-2'
            },
            confirmButtonText: "Yes, delete it!",
            buttonsStyling: false,
            showCloseButton: true
        }).then(function (result) {
            if (result.value) {
                for (i = 0; i < ids_array.length; i++) {
                    FileManeger.remove("id", ids_array[i]);
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