const themeSwitcher = document.querySelector(".theme-switcher");
const body = document.querySelector("body");
const movies = document.querySelectorAll(".movie");

const btn = document.querySelector(".btn");
const ytLogo = document.querySelector(".yt-logo-img");
function applyThemeStyles() {
  let theme = getCookie("theme");
  if (theme === "light") {
    // set box shadow to dark
    btn.style.border = "none";
    btn.style.boxShadow = "0px 0px 1px 0px rgba(0, 0, 0, 0.5)";
    // set light theme not found image
    try {
      document.querySelector(".not-found-img").src =
        "https://www.youtube.com/img/desktop/unavailable/unavailable_video_dark_theme.png";
    } catch {
      console.log("not found image not found");
    }
  } else {
    // set box shadow to light
    btn.style.border = "0.5px solid rgba(96, 96, 96, 0.562)";
    btn.style.boxShadow = "0px 0px 4px 0px rgba(255, 255, 255, 0.5)";
    // set dark theme not found image
    try {
      document.querySelector(".not-found-img").src =
        "https://www.youtube.com/img/desktop/unavailable/unavailable_video_dark_theme.png";
    } catch {
      console.log("not found image not found");
    }
  }
}



// loginBtn.addEventListener("click", ()=> {
//   window.location.href = loginBtn.dataset.url;
// });

// logoutBtn.addEventListener("click", ()=> {
//   window.location.href = logoutBtn.dataset.url;
// });

// uploadVideoBtn.addEventListener("click", ()=> {
//   window.location.href = uploadVideoBtn.dataset.url;
// });

function redirectToSignInPage() {
  window.location.href = "{% url 'play:login' %}";
}

function redirectToLogOutPage() {
  window.location.href = "{% url 'play:logout' %}";
}

function redirectToUploadVideoPage() {
  window.location.href = "{% url 'play:upload-video' %}";
}

// function to switch theme
function switchTheme(transition = true) {
  if (themeSwitcher.dataset.theme === "dark") {
    themeSwitcher.dataset.theme = "light";
    saveThemePreference("light");
    // apply light theme
    body.style.backgroundColor = "#fff";
    body.style.color = "#000";
    // change body --theme-color and --theme-bc accordingly
    body.style.setProperty("--theme-color", "#000");
    body.style.setProperty("--theme-bc", "#fff");
    body.style.setProperty("--box-shadow", "0 0px 2px 0px rgba(0, 0, 0, 0.5)");
    body.style.setProperty(
      "--box-shadow-hover",
      "0 0px 4px 0px rgba(0, 0, 0, 0.5)"
    );
    if (transition) {
      body.style.transition = "all 0.5s ease-in-out";
    }
  } else {
    themeSwitcher.dataset.theme = "dark";
    saveThemePreference("dark");
    // apply dark theme
    body.style.backgroundColor = "#000";
    body.style.color = "#fff";
    // change body --theme-color and --theme-bc accordingly
    body.style.setProperty("--theme-color", "#fff");
    body.style.setProperty("--theme-bc", "#000");
    body.style.setProperty(
      "--box-shadow",
      "0 0 2px 0px rgba(255, 255, 255, 0.5)"
    );
    body.style.setProperty(
      "--box-shadow-hover",
      "0 0 4px 0px rgba(255, 255, 255, 0.5)"
    );
    if (transition) {
      body.style.transition = "all 0.5s ease-in-out";
    }
  }
}

// switch theme on click
themeSwitcher.addEventListener("click", () => {
  switchTheme();
});

// apply user's saved theme preference on page load else use device's theme preference; defaults to light theme
const savedTheme = getCookie("theme");
if (!savedTheme) {
  const prefersDarkMode =
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches;
  if (prefersDarkMode) {
    switchTheme((transition = false));
  }
}
if (savedTheme === "dark") {
  switchTheme((transition = false));
}

// Save user's theme preference when it changes
function saveThemePreference(theme) {
  setCookie("theme", theme, 30); // cookie will last for 30 days
}

// Utility function to get a cookie by name
function getCookie(name) {
  const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  if (match) {
    return match[2];
  }
}

// Utility function to set a cookie
function setCookie(name, value, days) {
  const expires = new Date(
    Date.now() + days * 24 * 60 * 60 * 1000
  ).toUTCString();
  document.cookie =
    name +
    "=" +
    encodeURIComponent(value) +
    "; expires=" +
    expires +
    "; path=/";
}

// Utility function to delete a cookie
function deleteCookie(name) {
  document.cookie = name + "=; Max-Age=-99999999;";
}

// listen for '/' key press and focus the search bar if it does
document.addEventListener("keydown", (e) => {
  const tagName = document.activeElement.tagName.toLowerCase();
  const searchBar = document.querySelector(".search-input");

  if (tagName === "input" && e.key.toLowerCase() === "escape") {
    document.activeElement.blur();
  } else if (e.key.toLowerCase() === "/") {
    e.preventDefault();
    searchBar.focus();
  }
});
