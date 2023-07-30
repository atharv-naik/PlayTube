const leadingZeroFormatter = new Intl.NumberFormat(undefined, {
  minimumIntegerDigits: 2,
});
function formatDuration(time) {
  const seconds = Math.floor(time % 60);
  const minutes = Math.floor(time / 60) % 60;
  const hours = Math.floor(time / 3600);

  if (hours === 0) {
    return `${minutes}:${leadingZeroFormatter.format(seconds)}`;
  } else {
    return `${hours}:${leadingZeroFormatter.format(
      minutes
    )}:${leadingZeroFormatter.format(seconds)}`;
  }
}
const movieDurations = document.querySelectorAll(".movie-duration");
movieDurations.forEach((movieDuration) => {
  const duration = movieDuration.dataset.duration;
  movieDuration.innerHTML = formatDuration(duration);
});

const myMovies = document.querySelector(".my-movies");
const theme = getCookie("theme");
if (theme == "light") {
  // set light color on on-click-color property
  myMovies.style.setProperty("--on-click-color", "rgba(213, 211, 211, 0.418)");
} else {
  // set dark color on on-click-color property
  myMovies.style.setProperty("--on-click-color", "rgba(118, 117, 117, 0.318)");
}

// show movie thumbnail only after image is loaded
const movieImages = document.querySelectorAll(".movie-img");
movieImages.forEach((movieImage) => {
  movieImage.addEventListener("load", () => {
    movieImage.style.opacity = 1;
  });
});
