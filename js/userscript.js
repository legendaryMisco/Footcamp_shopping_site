const loginCoverBtn = document.querySelector(".login-cover-btn")
const signupCoverBtn = document.querySelector(".signup-cover-btn")
const loginCover = document.querySelector(".login-cover")
const signupCover = document.querySelector(".signup-cover");

loginCoverBtn.addEventListener("click", (e) => {
    loginCover.classList.add("active-cover");
    signupCover.classList.remove("active-cover")
})

signupCoverBtn.addEventListener("click", (e) => {
    loginCover.classList.remove("active-cover");
    signupCover.classList.add("active-cover")
})