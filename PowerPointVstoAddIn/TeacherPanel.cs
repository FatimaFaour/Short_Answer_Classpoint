using System;
using System.Windows.Forms;
using System.Diagnostics;
using System.IO;

namespace PowerPointVstoAddIn
{
    public partial class TeacherPanel : UserControl
    {
        private void StartMainApi()
        {
            var psi = new System.Diagnostics.ProcessStartInfo
            {
                FileName = @"C:\Users\user\Desktop\M2-ISDI\Short_Answer_Classpoint\Short_Answer_Classpoint\venv\Scripts\python.exe",
                Arguments = "-m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload",
                UseShellExecute = true,
                CreateNoWindow = false,
                WorkingDirectory = @"C:\Users\user\Desktop\M2-ISDI\Short_Answer_Classpoint\Short_Answer_Classpoint"
            };

            System.Diagnostics.Process.Start(psi);
        }
        private void StartTeacherApi()
        {
            var psi = new System.Diagnostics.ProcessStartInfo
            {
                FileName = @"C:\Users\user\Desktop\M2-ISDI\Short_Answer_Classpoint\Short_Answer_Classpoint\venv\Scripts\python.exe",
                Arguments = "-m teacher.app",
                UseShellExecute = true,
                CreateNoWindow = false,
                WorkingDirectory = @"C:\Users\user\Desktop\M2-ISDI\Short_Answer_Classpoint\Short_Answer_Classpoint"
            };

            System.Diagnostics.Process.Start(psi);
        }


        public TeacherPanel()
        {
            InitializeComponent();
        }



        private void btnLogin_Click(object sender, EventArgs e)
        {
            try
            {
                StartMainApi();
                StartTeacherApi();

                MessageBox.Show(
                    "FastAPI backends started successfully",
                    "Short Answer");
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Error");
            }
        }


    }
}
