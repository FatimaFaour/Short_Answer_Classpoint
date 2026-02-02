using System;
using System.Reflection;
using System.Runtime.InteropServices;
using Office = Microsoft.Office.Core;
using PowerPoint = Microsoft.Office.Interop.PowerPoint;

namespace PowerPointVstoAddIn
{
    [ComVisible(true)]
    public class Ribbon : Office.IRibbonExtensibility
    {
        private Office.IRibbonUI ribbon;

        public string GetCustomUI(string ribbonId)
        {
            return GetResourceText("PowerPointVstoAddIn.Ribbon.xml");
        }

        public void Ribbon_Load(Office.IRibbonUI ribbonUI)
        {
            ribbon = ribbonUI;
        }

        public void OnStartShortAnswer(Office.IRibbonControl control)
        {
            AddButtonToSlide();
            Globals.ThisAddIn.ShowTeacherPane();
        }

        private void AddButtonToSlide()
        {
            var app = Globals.ThisAddIn.Application;

            if (app.ActiveWindow == null || app.ActiveWindow.View.Slide == null)
                return;

            PowerPoint.Slide slide = app.ActiveWindow.View.Slide;

            var shape = slide.Shapes.AddShape(
                Office.MsoAutoShapeType.msoShapeRoundedRectangle,
                0, 102, 204, 70);

            shape.TextFrame.TextRange.Text = "Short Answer Question";
            shape.Fill.ForeColor.RGB = System.Drawing.Color.LightBlue.ToArgb();
        }

        private static string GetResourceText(string resourceName)
        {
            Assembly asm = Assembly.GetExecutingAssembly();
            foreach (string name in asm.GetManifestResourceNames())
            {
                if (string.Equals(resourceName, name, StringComparison.OrdinalIgnoreCase))
                {
                    using (var reader =
                        new System.IO.StreamReader(asm.GetManifestResourceStream(name)))
                    {
                        return reader.ReadToEnd();
                    }
                }
            }
            return null;
        }
    }
}
