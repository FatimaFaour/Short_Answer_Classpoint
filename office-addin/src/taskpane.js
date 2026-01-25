/* global Office, PowerPoint */

const SETTINGS_KEYS = {
  apiBaseUrl: "shortAnswerApiBaseUrl",
  questionId: "shortAnswerQuestionId",
  sessionCode: "shortAnswerSessionCode",
  slideData: "shortAnswerSlideData"
};

let lastTriggeredShapeId = null;

Office.onReady(() => {
  loadSettings();
  document.getElementById("saveSettings").addEventListener("click", saveSettings);
  Office.context.document.addHandlerAsync(
    Office.EventType.DocumentSelectionChanged,
    onSelectionChanged
  );
});

function loadSettings() {
  const settings = Office.context.document.settings;
  document.getElementById("apiBaseUrl").value = settings.get(SETTINGS_KEYS.apiBaseUrl) || "";
  document.getElementById("questionId").value = settings.get(SETTINGS_KEYS.questionId) || "";
  document.getElementById("sessionCode").value = settings.get(SETTINGS_KEYS.sessionCode) || "";
  showStatus("Settings loaded.");
}

function saveSettings() {
  const settings = Office.context.document.settings;
  settings.set(SETTINGS_KEYS.apiBaseUrl, document.getElementById("apiBaseUrl").value.trim());
  settings.set(SETTINGS_KEYS.questionId, document.getElementById("questionId").value.trim());
  settings.set(SETTINGS_KEYS.sessionCode, document.getElementById("sessionCode").value.trim());
  settings.saveAsync(result => {
    if (result.status === Office.AsyncResultStatus.Succeeded) {
      showStatus("Settings saved.");
    } else {
      showStatus("Could not save settings.", true);
    }
  });
}

async function onSelectionChanged() {
  try {
    await PowerPoint.run(async context => {
      const selectedShapes = context.presentation.getSelectedShapes();
      selectedShapes.load("items/id");
      await context.sync();

      if (!selectedShapes.items.length) {
        return;
      }

      const shape = selectedShapes.items[0];
      if (shape.id === lastTriggeredShapeId) {
        return;
      }

      shape.tags.load("items");
      await context.sync();

      const tagMap = toTagMap(shape.tags.items);
      if (tagMap.shortAnswer !== "true") {
        return;
      }

      lastTriggeredShapeId = shape.id;
      await triggerShortAnswer(tagMap);
    });
  } catch (error) {
    showStatus("Unable to read slide selection.", true);
  }
}

function toTagMap(tags) {
  const map = {};
  tags.forEach(tag => {
    map[tag.key] = tag.value;
  });
  return map;
}

async function triggerShortAnswer(tagMap) {
  const settings = Office.context.document.settings;
  const apiBaseUrl = settings.get(SETTINGS_KEYS.apiBaseUrl) || "";
  const questionId = tagMap.questionId || settings.get(SETTINGS_KEYS.questionId) || "";
  const slideId = tagMap.slideId || "";

  if (!apiBaseUrl) {
    showStatus("Set the API Base URL before starting a short answer session.", true);
    return;
  }

  try {
    const response = await fetch(`${apiBaseUrl.replace(/\/$/, "")}/shortanswer/start`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        slide_id: slideId,
        question_id: questionId
      })
    });

    if (!response.ok) {
      throw new Error("Request failed");
    }

    showStatus("Short answer session started.");
  } catch (error) {
    showStatus("We couldn't reach the Short Answer service. Please check the API URL and try again.", true);
  }
}

function showStatus(message, isError = false) {
  const status = document.getElementById("status");
  status.textContent = message;
  status.classList.toggle("error", isError);
}
