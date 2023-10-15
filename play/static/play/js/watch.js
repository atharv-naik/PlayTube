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
    case "a":
      enableNextAudioTrack();
      showControls();
      break;
    case "arrowup":
      changeVolume(0.05);
      showControls();
      showVolumeAnimation((increase = true));
      break;
    case "arrowdown":
      changeVolume(-0.05);
      showControls();
      showVolumeAnimation((increase = false));
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
  const previewImgSrc = `http://${ip}/api/get-preview-thumbnails/${video_id}/${previewImgNumber}`;
  previewImg.src = previewImgSrc;
  if (isScrubbing) {
    e.preventDefault();
    thumbnailImg.src = previewImgSrc;
    timelineContainer.style.setProperty("--progress-position", percent);
  }
  percent = Math.max(0.06, Math.min(0.94, percent));
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
speedBtn.addEventListener("click", changePlaybackSpeed);

function changePlaybackSpeed(forward = true) {
  if (forward) {
    let newPlaybackRate = video.playbackRate + 0.25;
    if (newPlaybackRate > 2) newPlaybackRate = 0.25;
    video.playbackRate = newPlaybackRate;
    speedBtn.textContent = `${newPlaybackRate}x`;
  } else {
    let newPlaybackRate = video.playbackRate - 0.25;
    if (newPlaybackRate < 0.25) newPlaybackRate = 2;
    video.playbackRate = newPlaybackRate;
    speedBtn.textContent = `${newPlaybackRate}x`;
  }
}

// Captions
// check if captions are available
function toggleCaptions() {
  showSubtitleAnimation();
  const captions = video.textTracks[0];
  const isHidden = captions.mode === "hidden";
  captions.mode = isHidden ? "showing" : "hidden";
  videoContainer.classList.toggle("captions", isHidden);
}

video.addEventListener("loadedmetadata", () => {
  if (video.textTracks.length > 0) {
    const captions = video.textTracks[0];
    captions.mode = "hidden";

    captionsBtn.addEventListener("click", toggleCaptions);
  } else {
    captionsBtn.style.display = "none";
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
videoContainer.addEventListener("dblclick", toggleFullScreenMode);

function toggleTheaterMode() {
  videoContainer.classList.toggle("theater");
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
  // thumbnailImg.classList.toggle("full-screen", document.fullscreenElement)
});

video.addEventListener("enterpictureinpicture", () => {
  videoContainer.classList.add("mini-player");
});

video.addEventListener("leavepictureinpicture", () => {
  videoContainer.classList.remove("mini-player");
});

// Play/Pause
playPauseBtn.addEventListener("click", togglePlay);
video.addEventListener("click", togglePlay);

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
let timeout;

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
    timeout = setTimeout(hideControls, 5000);
  }
}

// video.addEventListener("pause", () => {
//   clearTimeout(timeout);
//   showControls();
// });

// video.addEventListener("mousemove", () => {
//   clearTimeout(timeout);
//   showControls();

//   if (!video.paused) {
//     // showControls();
//     timeout = setTimeout(hideControls, 5000);
//   }
// });

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
