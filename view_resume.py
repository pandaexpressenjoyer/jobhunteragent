import os
import customtkinter as ctk

class ResumeTab(ctk.CTkFrame):
    """
    Manages the presentation layout and discrete storage read sweeps 
    allocated for the automated ATS-tailored resume modifications.
    """
    def __init__(self, master):
        super().__init__(master)

        # Initialize the tailored resume output box
        self.txt_resume = ctk.CTkTextbox(self, font=ctk.CTkFont(size=13))
        self.txt_resume.pack(fill="both", expand=True, padx=10, pady=10)

    def load_completed_file(self):
        """Safely processes and reads generated resume adjustments onto the textbox widget."""
        target_file = "ats_optimized_resume.md"
        if os.path.exists(target_file):
            with open(target_file, "r", encoding="utf-8") as file_handle:
                self.txt_resume.delete("1.0", "end")
                self.txt_resume.insert("1.0", file_handle.read())