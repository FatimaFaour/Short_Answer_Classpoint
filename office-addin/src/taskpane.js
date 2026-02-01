function resolveLoginUrl() {
  const currentUrl = new URL(window.location.href);
  return `${currentUrl.origin}/teacher/ui/login`;
}
function login() {
  Office.context.ui.displayDialogAsync(
    "https://shortanswerclasspoint.netlify.app/teacher/ui/login",
    { height: 60, width: 30 },
    function (result) {
      if (result.status !== Office.AsyncResultStatus.Succeeded) {
        console.error("Dialog failed to open");
        return;
      }

      const dialog = result.value;

      dialog.addEventHandler(
        Office.EventType.DialogMessageReceived,
        function (arg) {
          console.log("Login success:", arg.message);
          dialog.close();

          // store token/session here
        }
      );
    }
  );
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
