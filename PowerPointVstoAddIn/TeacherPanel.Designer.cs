namespace PowerPointVstoAddIn
{
    partial class TeacherPanel
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.Button btnLogin;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
                components.Dispose();
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.btnLogin = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // btnLogin
            // 
            this.btnLogin.Dock = System.Windows.Forms.DockStyle.Top;
            this.btnLogin.FlatStyle = System.Windows.Forms.FlatStyle.System;
            this.btnLogin.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.5F);
            this.btnLogin.Location = new System.Drawing.Point(0, 0);
            this.btnLogin.Name = "btnLogin";
            this.btnLogin.Size = new System.Drawing.Size(300, 50);
            this.btnLogin.TabIndex = 0;
            this.btnLogin.Text = "Teacher Login";
            this.btnLogin.Click += new System.EventHandler(this.btnLogin_Click);
            // 
            // TeacherPanel
            // 
            this.Controls.Add(this.btnLogin);
            this.Name = "TeacherPanel";
            this.Size = new System.Drawing.Size(300, 227);
            this.ResumeLayout(false);

        }
    }
}
