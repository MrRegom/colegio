/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Version: 1.0.0
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.com
File: Main Js File
*/

(function () {
	("use strict");

	/**
	 *  global variables
	 */
	var navbarMenuHTML = document.querySelector(".navbar-menu").innerHTML;
	var default_lang = "en"; // set Default Language
	var language = localStorage.getItem("language") ?? "en";
	var languageData = '';
	var moreMenuWidth = 150;

	function initLanguage() {
		// Set new language
		(language === null) ? setLanguage(default_lang) : setLanguage(language);
		var languages = document.getElementsByClassName("language");
		languages && Array.from(languages).forEach(function (dropdown) {
			dropdown.addEventListener("click", function (event) {
				setLanguage(dropdown.getAttribute("data-lang"));
			});
		});
	}

	function setLanguage(lang) {
		if (document.getElementById("header-lang-img")) {
			const navbarMenu = document.querySelector(".navbar-menu");
			navbarMenu.classList.add("opacity-0");
			document.getElementById("header-items").classList.add("opacity-0");
			navbarMenu.innerHTML = navbarMenuHTML;
			switch (lang) {
				case "en":
					document.getElementById("header-lang-img").src = "/static/images/flags/us.svg";
					break;
				case "es":
					document.getElementById("header-lang-img").src = "/static/images/flags/spain.svg";
					break;
				case "de":
					document.getElementById("header-lang-img").src = "/static/images/flags/germany.svg";
					break;
				case "it":
					document.getElementById("header-lang-img").src = "/static/images/flags/italy.svg";
					break;
				case "ru":
					document.getElementById("header-lang-img").src = "/static/images/flags/russia.svg";
					break;
				case "zh":
					document.getElementById("header-lang-img").src = "/static/images/flags/china.svg";
					break;
				case "fr":
					document.getElementById("header-lang-img").src = "/static/images/flags/french.svg";
					break;
				case "ar":
					document.getElementById("header-lang-img").src = "/static/images/flags/ae.svg";
					break;
				default:
					document.getElementById("header-lang-img").src = "/static/images/flags/us.svg";
					lang = 'en';
					return;
			}
			localStorage.setItem("language", lang);
			language = lang;
			getLanguage();
		}
	}

	// Multi language setting
	function getLanguage() {
		language == null ? setLanguage(default_lang) : false;
		var request = new XMLHttpRequest();
		// Instantiating the request object
		request.open("GET", "/static/lang/" + language + ".json");
		// Defining event listener for readystatechange event
		request.onreadystatechange = function () {
			// Check if the request is compete and was successful
			if (this.readyState === 4 && this.status === 200) {
				languageData = JSON.parse(this.responseText);
				Object.keys(languageData).forEach(function (key) {
					var elements = document.querySelectorAll("[data-key='" + key + "']");
					Array.from(elements).forEach(function (elem) {
						elem.textContent = languageData[key];
					});
				});
				navbarMenuHTML = document.querySelector(".navbar-menu").innerHTML
				// if (sessionStorage.getItem("data-layout") == "horizontal") {
				updateHorizontalMenus();
				(document.documentElement.clientWidth < 1025) ? windowResizeHover() : '';
				// }
			}
		};
		// Sending the request to the server
		request.send();
	}

	function pluginData() {
		/**
		 * Common plugins
		 */
		/**
		 * Toast UI Notification
		 */
		var toastExamples = document.querySelectorAll("[data-toast]");
		Array.from(toastExamples).forEach(function (element) {
			element.addEventListener("click", function () {
				var toastData = {};
				var isToastVal = element.attributes;
				if (isToastVal["data-toast-text"])
					toastData.text = isToastVal["data-toast-text"].value.toString();
				if (isToastVal["data-toast-gravity"])
					toastData.gravity = isToastVal["data-toast-gravity"].value.toString();
				if (isToastVal["data-toast-position"])
					toastData.position = isToastVal["data-toast-position"].value.toString();
				if (isToastVal["data-toast-className"])
					toastData.className = isToastVal["data-toast-className"].value.toString();
				if (isToastVal["data-toast-duration"])
					toastData.duration = isToastVal["data-toast-duration"].value.toString();
				if (isToastVal["data-toast-close"])
					toastData.close = isToastVal["data-toast-close"].value.toString();
				if (isToastVal["data-toast-style"])
					toastData.style = isToastVal["data-toast-style"].value.toString();
				if (isToastVal["data-toast-offset"])
					toastData.offset = isToastVal["data-toast-offset"];

				Toastify({
					newWindow: true,
					text: toastData.text,
					gravity: toastData.gravity,
					position: toastData.position,
					className: "bg-" + toastData.className,
					stopOnFocus: true,
					offset: {
						x: toastData.offset ? 50 : 0, // horizontal axis - can be a number or a string indicating unity. eg: '2em'
						y: toastData.offset ? 10 : 0, // vertical axis - can be a number or a string indicating unity. eg: '2em'
					},
					duration: toastData.duration,
					close: toastData.close == "close" ? true : false,
					style: toastData.style == "style" ? {
						background: "linear-gradient(to right, #0AB39C, #405189)"
					} : "",
				}).showToast();
			});
		});

		/**
		 * Choices Select plugin
		 */
		var choicesExamples = document.querySelectorAll("[data-choices]");
		Array.from(choicesExamples).forEach(function (item) {
			var choiceData = {};
			var isChoicesVal = item.attributes;
			if (isChoicesVal["data-choices-groups"])
				choiceData.placeholderValue = "This is a placeholder set in the config";
			if (isChoicesVal["data-choices-search-false"])
				choiceData.searchEnabled = false;
			if (isChoicesVal["data-choices-search-true"])
				choiceData.searchEnabled = true;
			if (isChoicesVal["data-choices-removeItem"])
				choiceData.removeItemButton = true;
			if (isChoicesVal["data-choices-sorting-false"])
				choiceData.shouldSort = false;
			if (isChoicesVal["data-choices-sorting-true"])
				choiceData.shouldSort = true;
			if (isChoicesVal["data-choices-multiple-remove"])
				choiceData.removeItemButton = true;
			if (isChoicesVal["data-choices-limit"])
				choiceData.maxItemCount = isChoicesVal["data-choices-limit"].value.toString();
			if (isChoicesVal["data-choices-limit"])
				choiceData.maxItemCount = isChoicesVal["data-choices-limit"].value.toString();
			if (isChoicesVal["data-choices-editItem-true"])
				choiceData.maxItemCount = true;
			if (isChoicesVal["data-choices-editItem-false"])
				choiceData.maxItemCount = false;
			if (isChoicesVal["data-choices-text-unique-true"])
				choiceData.duplicateItemsAllowed = false;
			if (isChoicesVal["data-choices-text-disabled-true"])
				choiceData.addItems = false;
			isChoicesVal["data-choices-text-disabled-true"] ? new Choices(item, choiceData).disable() : new Choices(item, choiceData);
		});

		/**
		 * flatpickr
		 */
		var flatpickrExamples = document.querySelectorAll("[data-provider]");
		Array.from(flatpickrExamples).forEach(function (item) {
			if (item.getAttribute("data-provider") == "flatpickr") {
				var dateData = {};
				var isFlatpickerVal = item.attributes;
				if (isFlatpickerVal["data-date-format"])
					dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
				if (isFlatpickerVal["data-enable-time"]) {
					(dateData.enableTime = true),
						(dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString() + " H:i");
				}
				if (isFlatpickerVal["data-altFormat"]) {
					(dateData.altInput = true),
						(dateData.altFormat = isFlatpickerVal["data-altFormat"].value.toString());
				}
				if (isFlatpickerVal["data-minDate"]) {
					dateData.minDate = isFlatpickerVal["data-minDate"].value.toString();
					dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
				}
				if (isFlatpickerVal["data-maxDate"]) {
					dateData.maxDate = isFlatpickerVal["data-maxDate"].value.toString();
					dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
				}
				if (isFlatpickerVal["data-default-date"]) {
					dateData.defaultDate = isFlatpickerVal["data-default-date"].value.toString();
					dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
				}
				if (isFlatpickerVal["data-multiple-date"]) {
					dateData.mode = "multiple";
					dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
				}
				if (isFlatpickerVal["data-range-date"]) {
					dateData.mode = "range";
					dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
				}
				if (isFlatpickerVal["data-inline-date"]) {
					(dateData.inline = true),
						(dateData.defaultDate = isFlatpickerVal["data-default-date"].value.toString());
					dateData.dateFormat = isFlatpickerVal["data-date-format"].value.toString();
				}
				if (isFlatpickerVal["data-disable-date"]) {
					var dates = [];
					dates.push(isFlatpickerVal["data-disable-date"].value);
					dateData.disable = dates.toString().split(",");
				}
				if (isFlatpickerVal["data-week-number"]) {
					var dates = [];
					dates.push(isFlatpickerVal["data-week-number"].value);
					dateData.weekNumbers = true
				}
				flatpickr(item, dateData);
			} else if (item.getAttribute("data-provider") == "timepickr") {
				var timeData = {};
				var isTimepickerVal = item.attributes;
				if (isTimepickerVal["data-time-basic"]) {
					(timeData.enableTime = true),
						(timeData.noCalendar = true),
						(timeData.dateFormat = "H:i");
				}
				if (isTimepickerVal["data-time-hrs"]) {
					(timeData.enableTime = true),
						(timeData.noCalendar = true),
						(timeData.dateFormat = "H:i"),
						(timeData.time_24hr = true);
				}
				if (isTimepickerVal["data-min-time"]) {
					(timeData.enableTime = true),
						(timeData.noCalendar = true),
						(timeData.dateFormat = "H:i"),
						(timeData.minTime = isTimepickerVal["data-min-time"].value.toString());
				}
				if (isTimepickerVal["data-max-time"]) {
					(timeData.enableTime = true),
						(timeData.noCalendar = true),
						(timeData.dateFormat = "H:i"),
						(timeData.minTime = isTimepickerVal["data-max-time"].value.toString());
				}
				if (isTimepickerVal["data-default-time"]) {
					(timeData.enableTime = true),
						(timeData.noCalendar = true),
						(timeData.dateFormat = "H:i"),
						(timeData.defaultDate = isTimepickerVal["data-default-time"].value.toString());
				}
				if (isTimepickerVal["data-time-inline"]) {
					(timeData.enableTime = true),
						(timeData.noCalendar = true),
						(timeData.defaultDate = isTimepickerVal["data-time-inline"].value.toString());
					timeData.inline = true;
				}
				flatpickr(item, timeData);
			}
		});

		// Dropdown
		const dropdownMenuLinks = document.querySelectorAll('.dropdown-menu a[data-bs-toggle="tab"]');
		dropdownMenuLinks.forEach(function (link) {
			link.addEventListener("click", function (event) {
				event.preventDefault();
				event.stopPropagation();
				const targetTab = bootstrap.Tab.getInstance(link);
				targetTab.show();
			});
		});
	}

	// on click collapse menu
	function isCollapseMenu() {
		/**
		 * Sidebar menu collapse
		 */
		const collapses = document.querySelectorAll(".navbar-nav .collapse");
		if (collapses) {
			collapses.forEach(function (collapse) {
				// Init collapses
				const collapseInstance = new bootstrap.Collapse(collapse, {
					toggle: false,
				});

				// Hide sibling collapses on `show.bs.collapse`
				collapse.addEventListener("show.bs.collapse", function (e) {
					e.stopPropagation();
					var closestCollapse = collapse.parentElement.closest(".collapse");
					if (closestCollapse) {
						var siblingCollapses = closestCollapse.querySelectorAll(".collapse");
						siblingCollapses.forEach(function (siblingCollapse) {
							var siblingCollapseInstance = bootstrap.Collapse.getInstance(siblingCollapse);
							if (siblingCollapseInstance === collapseInstance) {
								return;
							}
							siblingCollapseInstance.hide();
						});
					} else {
						var getSiblings = function (elem) {
							var siblings = [];
							var sibling = elem.parentNode.firstChild;
							while (sibling) {
								if (sibling.nodeType === 1 && sibling !== elem) {
									siblings.push(sibling);
								}
								sibling = sibling.nextSibling;
							}
							return siblings;
						};
						var siblings = getSiblings(collapse.parentElement);
						siblings.forEach(function (item) {
							if (item.childNodes.length > 2)
								item.firstElementChild.setAttribute("aria-expanded", "false");
							var ids = item.querySelectorAll("*[id]");
							ids.forEach(function (item1) {
								item1.classList.remove("show");
								if (item1.childNodes.length > 2) {
									var val = item1.querySelectorAll("ul li a");
									val.forEach(function (subitem) {
										if (subitem.hasAttribute("aria-expanded"))
											subitem.setAttribute("aria-expanded", "false");
									});
								}
							});
						});
					}
				});
			});
		}
	}


	//  Search menu dropdown on Topbar
	function isCustomDropdown() {
		//Search bar
		var searchOptions = document.getElementById("search-close-options");
		var dropdown = document.getElementById("search-dropdown");
		var searchInput = document.getElementById("search-options");
		if (searchInput) {
			searchInput.addEventListener("focus", function () {
				var inputLength = searchInput.value.length;
				if (inputLength > 0) {
					dropdown.classList.add("show");
					searchOptions.classList.remove("d-none");
				} else {
					dropdown.classList.remove("show");
					searchOptions.classList.add("d-none");
				}
			});

			searchInput.addEventListener("keyup", function (event) {
				var inputLength = searchInput.value.length;
				if (inputLength > 0) {
					dropdown.classList.add("show");
					searchOptions.classList.remove("d-none");

					var inputVal = searchInput.value.toLowerCase();
					var notifyItem = document.getElementsByClassName("notify-item");

					Array.from(notifyItem).forEach(function (element) {
						var notifyText = ''
						if (element.querySelector("h6")) {
							var spanText = element.getElementsByTagName("span")[0].innerText.toLowerCase()
							var name = element.querySelector("h6").innerText.toLowerCase()
							if (name.includes(inputVal)) {
								notifyText = name
							} else {
								notifyText = spanText
							}
						} else if (element.getElementsByTagName("span")) {
							notifyText = element.getElementsByTagName("span")[0].innerText.toLowerCase()
						}

						if (notifyText) {
							if (notifyText.includes(inputVal)) {
								element.classList.add("d-block");
								element.classList.remove("d-none");
							} else {
								element.classList.remove("d-block");
								element.classList.add("d-none");
							}
						}

						Array.from(document.getElementsByClassName("notification-group-list")).forEach(function (element) {
							if (element.querySelectorAll(".notify-item.d-block").length == 0) {
								element.querySelector(".notification-title").style.display = 'none'
							} else {
								element.querySelector(".notification-title").style.display = 'block'
							}
						});
					});
				} else {
					dropdown.classList.remove("show");
					searchOptions.classList.add("d-none");
				}
			});

			searchOptions.addEventListener("click", function () {
				searchInput.value = "";
				dropdown.classList.remove("show");
				searchOptions.classList.add("d-none");
			});

			document.body.addEventListener("click", function (e) {
				if (e.target.getAttribute("id") !== "search-options") {
					dropdown.classList.remove("show");
					searchOptions.classList.add("d-none");
				}
			});
		}
	}
	//  search menu dropdown on topbar
	function isCustomDropdownResponsive() {
		//Search bar
		var searchOptions = document.getElementById("search-close-options");
		var dropdownResponsive = document.getElementById("search-dropdown-reponsive");
		var searchInputResponsive = document.getElementById("search-options-reponsive");

		if (searchOptions && dropdownResponsive && searchInputResponsive) {
			searchInputResponsive.addEventListener("focus", function () {
				var inputLength = searchInputResponsive.value.length;
				if (inputLength > 0) {
					dropdownResponsive.classList.add("show");
					searchOptions.classList.remove("d-none");
				} else {
					dropdownResponsive.classList.remove("show");
					searchOptions.classList.add("d-none");
				}
			});

			searchInputResponsive.addEventListener("keyup", function () {
				var inputLength = searchInputResponsive.value.length;
				if (inputLength > 0) {
					dropdownResponsive.classList.add("show");
					searchOptions.classList.remove("d-none");
				} else {
					dropdownResponsive.classList.remove("show");
					searchOptions.classList.add("d-none");
				}
			});

			searchOptions.addEventListener("click", function () {
				searchInputResponsive.value = "";
				dropdownResponsive.classList.remove("show");
				searchOptions.classList.add("d-none");
			});

			document.body.addEventListener("click", function (e) {
				if (e.target.getAttribute("id") !== "search-options") {
					dropdownResponsive.classList.remove("show");
					searchOptions.classList.add("d-none");
				}
			});
		}
	}

	function initLeftMenuCollapse() {
		/**
		 * Vertical layout menu scroll add
		 */
		if (document.documentElement.getAttribute("data-layout") == "vertical") {
			if (document.querySelector(".navbar-menu")) {
				document.querySelector(".navbar-menu").innerHTML = navbarMenuHTML;
			}
			document.getElementById("scrollbar").setAttribute("data-simplebar", "");
			document.getElementById("navbar-nav").setAttribute("data-simplebar", "");
			document.getElementById("scrollbar").classList.add("h-100");
		}

		/**
		 * Horizontal layout menu
		 */
		if (document.documentElement.getAttribute("data-layout") == "horizontal") {
			updateHorizontalMenus();
		}
	}

	function isLoadBodyElement() {
		var verticalOverlay = document.getElementsByClassName("vertical-overlay");
		if (verticalOverlay) {
			Array.from(verticalOverlay).forEach(function (element) {
				element.addEventListener("click", function () {
					document.body.classList.remove("vertical-sidebar-enable");
					if (sessionStorage.getItem("data-layout") == "twocolumn")
						document.body.classList.add("twocolumn-panel");
					else
						document.documentElement.setAttribute("data-sidebar-size", sessionStorage.getItem("data-sidebar-size"));
				});
			});
		}
	}

	function windowResizeHover() {
		var windowSize = document.documentElement.clientWidth;
		const navbarMenu = document.querySelector(".navbar-menu");
		if (windowSize < 1025 && windowSize > 767) {

			if (navbarMenu) {
				navbarMenu.innerHTML = navbarMenuHTML;
			}
			// isCollapseMenu();
			// initActiveMenu();

			if (sessionStorage.getItem("data-layout") == "vertical") {
				document.documentElement.setAttribute("data-sidebar-size", "sm-hover");
			}

			if (document.querySelector(".hamburger-icon")) {
				document.querySelector(".hamburger-icon").classList.add("open");
			}
		} else if (windowSize >= 1025) {

			if (sessionStorage.getItem("data-layout") == "horizontal") {
				updateHorizontalMenus();
			}

			if (document.querySelector(".hamburger-icon")) {
				document.querySelector(".hamburger-icon").classList.remove("open");
			}

			if (sessionStorage.getItem("data-layout") == "vertical") {
				document.documentElement.setAttribute("data-sidebar-size", sessionStorage.getItem("data-sidebar-size"));
			}
		} else if (windowSize <= 767) {
			document.body.classList.remove("vertical-sidebar-enable");
			if (navbarMenu) {
				navbarMenu.innerHTML = navbarMenuHTML;
			}

			if (sessionStorage.getItem("data-layout") != "horizontal") {
				document.documentElement.setAttribute("data-sidebar-size", "lg");
			}

			if (document.querySelector(".hamburger-icon")) {
				document.querySelector(".hamburger-icon").classList.add("open");
			}
		}
		menuPosSetOnClickNHover();
	}

	function menuPosSetOnClickNHover() {
		const isElement = document.querySelectorAll("#navbar-nav > li.nav-item");
		Array.from(isElement).forEach(function (item) {
			item.addEventListener("click", menuItem.bind(this), false);
			item.addEventListener("mouseover", menuItem.bind(this), false);
		});
	}

	// menu item range outside the window
	function menuItem(e) {
		// get the dropdown menu element
		var dropdownMenu = e.target;
		const subMenus = (dropdownMenu.nextElementSibling) ? dropdownMenu.nextElementSibling : dropdownMenu.parentElement.nextElementSibling;
		if (dropdownMenu && subMenus) {
			// get the position and dimensions of the dropdown menu
			var dropdownOffset = subMenus.getBoundingClientRect();
			var dropdownWidth = subMenus.offsetWidth;
			var dropdownHeight = subMenus.offsetHeight;

			// get the dimensions of the screen
			var screenWidth = window.innerWidth;
			var screenHeight = window.innerHeight;

			// calculate the maximum x and y coordinates of the dropdown menu
			var maxDropdownX = dropdownOffset.left + dropdownWidth;
			var maxDropdownY = dropdownOffset.top + dropdownHeight;

			// check if the dropdown menu goes outside the screen
			var isDropdownOffScreen = (maxDropdownX > screenWidth) || (maxDropdownY > screenHeight);

			if (isDropdownOffScreen) {
				if (subMenus.classList.contains("menu-dropdown")) {
					subMenus.classList.add("dropdown-custom-right");
				}
			}
		}
	}

	function toggleHamburgerMenu() {
		const dataLayout = document.documentElement.getAttribute("data-layout");
		const windowSize = document.documentElement.clientWidth;

		if (dataLayout === "vertical") {
			if (windowSize <= 1025 && windowSize > 767) {
				document.body.classList.add("vertical-sidebar-enable");
				sessionStorage.getItem("data-sidebar-size") == "lg" ?
					setAttrItemAndTag("data-sidebar-size", "lg") : setAttrItemAndTag("data-sidebar-size", "lg")
			} else if (windowSize > 1025) {
				document.body.classList.remove("vertical-sidebar-enable");
				sessionStorage.getItem("data-sidebar-size") == "lg" ?
					setAttrItemAndTag("data-sidebar-size", "sm-hover") : setAttrItemAndTag("data-sidebar-size", "lg")
			} else if (windowSize <= 767) {
				document.body.classList.add("vertical-sidebar-enable");
				setAttrItemAndTag("data-sidebar-size", "lg")
			}
			document.querySelector(".hamburger-icon").classList.toggle("open");
		} else {
			if (windowSize > 767)
				document.querySelector(".hamburger-icon").classList.toggle("open");

			//For collapse horizontal menu
			document.body.classList.contains("menu") ? document.body.classList.remove("menu") : document.body.classList.add("menu");
		}
	}

	function windowLoadContent() {
		window.addEventListener("resize", windowResizeHover);
		windowResizeHover();

		document.addEventListener("scroll", function () {
			windowScroll();
		});

		window.addEventListener("load", function () {
			initActiveMenu();
			isLoadBodyElement();
			// addEventListenerOnSmHoverMenu();

			if (window.scrollY > 0)
				windowScroll();
		});

		if (document.getElementById("topnav-hamburger-icon")) {
			document.getElementById("topnav-hamburger-icon").addEventListener("click", toggleHamburgerMenu);
		}

		document.body.addEventListener('click', function (event) {
			(!event.target.closest("#navbar-header")) ? document.body.classList.remove("menu") : '';
		});
	}

	// page topbar class added
	function windowScroll() {
		var pageTopbar = document.getElementById("page-topbar");
		if (pageTopbar) {
			document.body.scrollTop >= 20 || document.documentElement.scrollTop >= 20 ? pageTopbar.classList.add("topbar-shadow") : pageTopbar.classList.remove("topbar-shadow");
		}
	}

	// menu active js
	function initActiveMenu() {
		var currentPath = location.pathname == "/" ? "index.html" : location.pathname.substring(1);
		currentPath = currentPath.substring(currentPath.lastIndexOf("/") + 1);
		if (currentPath) {
			// navbar-nav
			var a = document.getElementById("navbar-nav").querySelector('[href="' + currentPath + '"]');
			if (a) {
				a.classList.add("active");
				var parentCollapseDiv = a.closest(".collapse.menu-dropdown");
				if (parentCollapseDiv) {
					parentCollapseDiv.classList.add("show");
					parentCollapseDiv.parentElement.children[0].classList.add("active");
					parentCollapseDiv.parentElement.children[0].setAttribute("aria-expanded", "true");
					if (parentCollapseDiv.parentElement.closest(".collapse.menu-dropdown")) {
						parentCollapseDiv.parentElement.closest(".collapse").classList.add("show");
						if (parentCollapseDiv.parentElement.closest(".collapse").previousElementSibling)
							parentCollapseDiv.parentElement.closest(".collapse").previousElementSibling.classList.add("active");

						if (parentCollapseDiv.parentElement.parentElement.parentElement.parentElement.closest(".collapse.menu-dropdown")) {
							parentCollapseDiv.parentElement.parentElement.parentElement.parentElement.closest(".collapse").classList.add("show");
							if (parentCollapseDiv.parentElement.parentElement.parentElement.parentElement.closest(".collapse").previousElementSibling) {

								parentCollapseDiv.parentElement.parentElement.parentElement.parentElement.closest(".collapse").previousElementSibling.classList.add("active");
								// if ((document.documentElement.getAttribute("data-layout") == "horizontal") && parentCollapseDiv.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.closest(".collapse")) {
								parentCollapseDiv.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.closest(".collapse").previousElementSibling.classList.add("active")
								// }
							}
						}
					}
				}
			}
		}
	}

	function initComponents() {
		// tooltip
		const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

		tooltipTriggerList.forEach(function (tooltipTriggerEl) {
			new bootstrap.Tooltip(tooltipTriggerEl);
		});

		const popoverTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="popover"]'));

		popoverTriggerList.forEach(function (popoverTriggerEl) {
			new bootstrap.Popover(popoverTriggerEl);
		});
	}

	// Counter Number
	function counter() {
		const counters = document.querySelectorAll(".counter-value");
		const speed = 250;

		if (counters.length) {
			counters.forEach((counter) => {
				const target = +counter.getAttribute("data-target");
				const inc = target / speed;

				let count = 0;
				const updateCount = () => {
					count += inc;
					if (count < target) {
						counter.innerText = numberWithCommas(count.toFixed(0));
						setTimeout(updateCount, 1);
					} else {
						counter.innerText = numberWithCommas(target);
					}
				};
				updateCount();
			});
		}

		function numberWithCommas(x) {
			return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
		}
	}

	function updateHorizontalMenus() {

		const navbarMenu = document.querySelector(".navbar-menu");
		if (navbarMenu) {
			navbarMenu.innerHTML = navbarMenuHTML;
		}
		const navbarNav = document.getElementById("navbar-header");

		// count width of horizontal menu
		const headerLogo = document.getElementById("header-logo")?.clientWidth ?? 0;
		const headerItems = document.getElementById("header-items")?.clientWidth ?? 0;
		const fullWidthOfMenu = navbarNav.clientWidth - headerLogo - headerItems - moreMenuWidth;
		const extraMenuName = languageData ? languageData["t-more"] : "More";
		const dataLayout = document.documentElement.getAttribute("data-layout");
		const menuData = document.querySelectorAll("ul.navbar-nav > li.nav-item");
		let newMenus = "";
		let splitItem = "";
		let menusWidth = 0;

		Array.prototype.forEach.call(menuData, function (item, index) {
			menusWidth += item.offsetWidth;
			if (menusWidth > fullWidthOfMenu && fullWidthOfMenu != 0 && dataLayout && dataLayout !== "vertical") {
				newMenus += item.outerHTML;
				item.remove();
			} else {
				splitItem = item;
			}

			if (index + 1 === menuData.length) {
				if (splitItem.insertAdjacentHTML && newMenus) {
					splitItem.insertAdjacentHTML(
						"afterend",
						'<li class="nav-item">\
						<a class="nav-link menu-link" href="#sidebarMore" data-bs-toggle="collapse" role="button" aria-expanded="false" aria-controls="sidebarMore">\
							<i class="ri-briefcase-2-line"></i> <span data-key="t-more">' + extraMenuName + '</span>\
						</a>\
						<div class="collapse menu-dropdown dropdown-custom-right" id="sidebarMore"><ul class="nav nav-sm flex-column">' + newMenus + "</ul></div>\
					</li>"
					);
				}
			}
		});

		if (dataLayout === "vertical")
			document.getElementById("scrollbar").setAttribute("data-simplebar", "");
		else
			document.getElementById("scrollbar").removeAttribute("data-simplebar", "");

		menuPosSetOnClickNHover();
		initActiveMenu();
		navbarMenu.classList.remove("opacity-0");
		document.getElementById("header-items").classList.remove("opacity-0");
	}

	function setAttrItemAndTag(dataAttr, dataValue) {
		document.documentElement.setAttribute(dataAttr, dataValue);
		getElementUsingTagname(dataAttr, dataValue);
		sessionStorage.setItem(dataAttr, dataValue);
	}

	function hideShowLayoutOptions(dataLayout) {
		if (dataLayout == "vertical") {
			if (document.querySelector(".navbar-menu")) {
				document.querySelector(".navbar-menu").innerHTML = navbarMenuHTML;
			}
			if (document.getElementById("theme-settings-offcanvas")) {
				document.getElementById("sidebar-size").style.display = "block";
				document.getElementById("sidebar-color").style.display = "block";
				document.getElementById("layout-position").style.display = "block";
				document.getElementById("layout-width").style.display = "block";
			}
			initLeftMenuCollapse();
			initActiveMenu();
			// addEventListenerOnSmHoverMenu();
			initMenuItemScroll();
		} else if (dataLayout == "horizontal") {
			updateHorizontalMenus();
			if (document.getElementById("theme-settings-offcanvas")) {
				document.getElementById("sidebar-size").style.display = "none";
				document.getElementById("sidebar-color").style.display = "none";
				document.getElementById("layout-position").style.display = "block";
				document.getElementById("layout-width").style.display = "block";
			}
			initActiveMenu();
		}
	}

	// add listener Sidebar Hover icon on change layout from setting
	// function addEventListenerOnSmHoverMenu() {
	// 	document.getElementById("vertical-hover").addEventListener("click", function () {
	// 		if (document.documentElement.getAttribute("data-sidebar-size") === "sm-hover") {
	// 			document.documentElement.setAttribute("data-sidebar-size", "sm-hover-active");
	// 		} else if (document.documentElement.getAttribute("data-sidebar-size") === "sm-hover-active") {
	// 			document.documentElement.setAttribute("data-sidebar-size", "sm-hover");
	// 		} else {
	// 			document.documentElement.setAttribute("data-sidebar-size", "sm-hover");
	// 		}
	// 	});
	// }

	// set full layout
	function layoutSwitch(isLayoutAttributes) {
		switch (isLayoutAttributes) {
			case isLayoutAttributes:
				switch (isLayoutAttributes["data-layout"]) {
					case "vertical":
						setAttrItemAndTag("data-layout", "vertical");
						hideShowLayoutOptions("vertical");
						isCollapseMenu();
						break;
					case "horizontal":
						setAttrItemAndTag("data-layout", "horizontal");
						hideShowLayoutOptions("horizontal");
						break;
					default:
						if (sessionStorage.getItem("data-layout") == "vertical" && sessionStorage.getItem("data-layout")) {
							setAttrItemAndTag("data-layout", "vertical");
							hideShowLayoutOptions("vertical");
							isCollapseMenu();
						} else if (sessionStorage.getItem("data-layout") == "horizontal") {
							setAttrItemAndTag("data-layout", "horizontal");
							hideShowLayoutOptions("horizontal");
						}
						break;
				}
				switch (isLayoutAttributes["data-topbar"]) {
					case "light":
						setAttrItemAndTag("data-topbar", "light");
						break;
					case "dark":
						setAttrItemAndTag("data-topbar", "dark");
						break;
					case "brand":
						setAttrItemAndTag("data-topbar", "brand");
						break;
					default:
						setAttrItemAndTag("data-topbar", "light");
						break;
				}
				switch (isLayoutAttributes["data-topbar-image"]) {
					case "pattern-1":
						setAttrItemAndTag("data-topbar-image", "pattern-1");
						break;
					case "pattern-2":
						setAttrItemAndTag("data-topbar-image", "pattern-2");
						break;
					case "pattern-3":
						setAttrItemAndTag("data-topbar-image", "pattern-3");
						break;
					default:
						sessionStorage.getItem("data-topbar-image") ?? "pattern-1";
						break;
				}

				switch (isLayoutAttributes["data-bs-theme"]) {
					case "light":
						setAttrItemAndTag("data-bs-theme", "light");
						break;
					case "dark":
						setAttrItemAndTag("data-bs-theme", "dark");
						break;
					case "brand":
						setAttrItemAndTag("data-bs-theme", "brand");
						break;
					default:
						setAttrItemAndTag("data-bs-theme", "light");
						break;
				}

				switch (isLayoutAttributes["data-layout-width"]) {
					case "fluid":
						setAttrItemAndTag("data-layout-width", "fluid");
						break;
					case "boxed":
						setAttrItemAndTag("data-layout-width", "boxed");
						break;
					default:
						setAttrItemAndTag("data-layout-width", sessionStorage.getItem("data-layout-width") ?? "fluid");
						break;
				}
				switch (isLayoutAttributes["data-sidebar-size"]) {
					case "lg":
						setAttrItemAndTag("data-sidebar-size", "lg");
						break;

					case "md":
						setAttrItemAndTag("data-sidebar-size", "md");
						break;

					case "sm-hover":
						setAttrItemAndTag("data-sidebar-size", "sm-hover");
						break;

					default:
						setAttrItemAndTag("data-sidebar-size", sessionStorage.getItem("data-sidebar-size") ?? "lg");
						break;
				}
				switch (isLayoutAttributes["data-sidebar"]) {
					case "light":
						setAttrItemAndTag("data-sidebar", "light");
						break;
					case "dark":
						setAttrItemAndTag("data-sidebar", "dark");
						break;
					case "gradient":
						setAttrItemAndTag("data-sidebar", "gradient");
						break;
					case "gradient-2":
						setAttrItemAndTag("data-sidebar", "gradient-2");
						break;
					case "gradient-3":
						setAttrItemAndTag("data-sidebar", "gradient-3");
						break;
					case "gradient-4":
						setAttrItemAndTag("data-sidebar", "gradient-4");
						break;
					default:
						setAttrItemAndTag("data-sidebar", sessionStorage.getItem("data-sidebar") ?? "light");
						break;
				}
				switch (isLayoutAttributes["data-card-layout"]) {
					case "borderless":
						setAttrItemAndTag("data-card-layout", "borderless");
						break;
					case "border":
						setAttrItemAndTag("data-card-layout", "border");
						break;
					default:
						setAttrItemAndTag("data-card-layout", sessionStorage.getItem("data-card-layout") ?? "borderless");
						break;
				}

				switch (isLayoutAttributes["data-layout-position"]) {
					case "fixed":
						setAttrItemAndTag("data-layout-position", "fixed");
						break;
					case "scrollable":
						setAttrItemAndTag("data-layout-position", "scrollable");
						break;
					default:
						setAttrItemAndTag("data-layout-position", sessionStorage.getItem("data-layout-position") ?? "fixed");
						break;
				}

				switch (isLayoutAttributes["data-layout-position"]) {
					case "fixed":
						setAttrItemAndTag("data-layout-position", "fixed");
						break;
					case "scrollable":
						setAttrItemAndTag("data-layout-position", "scrollable");
						break;
					default:
						setAttrItemAndTag("data-layout-position", sessionStorage.getItem("data-layout-position") ?? "fixed");
						break;
				}
				switch (isLayoutAttributes["data-preloader"]) {
					case "disable":
						setAttrItemAndTag("data-preloader", "disable");
						break;
					case "enable":
						preloaderEnable();
						break;
					default:
						if (sessionStorage.getItem("data-preloader") && sessionStorage.getItem("data-preloader") == "disable") {
							setAttrItemAndTag("data-preloader", "disable");
						} else if (sessionStorage.getItem("data-preloader") == "enable") {
							preloaderEnable();
						} else {
							document.documentElement.setAttribute("data-preloader", "disable");
						}
						break;
				}

			default:
				break;
		}
	}

	function preloaderEnable() {
		setAttrItemAndTag("data-preloader", "enable");
		var preloader = document.getElementById("preloader");
		if (preloader) {
			window.addEventListener("load", function () {
				preloader.style.opacity = "0";
				preloader.style.visibility = "hidden";
			});
		}
	}

	function initMenuItemScroll() {
		setTimeout(function () {
			var sidebarMenu = document.getElementById("navbar-nav");
			if (sidebarMenu) {
				var activeMenu = sidebarMenu.querySelector(".nav-item .active");
				var offset = activeMenu ? activeMenu.offsetTop : 0;
				if (offset > 300) {
					var verticalMenu = document.getElementsByClassName("app-menu") ? document.getElementsByClassName("app-menu")[0] : "";
					if (verticalMenu && verticalMenu.querySelector(".simplebar-content-wrapper")) {
						setTimeout(function () {
							offset == 330 ?
								(verticalMenu.querySelector(".simplebar-content-wrapper").scrollTop = offset + 85) :
								(verticalMenu.querySelector(".simplebar-content-wrapper").scrollTop = offset);
						}, 0);
					}
				}
			}
		}, 250);
	}

	// add change event listener on right layout setting
	function getElementUsingTagname(ele, val) {
		const inputs = Array.from(document.querySelectorAll(`input[name="${ele}"]`));

		inputs.forEach(function (x) {
			x.checked = val === x.value;
			x.addEventListener("change", function () {
				document.documentElement.setAttribute(ele, x.value);
				sessionStorage.setItem(ele, x.value);

				if (ele === "data-bs-theme") {
					// const colorButton = x.value === "light" ? document.getElementById("topbar-color-light")?.click() :
					// 	document.getElementById("topbar-color-dark")?.click();
					if (x.value === "light") {
						document.getElementById("topbar-color-dark")?.click();
						document.getElementById("sidebar-color-light")?.click();
					} else if (x.value === "dark") {
						document.getElementById("topbar-color-dark")?.click();
						document.getElementById("sidebar-color-dark")?.click();
					} else if (x.value === "brand") {
						document.getElementById("topbar-color-brand")?.click();
						document.getElementById("sidebar-color-dark")?.click();
					} else {
						document.getElementById("topbar-color-dark")?.click();
						document.getElementById("sidebar-color-light")?.click();
					}
					window.dispatchEvent(new Event("resize"));
				}

				if (ele == "data-layout-width" && x.value == "boxed") {
					document.documentElement.setAttribute("data-sidebar-size", "sm-hover");
					sessionStorage.setItem("data-sidebar-size", "sm-hover");
					document.getElementById("sidebar-size-small-hover").checked = true;
				} else if (ele == "data-layout-width" && x.value == "fluid") {
					document.documentElement.setAttribute("data-sidebar-size", "lg");
					sessionStorage.setItem("data-sidebar-size", "lg");
					document.getElementById("sidebar-size-default").checked = true;
				}

				if (ele == "data-layout") {
					if (x.value == "vertical") {
						hideShowLayoutOptions("vertical");
						isCollapseMenu();
					} else if (x.value == "horizontal") {
						hideShowLayoutOptions("horizontal");
					}
				}

				if (ele === "data-card-layout") {
					if (x.value === "borderless") {
						document.documentElement.setAttribute("data-card-layout", "borderless");
					} else if (x.value === "border") {
						document.documentElement.setAttribute("data-card-layout", "border");
					} else {
						document.documentElement.setAttribute("data-card-layout", "borderless");
					}
					window.dispatchEvent(new Event("resize"));
				}


				if (ele === "data-preloader") {
					const preloader = document.getElementById("preloader");
					if (x.value === "enable" && preloader) {
						document.documentElement.setAttribute("data-preloader", "enable");
						setTimeout(() => {
							preloader.style.opacity = "0";
							preloader.style.visibility = "hidden";
							document.getElementById("customizerclose-btn").click();
						}, 1000);
					} else if (x.value === "disable") {
						document.documentElement.setAttribute("data-preloader", "disable");
						document.getElementById("customizerclose-btn").click();
					}
				}
				if (ele === "data-layout-width") {
					updateHorizontalMenus();
				}
			});
		});
	}

	function setDefaultAttribute() {
		if (!sessionStorage.getItem("defaultAttribute")) {
			var attributesValue = document.documentElement.attributes;
			var isLayoutAttributes = {};
			Array.from(attributesValue).forEach(function (x) {
				if (x && x.nodeName && x.nodeName != "undefined") {
					var nodeKey = x.nodeName;
					isLayoutAttributes[nodeKey] = x.nodeValue;
					sessionStorage.setItem(nodeKey, x.nodeValue);
				}
			});
			sessionStorage.setItem("defaultAttribute", JSON.stringify(isLayoutAttributes));
			layoutSwitch(isLayoutAttributes);

			// open right sidebar on first time load
			var offCanvas = document.querySelector('.btn[data-bs-target="#theme-settings-offcanvas"]');
			offCanvas && offCanvas.click();
		} else {
			var isLayoutAttributes = {};
			var attributesToRetrieve = [
				'data-layout',
				'data-sidebar',
				'data-card-layout',
				'data-sidebar-size',
				"data-bs-theme",
				"data-layout-width",
				"data-layout-position",
				"data-topbar",
				"data-topbar-image",
				"data-preloader",
			];
			attributesToRetrieve.forEach(function (attribute) {
				isLayoutAttributes[attribute] = sessionStorage.getItem(attribute);
			});
			layoutSwitch(isLayoutAttributes);
		}
	}

	function initFullScreen() {
		const fullscreenBtn = document.querySelector('[data-toggle="fullscreen"]');
		if (fullscreenBtn) {
			fullscreenBtn.addEventListener("click", function (e) {
				e.preventDefault();
				document.body.classList.toggle("fullscreen-enable");

				if (!document.fullscreenElement &&
					!document.mozFullScreenElement &&
					!document.webkitFullscreenElement &&
					!document.msFullscreenElement) {
					// current working methods
					if (document.documentElement.requestFullscreen) {
						document.documentElement.requestFullscreen();
					} else if (document.documentElement.mozRequestFullScreen) {
						document.documentElement.mozRequestFullScreen();
					} else if (document.documentElement.webkitRequestFullscreen) {
						document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
					} else if (document.documentElement.msRequestFullscreen) {
						document.documentElement.msRequestFullscreen();
					}
				} else {
					if (document.exitFullscreen) {
						document.exitFullscreen();
					} else if (document.mozCancelFullScreen) {
						document.mozCancelFullScreen();
					} else if (document.webkitExitFullscreen) {
						document.webkitExitFullscreen();
					} else if (document.msExitFullscreen) {
						document.msExitFullscreen();
					}
				}
			});
		}

		document.addEventListener("fullscreenchange", exitHandler);
		document.addEventListener("webkitfullscreenchange", exitHandler);
		document.addEventListener("mozfullscreenchange", exitHandler);
		document.addEventListener("MSFullscreenChange", exitHandler);

		function exitHandler() {
			if (!document.fullscreenElement &&
				!document.mozFullScreenElement &&
				!document.webkitFullscreenElement &&
				!document.msFullscreenElement) {
				document.body.classList.remove("fullscreen-enable");
			}
		}
	}

	function setLayoutMode(mode, modeType, modeTypeId, html) {
		const isModeTypeId = document.getElementById(modeTypeId);
		html.setAttribute(mode, modeType);
		if (isModeTypeId) {
			document.getElementById(modeTypeId).click();
		}
	}

	function initModeSetting() {
		const html = document.documentElement;
		const lightDarkModeItems = document.querySelectorAll("#light-dark-mode .dropdown-item");

		lightDarkModeItems.forEach(item => {
			item.addEventListener("click", event => {
				const { mode } = item.dataset;

				if (html.hasAttribute("data-bs-theme") && mode !== "auto") {
					setLayoutMode("data-bs-theme", mode, `layout-mode-${mode}`, html);
					sessionStorage.setItem("data-layout-auto", "false");
				} else if (html.hasAttribute("data-bs-theme") && mode === "auto") {
					const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");
					const modeValue = prefersDarkScheme.matches ? "dark" : "light";

					setLayoutMode("data-bs-theme", modeValue, `layout-mode-${modeValue}`, html);
					sessionStorage.setItem("data-layout-auto", "true");
				}

				html.classList.toggle("mode-auto", sessionStorage.getItem("data-layout-auto") === "true");
			});
		});

		html.classList.toggle("mode-auto", sessionStorage.getItem("data-layout-auto") === "true");
	}

	function resetLayout() {
		const resetLayoutButton = document.getElementById("reset-layout");
		if (resetLayoutButton) {
			resetLayoutButton.addEventListener("click", function () {
				sessionStorage.clear();
				location.reload();
			});
		}
	}

	// mark all read
	if (document.getElementById("markRead")) {
		document.getElementById("markRead").addEventListener("click", function () {
			var notiElement = document.getElementById("notificationItemsTabContent");
			if (notiElement) {
				Array.from(notiElement.querySelectorAll(".notification-item.unread-message")).forEach((item) => {
					item.classList.remove("unread-message");
				});
			}
		});
	}

	// mark all clear
	if (document.getElementById("deleteAllNotification")) {
		document.getElementById("deleteAllNotification").addEventListener("click", function () {
			var notiElement = document.getElementById("notificationItemsTabContent");
			if (notiElement) {
				Array.from(notiElement.querySelectorAll(".notification-item")).forEach((item) => {
					item.remove();

					// change count
					if (document.querySelectorAll(".notification-badge")) {
						Array.from(document.querySelectorAll(".notification-badge")).forEach((count) => {
							count.innerHTML = 0;
						})
					}
					//
					document.querySelector('.empty-notification-elem').classList.remove("d-none");
				});
			}
		});
	}

	// input spin
	function inputSpinComponents() {
		isData();
		function isData() {
			var plus = document.getElementsByClassName('plus');
			var minus = document.getElementsByClassName('minus');
			var product = document.getElementsByClassName("product");

			if (plus) {
				Array.from(plus).forEach(function (e) {
					e.addEventListener('click', function (event) {
						if (parseInt(e.previousElementSibling.value) < event.target.previousElementSibling.getAttribute('max')) {
							event.target.previousElementSibling.value++;
							if (product) {
								Array.from(product).forEach(function (x) {
									updateQuantity(event.target);
								})
							}
						}
					});
				});
			}

			if (minus) {
				Array.from(minus).forEach(function (e) {
					e.addEventListener('click', function (event) {
						if (parseInt(e.nextElementSibling.value) > event.target.nextElementSibling.getAttribute('min')) {
							event.target.nextElementSibling.value--;
							if (product) {
								Array.from(product).forEach(function (x) {
									updateQuantity(event.target);
								})
							}
						}
					});
				});
			}
		}
	}

	function init() {
		setDefaultAttribute();
		isCustomDropdown();
		isCustomDropdownResponsive();
		initFullScreen();
		initModeSetting();
		windowLoadContent();
		counter();
		initComponents();
		resetLayout();
		pluginData();
		initLanguage();
		isCollapseMenu();
		inputSpinComponents();
	}
	init();

	var timeOutFunctionId;

	function setResize() {
		var currentLayout = document.documentElement.getAttribute("data-layout");
		if (currentLayout !== "horizontal") {
			if (document.getElementById("navbar-nav")) {
				var simpleBar = new SimpleBar(document.getElementById("navbar-nav"));
				if (simpleBar) simpleBar.getContentElement();
			}
			clearTimeout(timeOutFunctionId);
		}
	}

	window.addEventListener("resize", function () {
		if (timeOutFunctionId) clearTimeout(timeOutFunctionId);
		timeOutFunctionId = setTimeout(setResize, 2000);
	});

})();


//
/********************* scroll top js ************************/
//

const myButton = document.getElementById("back-to-top");

if (myButton) {
	// Show the button when the user scrolls down 100px from the top of the document
	window.addEventListener('scroll', function () {
		if (window.scrollY > 100) {
			myButton.style.display = "block";
		} else {
			myButton.style.display = "none";
		}
	});

	// Scroll to the top of the document when the user clicks on the button
	myButton.addEventListener('click', function () {
		window.scrollTo({
			top: 0,
			behavior: "smooth"
		});
	});
}