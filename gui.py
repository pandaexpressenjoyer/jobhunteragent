import os
import sys
import queue
import threading
from dotenv import load_dotenv
from pypdf import PdfReader
import customtkinter as ctk
from tkinter import filedialog
from crewai import Crew, Process, LLM

# Import backend modular engineering factories
from agents import create_agents
from tasks import create_tasks

# Import decoupled graphical view tab components
from view_log import LogTab, GUIQueueStream
from view_playbook import PlaybookTab
from view_resume import ResumeTab

# Configure application unified appearance and color palettes
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Resolve absolute path variables to prevent background threads from dropping environment handles
script_directory = os.path.dirname(os.path.abspath(__file__))
secure_env_path = os.path.join(script_directory, ".env")
load_dotenv(secure_env_path)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Main graphical layout configurations
        self.title("GTA Embedded Pipeline Core")
        self.geometry("1200x800")
        self.selected_resume_path = None
        self.text_queue = queue.Queue()

        # Allocate space rules across grid boundaries
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # =================================================================
        # LEFT CONTROL INTERFACE PANEL: PANELS CONFIGURATION
        # =================================================================
        self.left_panel = ctk.CTkFrame(self, width=300, corner_radius=10)
        self.left_panel.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        self.left_panel.grid_rowconfigure(7, weight=1)

        self.lbl_title = ctk.CTkLabel(self.left_panel, text="Pipeline Inputs", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_title.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Configuration field inputs for automated tracking targets
        self.lbl_roles = ctk.CTkLabel(self.left_panel, text="Target Role Tracker:", font=ctk.CTkFont(weight="bold"))
        self.lbl_roles.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.entry_roles = ctk.CTkEntry(self.left_panel, width=260)
        self.entry_roles.insert(0, "Embedded Software & Firmware Engineering Internships")
        self.entry_roles.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        self.lbl_location = ctk.CTkLabel(self.left_panel, text="Target Region Location:", font=ctk.CTkFont(weight="bold"))
        self.lbl_location.grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.entry_location = ctk.CTkEntry(self.left_panel, width=260)
        self.entry_location.insert(0, "Greater Toronto Area")
        self.entry_location.grid(row=4, column=0, padx=20, pady=5, sticky="w")

        self.lbl_file = ctk.CTkLabel(self.left_panel, text="Active Profile Target:", font=ctk.CTkFont(weight="bold"))
        self.lbl_file.grid(row=5, column=0, padx=20, pady=5, sticky="w")
        
        self.btn_browse = ctk.CTkButton(self.left_panel, text="Select Resume PDF", fg_color="transparent", border_width=2, command=self.browse_pdf)
        self.btn_browse.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        
        self.lbl_status_file = ctk.CTkLabel(self.left_panel, text="No PDF Loaded (Select a file)", text_color="gray", font=ctk.CTkFont(size=12))
        self.lbl_status_file.grid(row=7, column=0, padx=20, pady=5, sticky="nw")

        self.btn_run = ctk.CTkButton(self.left_panel, text="Launch Agent Engine", state="disabled", command=self.start_pipeline_thread)
        self.btn_run.grid(row=8, column=0, padx=20, pady=20, sticky="ew")

        # =================================================================
        # RIGHT INTERFACE PANEL: TABBED WINDOW MANAGER
        # =================================================================
        self.tab_view = ctk.CTkTabview(self, corner_radius=10)
        self.tab_view.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        
        # Instantiate sub windows tabs
        self.tab_view.add("Live Terminal Trace")
        self.tab_view.add("Interview Playbook")
        self.tab_view.add("ATS Tailored Resume")

        # Pack external modular frames into the tab coordinates
        self.log_window = LogTab(self.tab_view.tab("Live Terminal Trace"), self.text_queue)
        self.log_window.pack(fill="both", expand=True)

        self.playbook_window = PlaybookTab(self.tab_view.tab("Interview Playbook"))
        self.playbook_window.pack(fill="both", expand=True)

        self.resume_window = ResumeTab(self.tab_view.tab("ATS Tailored Resume"))
        self.resume_window.pack(fill="both", expand=True)

    def browse_pdf(self):
        """Dynamic local file selection window module handler."""
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.selected_resume_path = file_path
            filename = os.path.basename(file_path)
            self.lbl_status_file.configure(text=f"Loaded: {filename}", text_color="green")
            self.btn_run.configure(state="normal")

    def start_pipeline_thread(self):
        """Asynchronous worker activation routine ensuring GUI fluid latency."""
        self.btn_run.configure(state="disabled", text="Processing...")
        self.log_window.write_system_message("Initializing background processing pipelines...\n")
        
        worker = threading.Thread(target=self.run_crewai_pipeline, daemon=True)
        worker.start()

    def run_crewai_pipeline(self):
        """Background process container executing heavy internet searches and model scans."""
        try:
            # Hijack console stream handles and re-route blocks to our queue view class
            sys.stdout = GUIQueueStream(self.text_queue)

            print(f"Scraping vector records across layout target: {self.selected_resume_path}")
            pdf_reader = PdfReader(self.selected_resume_path)
            extracted_resume_text = ""
            for page_num, page in enumerate(pdf_reader.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    extracted_resume_text += f"\n--- RESUME PAGE {page_num} ---\n" + page_text

            # Boot language framework properties
            claude_brain = LLM(model="anthropic/claude-sonnet-5")

            # Load architectural definitions from factory scripts
            job_searcher, skills_advisor, interview_coach, ats_optimizer = create_agents(claude_brain)
            tasks_list = create_tasks(job_searcher, skills_advisor, interview_coach, ats_optimizer)

            job_hunting_crew = Crew(
                agents=[job_searcher, skills_advisor, interview_coach, ats_optimizer],
                tasks=tasks_list,
                process=Process.sequential
            )

            execution_inputs = {
                "target_roles": self.entry_roles.get(),
                "location": self.entry_location.get(),
                "user_profile": extracted_resume_text
            }

            print("\nExecuting Agent Orchestration Pipeline - Tracking outputs directly in UI tabs...")
            job_hunting_crew.kickoff(inputs=execution_inputs)

            # Draw the original document page images inside the visual pane window
            self.resume_window.display_pdf_layout(self.selected_resume_path)
            
            # Pull written report updates back into view text panels
            self.playbook_window.load_completed_file()
            self.resume_window.load_completed_file()
            print("\n✨ Reports loaded into UI windows successfully.")

        except Exception as e:
            print(f"\nOperational Failure inside backend vectors: {str(e)}\n")
        finally:
            # Revert tracking pipes back to operating system standard handles
            sys.stdout = sys.__stdout__
            self.btn_run.configure(state="normal", text="Launch Agent Engine")


if __name__ == "__main__":
    app = App()
    app.mainloop()