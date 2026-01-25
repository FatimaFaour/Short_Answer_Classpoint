/* global Office, PowerPoint */

const SETTINGS_KEYS = {
  apiBaseUrl: "shortAnswerApiBaseUrl",
  questionId: "shortAnswerQuestionId",
  sessionCode: "shortAnswerSessionCode",
  slideData: "shortAnswerSlideData"
};

Office.onReady(() => {
  Office.actions.associate("insertShortAnswerButton", insertShortAnswerButton);
});

async function insertShortAnswerButton(event) {
  try {
    await PowerPoint.run(async context => {
      const settings = Office.context.document.settings;
      const questionId = settings.get(SETTINGS_KEYS.questionId) || "placeholder-question";
      const sessionCode = settings.get(SETTINGS_KEYS.sessionCode) || "placeholder-session";

      const selectedSlides = context.presentation.getSelectedSlides();
      selectedSlides.load("items/id");
      await context.sync();

      if (!selectedSlides.items.length) {
        throw new Error("No slide selected.");
      }

      const slide = selectedSlides.items[0];

      let slideWidth = 960;
      let slideHeight = 540;
      try {
        const slideSize = context.presentation.getSlideSize();
        slideSize.load("width,height");
        await context.sync();
        slideWidth = slideSize.width;
        slideHeight = slideSize.height;
      } catch (sizeError) {
        // Use fallback slide size
      }

      const buttonWidth = 240;
      const buttonHeight = 60;
      const left = Math.max(0, (slideWidth - buttonWidth) / 2);
      const top = Math.max(0, slideHeight - buttonHeight - 40);

      let shape;
      try {
        shape = slide.shapes.addGeometricShape(PowerPoint.GeometricShapeType.roundedRectangle);
      } catch (shapeError) {
        shape = slide.shapes.addTextBox("Short Answer");
      }

      shape.left = left;
      shape.top = top;
      shape.width = buttonWidth;
      shape.height = buttonHeight;

      if (shape.fill) {
        shape.fill.setSolidColor("#0078D4");
      }
      if (shape.line) {
        shape.line.color = "#005A9E";
        shape.line.weight = 1;
      }

      shape.textFrame.textRange.text = "Short Answer";
      shape.textFrame.textRange.font.color = "#FFFFFF";
      shape.textFrame.textRange.font.size = 18;
      shape.textFrame.textRange.font.bold = true;
      shape.textFrame.textRange.paragraphFormat.alignment = "Center";

      shape.tags.add("shortAnswer", "true");
      shape.tags.add("questionId", questionId);
      shape.tags.add("sessionCode", sessionCode);
      shape.tags.add("slideId", slide.id);

      shape.load("id");
      await context.sync();

      const slideData = settings.get(SETTINGS_KEYS.slideData) || {};
      slideData[slide.id] = {
        slideId: slide.id,
        shapeId: shape.id,
        questionId,
        sessionCode
      };
      settings.set(SETTINGS_KEYS.slideData, slideData);

      await new Promise(resolve => settings.saveAsync(() => resolve()));
    });
  } catch (error) {
    // Errors will surface in Office UI logs.
  } finally {
    event.completed();
  }
}
