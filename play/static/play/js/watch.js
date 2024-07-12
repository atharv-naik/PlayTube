const playPauseBtn = document.querySelector(".play-pause-btn");
const theaterBtn = document.querySelector(".theater-btn");
const fullScreenBtn = document.querySelector(".full-screen-btn");
const miniPlayerBtn = document.querySelector(".mini-player-btn");
const muteBtn = document.querySelector(".mute-btn");
const captionsBtn = document.querySelector(".captions-btn");
const speedBtn = document.querySelector(".speed-btn");
const currentTimeElem = document.querySelector(".current-time");
const totalTimeElem = document.querySelector(".total-time");
const previewImg = document.querySelector(".preview-img");
const thumbnailImg = document.querySelector(".thumbnail-img");
const volumeSlider = document.querySelector(".volume-slider");
const videoContainer = document.querySelector(".video-container");
const timelineContainer = document.querySelector(".timeline-container");
const previewTimeStamp = document.querySelector(".preview-time-stamp");
const video = document.querySelector("video");
const volumeUpBtn = document.querySelector(".volume-up-animation-icon");
const volumeDawnBtn = document.querySelector(".volume-dawn-animation-icon");
const volumeMuteBtn = document.querySelector(".volume-mute-animation-icon");
const subtitlesBtn = document.querySelector(".subtitle-toggle-animation-btn");
const playBtn = document.querySelector(".play-animation-btn");
const pauseBtn = document.querySelector(".pause-animation-btn");
const circle = document.querySelector(".center-animations-circle");
const loadingSpinner = document.querySelector(".loading-spinner");
const ptpPlayer = document.querySelector("#ptp-player");
const ambientLight = document.querySelector(".ptp-ambient-light");
const leftContainer = document.querySelector(".container-left");

let clickTimer;
const delay = 200;

function handleSingleClick(func) {
  clearTimeout(clickTimer);

  clickTimer = setTimeout(() => {
    func();
  }, delay);
}

function handleDoubleClick(func) {
  clearTimeout(clickTimer);

  func();
}

document.addEventListener("keydown", (e) => {
  const tagName = document.activeElement.tagName.toLowerCase();

  if (tagName === "input") return;

  switch (e.key.toLowerCase()) {
    case " ":
      e.preventDefault();
      if (tagName === "button") return;
    case "k":
      togglePlay();
      showControls();
      break;
    case "f":
      toggleFullScreenMode();
      break;
    case "t":
      document.exitFullscreen();
      toggleTheaterMode();
      break;
    case "i":
      toggleMiniPlayerMode();
      break;
    case "m":
      toggleMute();
      showControls();
      showVolumeAnimation((increase = true), (showMute = video.muted));
      break;
    case "arrowleft":
      skip(-5);
      showControls();
      break;
    case "j":
      skip(-10);
      showControls();
      break;
    case "arrowright":
      skip(5);
      showControls();
      break;
    case "l":
      skip(10);
      showControls();
      break;
    case "c":
      toggleCaptions();
      showControls();
      break;
    case "arrowup":
      // prevent default scrolling
      e.preventDefault();
      changeVolume(0.05);
      showControls();
      // showVolumeAnimation((increase = true));
      break;
    case "arrowdown":
      // prevent default scrolling
      e.preventDefault();
      changeVolume(-0.05);
      showControls();
      // showVolumeAnimation((increase = false));
      break;
    case "0":
    case "1":
    case "2":
    case "3":
    case "4":
    case "5":
    case "6":
    case "7":
    case "8":
    case "9": {
      const percent = (video_duration * Number(e.key)) / 10;
      skipTo(percent);
      showControls();
      break;
    }
    case "home":
      skipTo(0);
      showControls();
      break;
    case "end":
      skipTo(video_duration);
      showControls();
      break;
    case ">":
      changePlaybackSpeed();
      showControls();
      break;
    case "<":
      changePlaybackSpeed((forward = false));
      showControls();
      break;
    case ".":
      if (video.paused) skip(1 / 61);
      showControls();
      break;
    case ",":
      if (video.paused) skip(-1 / 61);
      showControls();
      break;
  }
});

// Timeline
timelineContainer.addEventListener("mousemove", handleTimelineUpdate);
timelineContainer.addEventListener("mousedown", toggleScrubbing);
document.addEventListener("mouseup", (e) => {
  if (isScrubbing) toggleScrubbing(e);
});
document.addEventListener("mousemove", (e) => {
  if (isScrubbing) handleTimelineUpdate(e);
});

