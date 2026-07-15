import os
import customtkinter as ctk

class PlaybookTab(ctk.CTkFrame):
    """
    Manages the presentation layout and discrete storage read sweeps 
    allocated for the custom target interview prep materials.
    """
    def __init__(self, master):
        super().__init__(master)

        # Initialize the readable text rendering box
        self.txt_playbook = ctk.CTkTextbox(self, font=ctk.CTkFont(size=13))
        self.txt_playbook.pack(fill="both", expand=True, padx=10, pady=10)

    def load_completed_file(self):
        """Safely processes and reads generated playbook markdown files onto the textbox widget."""
        target_file = "gta_firmware_playbook.md"
        if os.path.exists(target_file):
            with open(target_file, "r", encoding="utf-8") as file_handle:
                self.txt_playbook.delete("1.0", "end")
                self.txt_playbook.insert("1.0", file_handle.read())