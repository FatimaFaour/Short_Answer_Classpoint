using System;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using Microsoft.Office.Core;
using Microsoft.Office.Interop.PowerPoint;

namespace PowerPointVstoAddIn;

/// <summary>
/// Ribbon implementation for the "My Add-in" custom tab.
/// </summary>
[ComVisible(true)]
public class Ribbon : IRibbonExtensibility
{
	private IRibbonUI? _ribbon;

	/// <summary>
	/// Returns the ribbon XML that defines the UI.
	/// </summary>
	public string GetCustomUI(string ribbonId)
	{
		return @"
<customUI xmlns='http://schemas.microsoft.com/office/2009/07/customui' onLoad='OnLoad'>
  <ribbon>
    <tabs>
      <tab id='MyAddInTab' label='My Add-in'>
        <group id='MyAddInGroup' label='Utilities'>
          <button id='SlideInfoButton'
                  label='Slide Info'
                  size='large'
                  onAction='OnSlideInfoButtonPressed'
                  imageMso='SlideShowFromCurrent'
                  />
        </group>
      </tab>
    </tabs>
  </ribbon>
</customUI>";
	}

	/// <summary>
	/// Callback invoked by Office when the ribbon loads.
	/// </summary>
	public void OnLoad(IRibbonUI ribbonUI)
	{
		_ribbon = ribbonUI;
	}

	/// <summary>
	/// Handles the Slide Info button click.
	/// </summary>
	public void OnSlideInfoButtonPressed(IRibbonControl control)
	{
		Presentation? presentation = null;
		Slide? currentSlide = null;

		try
		{
			var application = Globals.ThisAddIn.Application;
			presentation = application.ActivePresentation;

			if (presentation == null)
			{
				MessageBox.Show(
					"No active presentation was found.",
					"Slide Info",
					MessageBoxButtons.OK,
					MessageBoxIcon.Information);
				return;
			}

			currentSlide = application.ActiveWindow?.View?.Slide;
			int currentSlideNumber = currentSlide?.SlideIndex ?? 0;
			int totalSlides = presentation.Slides.Count;

			MessageBox.Show(
				$"Current Slide: {currentSlideNumber}\nTotal Slides: {totalSlides}",
				"Slide Info",
				MessageBoxButtons.OK,
				MessageBoxIcon.Information);
		}
		catch (Exception ex)
		{
			MessageBox.Show(
				$"Unable to retrieve slide information. {ex.Message}",
				"Slide Info",
				MessageBoxButtons.OK,
				MessageBoxIcon.Error);
		}
		finally
		{
			if (currentSlide != null)
			{
				Marshal.ReleaseComObject(currentSlide);
			}

			if (presentation != null)
			{
				Marshal.ReleaseComObject(presentation);
			}
		}
	}
}
