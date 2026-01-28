function resolveLoginUrl() {
  const currentUrl = new URL(window.location.href);
  const overrideUrl = currentUrl.searchParams.get("loginUrl");
  if (overrideUrl) {
    return overrideUrl;
  }
    return `${currentUrl.origin}/teacher/login`;
}


function showStatus(message, isError = false) {
  const status = document.getElementById("status");
  status.textContent = message;
  status.classList.toggle("error", isError);
}

function loadLoginFrame() {
  const loginFrame = document.getElementById("loginFrame");
  const loginUrl = resolveLoginUrl();

  loginFrame.src = loginUrl;
  showStatus(`Loaded login page: ${loginUrl}`);

  loginFrame.addEventListener("error", () => {
  showStatus("Unable to load the teacher login page.", true);
  });
}

document.addEventListener("DOMContentLoaded", loadLoginFrame);