let isScrubbing = false;
let wasPaused;
function toggleScrubbing(e) {
  video.currentTime;
  const rect = timelineContainer.getBoundingClientRect();
  const percent = Math.min(Math.max(0, e.x - rect.x), rect.width) / rect.width;
  previewTimeStamp.textContent = formatDuration(percent * video_duration);
  isScrubbing = (e.buttons & 1) === 1;
  videoContainer.classList.toggle("scrubbing", isScrubbing);
  if (isScrubbing) {
    wasPaused = video.paused;
    video.pause();
  } else {
    video.currentTime = percent * video_duration;
    if (!wasPaused) video.play();
  }

  handleTimelineUpdate(e);
}

function handleTimelineUpdate(e) {
  const rect = timelineContainer.getBoundingClientRect();
  var percent = Math.min(Math.max(0, e.x - rect.x), rect.width) / rect.width;
  previewTimeStamp.textContent = formatDuration(percent * video_duration);
  const previewImgNumber = Math.max(
    1,
    Math.floor((percent * video_duration) / 10)
  );
  const previewImgSrc = `${stream_url}/preview_images/preview${previewImgNumber}.jpg`;
  previewImg.src = previewImgSrc;
  if (isScrubbing) {
    e.preventDefault();
    thumbnailImg.src = previewImgSrc;
    timelineContainer.style.setProperty("--progress-position", percent);
  }

  timelineContainer.style.setProperty("--preview-position", percent);
}

// Show Loading Spinner while video is buffering
video.addEventListener("waiting", () => {
  loadingSpinner.style.display = "block";
});

video.addEventListener("canplay", () => {
  loadingSpinner.style.display = "none";
});

// Show amount of video loaded on seek bar
video.addEventListener("progress", () => {
  const duration = video_duration;
  if (duration > 0) {
    let percent = 0;
    for (let i = 0; i < video.buffered.length; i++) {
      if (
        video.buffered.start(video.buffered.length - 1 - i) < video.currentTime
      ) {
        percent = Math.max(
          percent,
          video.buffered.end(video.buffered.length - 1 - i) / duration
        );
        // break;
      }
    }
    timelineContainer.style.setProperty("--buffer-position", percent);
  }
});

// Playback Speed

function changePlaybackSpeed(forward = true) {
  if (forward) {
    let newPlaybackRate = video.playbackRate + 0.25;
    if (newPlaybackRate > 2) return;
    video.playbackRate = newPlaybackRate;

    showCurrentPlaybackSpeed(newPlaybackRate);
  } else {
    let newPlaybackRate = video.playbackRate - 0.25;
    if (newPlaybackRate < 0.25) return;
    video.playbackRate = newPlaybackRate;

    showCurrentPlaybackSpeed(newPlaybackRate);
  }
}

// Captions
// check if captions are available
let captionsUnavailable = false;
function toggleCaptions() {
  if (captionsUnavailable) return;

  // showSubtitleAnimation();

  if (hls.subtitleDisplay) {
    hls.subtitleDisplay = false;
    showCurrentSubtitle("Off");
  } else {
    hls.subtitleDisplay = true;
    showCurrentSubtitle("English");
  }
}

video.addEventListener("loadedmetadata", () => {
  if (hls.subtitleTracks.length > 0) {
    hls.subtitleTrack = 0;
    hls.subtitleDisplay = false;
    captionsBtn.addEventListener("click", toggleCaptions);
  } else {
    captionsBtn.style.opacity = "0.65";
    captionsUnavailable = true;
  }
});

// Disable hindi audio track
video.addEventListener("loadedmetadata", () => {
  // check if multiple audio tracks are available
  try {
    if (video.audioTracks.length > 1) {
      // disable hindi audio track
      for (let i = 0; i < video.audioTracks.length; i += 1) {
        if (video.audioTracks[i].language === "hin") {
          video.audioTracks[i].enabled = false;
        } else {
          video.audioTracks[i].enabled = true;
        }
      }
    }
  } catch (err) {
    console.log(err);
  }
});

function enableNextAudioTrack() {
  try {
    if (video.audioTracks.length > 1) {
      let len = video.audioTracks.length;
      // enable the next audio track and disable the current one
      for (let i = 0; i < len; i += 1) {
        if (video.audioTracks[i].enabled) {
          video.audioTracks[(i + 1) % len].enabled = true;
          video.audioTracks[i].enabled = false;
          skip(0); // to update the audio track
          break;
        }
      }
    }
  } catch (err) {
    console.log(err);
  }
}

