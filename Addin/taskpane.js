const API_BASE = "http://127.0.0.1:8000/api";

document.getElementById("startBtn").onclick = async () => {
  try {
    await fetch(`${API_BASE}/question/start`, {
      method: "POST",
    });
    alert("Question started");
  } catch (e) {
    alert("Backend not running");
  }
};

document.getElementById("closeBtn").onclick = async () => {
  try {
    await fetch(`${API_BASE}/question/close`, {
      method: "POST",
    });
    alert("Question closed");
  } catch (e) {
    alert("Backend not running");
  }
};
