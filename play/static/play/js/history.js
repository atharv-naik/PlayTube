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
  
  // show movie thumbnail only after image is loaded
  const movieImages = document.querySelectorAll(".movie-img");
  movieImages.forEach((movieImage) => {
    movieImage.addEventListener("load", () => {
      movieImage.style.opacity = 1;
    });
  });
  