function showSubtitleAnimation() {
  // hide all animation icons
  playBtn.style.display = "none";
  pauseBtn.style.display = "none";
  circle.style.display = "none";
  circle.style.animation = "";
  volumeUpBtn.style.display = "none";
  volumeDawnBtn.style.display = "none";
  volumeMuteBtn.style.display = "none";
  subtitlesBtn.style.display = "none";

  // show subtitle animation
  subtitlesBtn.style.display = "block";
  circle.style.display = "block";
  circle.style.animation = "dropOut 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)";
  // remove animation after it is done
  circle.addEventListener("animationend", () => {
    circle.style.display = "none";
    circle.style.animation = "";
    subtitlesBtn.style.display = "none";
  });
}

// Duration

video.addEventListener("timeupdate", () => {
  currentTimeElem.textContent = formatDuration(video.currentTime);
  const percent = video.currentTime / video_duration;
  timelineContainer.style.setProperty("--progress-position", percent);
});

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

function skip(duration) {
  video.currentTime += duration;
}

function skipTo(timeStamp) {
  video.currentTime = timeStamp;
}

// Volume

function changeVolume(percentDelta) {
  // showVolumeAnimation();
  video.volume = Math.min(Math.max(0, video.volume + percentDelta), 1);
}

muteBtn.addEventListener("click", toggleMute);
volumeSlider.addEventListener("input", (e) => {
  video.volume = e.target.value;
  video.muted = e.target.value === 0;
});

function toggleMute() {
  video.muted = !video.muted;
}

function showVolumeAnimation(increase = true, showMute = false) {
  // hide all animation icons
  volumeUpBtn.style.display = "none";
  volumeDawnBtn.style.display = "none";
  volumeMuteBtn.style.display = "none";
  circle.style.display = "none";
  circle.style.animation = "";
  playBtn.style.display = "none";
  pauseBtn.style.display = "none";
  subtitlesBtn.style.display = "none";

  if (showMute) {
    volumeMuteBtn.style.display = "block";
    circle.style.display = "block";
    circle.style.animation =
      "dropOut 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)";
    // remove animation after it is done
    circle.addEventListener("animationend", () => {
      circle.style.display = "none";
      circle.style.animation = "";
      volumeMuteBtn.style.display = "none";
    });
    return;
  }
  if (increase) {
    volumeUpBtn.style.display = "block";
    circle.style.display = "block";
    circle.style.animation =
      "dropOut 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)";
    // remove animation after it is done
    circle.addEventListener("animationend", () => {
      circle.style.display = "none";
      circle.style.animation = "";
      volumeUpBtn.style.display = "none";
    });
  } else {
    if (video.volume === 0) {
      volumeMuteBtn.style.display = "block";
      circle.style.display = "block";
      circle.style.animation =
        "dropOut 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)";
      // remove animation after it is done
      circle.addEventListener("animationend", () => {
        circle.style.display = "none";
        circle.style.animation = "";
        volumeMuteBtn.style.display = "none";
      });
    } else {
      volumeDawnBtn.style.display = "block";
      circle.style.display = "block";
      circle.style.animation =
        "dropOut 1s cubic-bezier(0.25, 0.46, 0.45, 0.94)";
      // remove animation after it is done
      circle.addEventListener("animationend", () => {
        circle.style.display = "none";
        circle.style.animation = "";
        volumeDawnBtn.style.display = "none";
      });
    }
  }
}

video.addEventListener("volumechange", () => {
  volumeSlider.value = video.volume;
  let volumeLevel;
  if (video.muted || video.volume === 0) {
    volumeSlider.value = 0;
    volumeLevel = "muted";
  } else if (video.volume >= 0.5) {
    volumeLevel = "high";
  } else {
    volumeLevel = "low";
  }

  videoContainer.dataset.volumeLevel = volumeLevel;
});

// View Modes
theaterBtn.addEventListener("click", toggleTheaterMode);
fullScreenBtn.addEventListener("click", toggleFullScreenMode);
miniPlayerBtn.addEventListener("click", toggleMiniPlayerMode);

// double click to toggle fullscreen mode
// liste for double click event
video.addEventListener(
  "dblclick",
  handleDoubleClick.bind(null, toggleFullScreenMode)
);

function toggleTheaterMode() {
  videoContainer.classList.toggle("theater");
  ptpPlayer.classList.toggle("theater");
  leftContainer.classList.toggle("theater");
  // thumbnailImg.classList.toggle("theater")
}

