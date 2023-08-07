const body = document.querySelector("body");
const movies = document.querySelectorAll(".movie");

const btn = document.querySelector(".btn");
const ytLogo = document.querySelector(".yt-logo-img");

function applyThemeStyles() {
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



function redirectToSignInPage() {
  window.location.href = "{% url 'play:login' %}";
}

function redirectToLogOutPage() {
  window.location.href = "{% url 'play:logout' %}";
}

function redirectToUploadVideoPage() {
  window.location.href = "{% url 'play:upload-video' %}";
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
