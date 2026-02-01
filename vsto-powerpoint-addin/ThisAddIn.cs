using System;
using Microsoft.Office.Tools;

namespace PowerPointVstoAddIn;

/// <summary>
/// Entry point for the PowerPoint VSTO add-in.
/// </summary>
public partial class ThisAddIn
{
    /// <summary>
    /// Handles add-in startup. This is a good place for any initialization logic.
    /// </summary>
    private void ThisAddIn_Startup(object sender, EventArgs e)
    {
    }

    /// <summary>
    /// Handles add-in shutdown. This is a good place for cleanup logic if needed.
    /// </summary>
    private void ThisAddIn_Shutdown(object sender, EventArgs e)
    {
    }

    /// <summary>
    /// Provides the custom ribbon implementation to PowerPoint.
    /// </summary>
    /// <returns>The ribbon extensibility object.</returns>
    protected override Microsoft.Office.Core.IRibbonExtensibility CreateRibbonExtensibilityObject()
    {
        return new Ribbon();
    }

    #region VSTO generated code

    /// <summary>
    /// Required method for Designer support - do not modify
    /// the contents of this method with the code editor.
    /// </summary>
    private void InternalStartup()
    {
        Startup += ThisAddIn_Startup;
        Shutdown += ThisAddIn_Shutdown;
    }

    #endregion
}