function toggleFullScreenMode() {
  if (document.fullscreenElement == null) {
    videoContainer.requestFullscreen();

    // try switching orientation to landscape on mobile
    try {
      screen.orientation.lock("landscape");
    } catch (err) {
      // pass
    }

    // hide mini player and theater buttons
    miniPlayerBtn.style.display = "none";
    theaterBtn.style.display = "none";
  } else {
    document.exitFullscreen();

    // try switching orientation to portrait on mobile
    try {
      screen.orientation.lock("portrait");
    } catch (err) {
      // pass
    }

    // show mini player and theater buttons only if device is not mobile
    // check if device is mobile
    if (window.innerWidth < 900) {
      miniPlayerBtn.style.display = "none";
      theaterBtn.style.display = "none";
    } else {
      miniPlayerBtn.style.display = "block";
      theaterBtn.style.display = "block";
    }
  }
}

function toggleMiniPlayerMode() {
  if (videoContainer.classList.contains("mini-player")) {
    document.exitPictureInPicture();
  } else {
    video.requestPictureInPicture();
  }
}

document.addEventListener("fullscreenchange", () => {
  videoContainer.classList.toggle("full-screen", document.fullscreenElement);
});

video.addEventListener("enterpictureinpicture", () => {
  videoContainer.classList.add("mini-player");
});

video.addEventListener("leavepictureinpicture", () => {
  videoContainer.classList.remove("mini-player");
});

// Play/Pause
playPauseBtn.addEventListener("click", togglePlay);
video.addEventListener("click", handleSingleClick.bind(null, togglePlay));

function togglePlay() {
  if (video.paused) {
    video.play();
  } else {
    video.pause();
  }
}

// Handle Mouse inactivity to hide controls
// first check if the video is playing
const videoControls = document.querySelector(".video-controls-container");
const videoTitle = document.querySelector(".video-title-container");
let timeout = undefined;

function hideControls() {
  // hide only if not hovering over controls
  if (!videoControls.matches(":hover") && !videoTitle.matches(":hover")) {
    videoControls.style.opacity = "0";
    videoTitle.style.opacity = "0";
    // hide cursor
    if (
      videoContainer.matches(":hover") &&
      document.body.style.cursor !== "none"
    ) {
      document.body.style.cursor = "none";
    }
  }
}

function showControls() {
  videoControls.style.opacity = "1";
  videoTitle.style.opacity = "1";
  // show cursor
  if (document.body.style.cursor === "none") {
    document.body.style.cursor = "default";
  }

  // if the video is playing, hide controls after 3 seconds
  if (!video.paused) {
    // clear previous timeout
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(hideControls, 5000);
  }
}

function toggleAmbientMode() {
  ambientLight.classList.toggle("show");
}

// ambient light handler
var ambientLightCanvas = document.createElement("canvas");
var ambientLightCtx = ambientLightCanvas.getContext("2d");
function ambientLightHandler() {
  ambientLightCtx.drawImage(
    video,
    0,
    0,
    ambientLightCanvas.width,
    ambientLightCanvas.height
  );
  var videoFrameImage = ambientLightCanvas.toDataURL("image/jpeg", 0.1);
  // attach as background-image to ptp-ambient-light
  ambientLight.style.backgroundImage = `url(${videoFrameImage})`;
}

video.addEventListener("play", function () {
  const interval = 1000 / video.playbackRate; // Adjust frame capture rate

  setInterval(ambientLightHandler, interval);
});

document.addEventListener("DOMContentLoaded", function () {
  var header = document.querySelector(".website-header");
  var scrollPosition = window.scrollY;

  function updateHeaderOpacity() {
    var newOpacity = Math.min(1, scrollPosition / 30);
    header.style.backgroundColor = "rgba(13, 13, 13, " + newOpacity + ")";
  }

  window.addEventListener("scroll", function () {
    scrollPosition = window.scrollY;
    updateHeaderOpacity();
  });

  updateHeaderOpacity(); // Call initially to set opacity based on initial scroll position
});

videoContainer.addEventListener("mousemove", () => {
  if (!video.paused) {
    clearTimeout(timeout);
    showControls();
    // timeout = setTimeout(hideControls, 5000);
  }
});

video.addEventListener("play", () => {
  videoContainer.classList.remove("paused");
});

video.addEventListener("pause", () => {
  videoContainer.classList.add("paused");
  clearTimeout(timeout);
  showControls();
});

// // video loading animation
// const loading = document.querySelector(".loading");
// video.addEventListener("waiting", () => {
//   loading.style.display = "block";
// });

// video.addEventListener("canplay", () => {
//   loading.style.display = "none";
// });

// toggle control buttons panel
function toggleSettingsMenu() {
  const settingsMenu = document.querySelector(".ptp-settings");
  settingsMenu.classList.toggle("show");

  closeSubmenu();
}

