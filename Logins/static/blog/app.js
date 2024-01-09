function InvalidForm() {
  alert("Invalid Form");
}

let rememberMe = document.getElementById("remember-me");

rememberMe.style.opacity = 0;
document.getElementById("floatingPassword").addEventListener("focus", () => {
  rememberMe.style.opacity = 100;
});
