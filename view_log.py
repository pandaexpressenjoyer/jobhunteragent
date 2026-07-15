import re
import queue
import customtkinter as ctk

class GUIQueueStream:
    """
    Hooks directly into the standard output stream inside the background thread.
    Scrubs out terminal ANSI color signals before safely passing clean strings 
    into the visual UI thread queue.
    """
    def __init__(self, text_queue):
        self.text_queue = text_queue
        self.ansi_cleaner = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def write(self, message):
        if message:
            clean_message = self.ansi_cleaner.sub('', message)
            self.text_queue.put(clean_message)

    def flush(self):
        pass


class LogTab(ctk.CTkFrame):
    """
    Encapsulates the text interface container and queue-polling routines 
    allocated for the real-time background execution log window.
    """
    def __init__(self, master, text_queue):
        super().__init__(master)
        self.text_queue = text_queue

        # Initialize the monospace logging textbox
        self.txt_log = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Courier", size=12))
        self.txt_log.pack(fill="both", expand=True, padx=10, pady=10)

        # Trigger the persistent monitoring queue loop
        self.check_queue_loop()

    def check_queue_loop(self):
        """
        Asynchronous worker monitor loop driving updates onto text panels
        without locking the main application thread framework.
        """
        while not self.text_queue.empty():
            try:
                msg = self.text_queue.get_nowait()
                self.txt_log.insert("end", msg)
                self.txt_log.see("end")
            except queue.Empty:
                break
        self.after(100, self.check_queue_loop)

    def write_system_message(self, message):
        """Allows outbound main modules to write status updates directly to this log."""
        self.txt_log.insert("end", message)
        self.txt_log.see("end")