function closeSubmenu() {
  const ptpSubmenu = document.querySelector(".ptp-panel-submenu");
  ptpSubmenu.style.display = "none";
  const mainmenu = document.querySelector(".ptp-panel-menu");
  mainmenu.style.display = "flex";

  // close all submenus
  const submenus = document.querySelectorAll(".ptp-submenu");
  submenus.forEach((submenu) => {
    submenu.style.display = "none";
  });
}

function hideMainMenu() {
  const manMenu = document.querySelector(".ptp-panel-menu");
  manMenu.style.display = "none";
}

function showSubMenu(obj) {
  const ptpSubmenu = document.querySelector(".ptp-panel-submenu");
  ptpSubmenu.style.display = "flex";

  const classname = obj.id;
  const submenu = document.querySelector(`.${classname}`);
  hideMainMenu();
  submenu.style.display = "flex";
}

function getBackToMainMenu() {
  closeSubmenu();
  const mainmenu = document.querySelector(".ptp-panel-menu");
  mainmenu.style.display = "flex";
}

function changeVideoQuality(quality) {
  console.log(quality);
  let level;
  if (quality === "720p") {
    level = 2;
  } else if (quality === "480p") {
    level = 1;
  } else if (quality === "240p") {
    level = 0;
  } else {
    level = -1;

    currentTime = video.currentTime;
    paused = video.paused;

    hls.destroy();

    hls = new Hls();
    hls.loadSource(videoSrc);
    hls.attachMedia(video);

    hls.on(Hls.Events.MANIFEST_PARSED, function (event, data) {
      skipTo(currentTime);
      if (paused) video.pause();
      else video.play();
    });

    showCurrentVideoQuality(quality);
    return;
  }

  hls.autoLevelEnabled = "false";

  hls.currentLevel = level;
  console.log(hls.currentLevel);

  showCurrentVideoQuality(quality);
}

function showCurrentVideoQuality(quality) {
  const currentQuality = document.querySelector(".ptp-current-quality");
  currentQuality.textContent = capitalize(quality);

  // remove current-quality-tick from all qualities
  const qualities = document.querySelectorAll(".ptp-quality .ptp-submenu-item");
  qualities.forEach((quality) => {
    quality.classList.remove("selected");
  });

  // add current-quality-tick to the selected quality
  const selectedQuality = document.querySelector(`.quality-${quality}`);

  selectedQuality.classList.add("selected");
}

function setPlaybackSpeed(speed) {
  const video = document.querySelector("video");
  if (speed === "normal" || speed === 1) {
    video.playbackRate = 1;
  } else {
    video.playbackRate = speed;
  }
  showCurrentPlaybackSpeed(speed);
}

function showCurrentPlaybackSpeed(speed) {
  speed = speed.toString();
  if (speed === "1") {
    speed = "normal";
  }

  const currentSpeed = document.querySelector(".ptp-current-playback-speed");
  currentSpeed.textContent = capitalize(speed);

  // format speed to match the class name
  speed = speed.replace(".", "-");

  // remove current-speed-tick from all speeds
  const speeds = document.querySelectorAll(
    ".ptp-playback-speed .ptp-submenu-item"
  );
  speeds.forEach((item) => {
    item.classList.remove("selected");
  });

  // add current-speed-tick to the selected speed
  console.log(speed);
  const selectedSpeed = document.querySelector(`.pb_${speed}`);

  selectedSpeed.classList.add("selected");
}

function subtitlesHandler(state) {
  if (state.toLowerCase() === "off") {
    hls.subtitleDisplay = false;
  } else {
    hls.subtitleDisplay = true;
  }

  showCurrentSubtitle(state);
}

function showCurrentSubtitle(state) {
  const currentSubtitle = document.querySelector(".ptp-current-subtitle");
  currentSubtitle.textContent = capitalize(state);

  // remove current-subtitle-tick from all states
  const states = document.querySelectorAll(".ptp-subtitles .ptp-submenu-item");
  states.forEach((item) => {
    item.classList.remove("selected");
  });

  // add current-subtitle-tick to the selected state
  const selectedState = document.querySelector(
    `.subtitle-${state.toLowerCase()}`
  );

  selectedState.classList.add("selected");

  // show captions underlining when captions are on
  const captions = document.querySelector(".captions-btn");
  if (state.toLowerCase() === "off") {
    captions.style.borderBottom = "none";
  } else {
    captions.style.borderBottom = "4px solid red";
  }
}

// helper function
function capitalize(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}
