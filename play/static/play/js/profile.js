const tabsContainer = document.querySelector("[role=tablist]");
const tabButtons = tabsContainer.querySelectorAll("[role=tab]");
const tabPanels = document.querySelectorAll("[role=tabpanel]");
const moreAboutChannel = document.querySelector("#more-about-channel");

moreAboutChannel.addEventListener("click", (e) => {
  const currentTab = tabsContainer.querySelector('[aria-selected="true"]');
  const aboutChannelTab = document.querySelector('#tab-7');
  
    if (currentTab == aboutChannelTab) return;

    switchTab(aboutChannelTab);
})

tabsContainer.addEventListener("click", (e) => {
  const clickedTab = e.target.closest("button");
  const currentTab = tabsContainer.querySelector('[aria-selected="true"]');

  if (!clickedTab || clickedTab === currentTab) return;

  switchTab(clickedTab);
});

tabsContainer.addEventListener("keydown", (e) => {
  switch (e.key) {
    case "ArrowLeft":
      moveLeft();
      break;
    case "ArrowRight":
      moveRight();
      break;
    case "Home":
      e.preventDefault();
      switchTab(tabButtons[0]);
      break;
    case "End":
      e.preventDefault();
      switchTab(tabButtons[tabButtons.length - 1]);
      break;
  }
});

function moveLeft() {
  const currentTab = document.activeElement;

  if (!currentTab.previousElementSibling) {
    tabButtons.item(tabButtons.length - 1).focus();
  } else {
    currentTab.previousElementSibling.focus();
  }
}

function moveRight() {
  const currentTab = document.activeElement;
  if (!currentTab.nextElementSibling) {
    tabButtons.item(0).focus();
  } else {
    currentTab.nextElementSibling.focus();
  }
}

function switchTab(newTab) {
  const oldTab = tabsContainer.querySelector('[aria-selected="true"]');
  const activePanelId = newTab.getAttribute("aria-controls");
  const activePanel = tabsContainer.nextElementSibling.querySelector(
    "#" + CSS.escape(activePanelId)
  );
  tabButtons.forEach((button) => {
    button.setAttribute("aria-selected", false);
    button.setAttribute("tabindex", "-1");
  });

  tabPanels.forEach((panel) => {
    panel.setAttribute("hidden", true);
  });

  activePanel.removeAttribute("hidden", false);

  newTab.setAttribute("aria-selected", true);
  newTab.setAttribute("tabindex", "0");
  newTab.focus();
  moveIndicator(oldTab, newTab);
}

// move underline indicator
function moveIndicator(oldTab, newTab) {
  const newTabPosition = oldTab.compareDocumentPosition(newTab);
  const newTabWidth = newTab.offsetWidth / tabsContainer.offsetWidth;
  let transitionWidth;

  // if the new tab is to the right
  if (newTabPosition === 4) {
    transitionWidth =
      newTab.offsetLeft + newTab.offsetWidth - oldTab.offsetLeft;
  } else {
    // if the tab is to the left
    transitionWidth =
      oldTab.offsetLeft + oldTab.offsetWidth - newTab.offsetLeft;
    tabsContainer.style.setProperty("--_left", newTab.offsetLeft + "px");
  }

  tabsContainer.style.setProperty(
    "--_width",
    transitionWidth / tabsContainer.offsetWidth
  );

  setTimeout(() => {
    tabsContainer.style.setProperty("--_left", newTab.offsetLeft + "px");
    tabsContainer.style.setProperty("--_width", newTabWidth);
  }, 220);
}
