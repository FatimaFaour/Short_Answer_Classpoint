using System;
using Microsoft.Office.Tools;

namespace PowerPointVstoAddIn
{
    public sealed partial class ThisAddIn
    {
        private CustomTaskPane _teacherPane;

        protected override Microsoft.Office.Core.IRibbonExtensibility CreateRibbonExtensibilityObject()
        {
            return new Ribbon();
        }

        private void ThisAddIn_Startup(object sender, EventArgs e)
        {
        }

        private void ThisAddIn_Shutdown(object sender, EventArgs e)
        {
        }

        public void ShowTeacherPane()
        {
            if (_teacherPane == null)
            {
                var panel = new TeacherPanel();
                _teacherPane = this.CustomTaskPanes.Add(panel, "Short Answer");
                _teacherPane.Width = 300;
            }

            _teacherPane.Visible = true;
        }
    }
}
