function redirectToURL() {
  window.location.href = "{% url 'play:home' %}";
}

// check theme
// const themeSwitcher = document.querySelector('.theme-switcher');

applyThemeStyles();
themeSwitcher.addEventListener("click", () => {
  applyThemeStyles();
});
