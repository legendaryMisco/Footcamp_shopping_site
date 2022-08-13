'use strict';



/**
 * navbar toggle
 */

const overlay = document.querySelector("[data-overlay]");
const navOpenBtn = document.querySelector("[data-nav-open-btn]");
const navbar = document.querySelector("[data-navbar]");
const navCloseBtn = document.querySelector("[data-nav-close-btn]");

const navElems = [overlay, navOpenBtn, navCloseBtn];

for (let i = 0; i < navElems.length; i++) {
  navElems[i].addEventListener("click", function () {
    navbar.classList.toggle("active");
    overlay.classList.toggle("active");
  });
}



/**
 * header & go top btn active on page scroll
 */

const header = document.querySelector("[data-header]");
const goTopBtn = document.querySelector("[data-go-top]");

window.addEventListener("scroll", function () {
  if (window.scrollY >= 80) {
    header.classList.add("active");
    goTopBtn.classList.add("active");
  } else {
    header.classList.remove("active");
    goTopBtn.classList.remove("active");
  }
});




const addToCartBtn = document.querySelectorAll(".card-action-btn");


const closeSearchPanel = document.querySelector(".close-search");
const openSearchPanel = document.querySelector(".search-btn");
const SearchPanel = document.querySelector(".search-content");

openSearchPanel.onclick = function() {
  SearchPanel.classList.add("active-search-panel")
}

closeSearchPanel.addEventListener("click", ()=> {
  SearchPanel.classList.remove("active-search-panel")
    // alert()
})

document.querySelector(".search").addEventListener("keyup", () => {
  var inputValue = document.querySelector(".search").value.toUpperCase(),
      names = document.querySelectorAll(".names");

  // LOOP THROUGH THE TEXT CONTENT OF THE LIST ITEMS
  // AND HIDE ITEMS WHOSE RESULTS DON'T MATCH.
  for (let i = 0; i < names.length; i++) {
      const element = names[i];
      
      // GRAB THE "a" TAG IN LIST ITEM
      var nameInnerText = element.getElementsByTagName("a")[0].textContent;
      var NoName = document.querySelector(".no-name");

      if (nameInnerText.toUpperCase().indexOf(inputValue) > -1) {
              element.style.display = "";
              NoName.style.display = "none"
          } else {
              element.style.display = "none";
              NoName.style.display = ""
      }
  }
})