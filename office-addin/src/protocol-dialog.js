Office.onReady(() => {
  const url = new URL(window.location.href);
  const protocolUrl = url.searchParams.get("protocolUrl");
  const protocolUrlElement = document.getElementById("protocol-url");
  if (protocolUrl && protocolUrlElement) {
    protocolUrlElement.textContent = protocolUrl;
  }
});
