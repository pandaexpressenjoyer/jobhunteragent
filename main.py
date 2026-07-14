import os
import sys  
import re   
from pypdf import PdfReader  
from dotenv import load_dotenv
from crewai import Crew, Process, LLM

# Import factory functions from our local modules
from agents import create_agents
from tasks import create_tasks

# =====================================================================
# STANDARD STREAM INTERCEPTOR (THE TEE FILTER PATTERN)
# =====================================================================
class TerminalTee:
    """
    Hooks directly into the system stdout vector. Duplicates colored text streams 
    to the monitor screen while processing and cleaning out ANSI system terminal signals 
    before committing markdown entries onto local storage media blocks.
    """
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log_file = open(filename, "w", encoding="utf-8")
        # Regular expression compiled to capture and isolate terminal color/graphics escapes
        self.ansi_cleaner = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def write(self, message):
        # Forward un-modified array data stream straight to live visual terminal screen
        self.terminal.write(message)   
        
        # Scrub formatting escapes prior to physical document execution steps
        clean_message = self.ansi_cleaner.sub('', message)
        self.log_file.write(clean_message)   

    def flush(self):
        # Enforce instant physical disk writes for underlying buffer queues
        self.terminal.flush()
        self.log_file.flush()


# Load credential profiles from the local environment variable repository
load_dotenv()

# Instantiate core large language model control loop
claude_brain = LLM(
    model="anthropic/claude-sonnet-5"
)

# Unpack our four working agent systems and link task criteria objects
job_searcher, skills_advisor, interview_coach, ats_optimizer = create_agents(claude_brain)
tasks_list = create_tasks(job_searcher, skills_advisor, interview_coach, ats_optimizer)

# Assemble structural pipeline models into execution framework
job_hunting_crew = Crew(
    agents=[job_searcher, skills_advisor, interview_coach, ats_optimizer],
    tasks=tasks_list,
    process=Process.sequential  
)

# =====================================================================
# BINARY DATA INGESTION SUITE (PDF STREAM READER)
# =====================================================================
resume_path = "resume.pdf"

# Verify standard source parameters prior to pipeline loop entry
if not os.path.exists(resume_path):
    print(f"❌ Error: Target resume file '{resume_path}' not found in root directory.")
    print("Please place your 'resume.pdf' in this folder before running the pipeline.")
    sys.exit(1)

print(f"📄 Scanning and parsing text layers from '{resume_path}'...")

# Unpack internal document objects page by page
pdf_reader = PdfReader(resume_path)
extracted_resume_text = ""

for page_num, page in enumerate(pdf_reader.pages, start=1):
    page_text = page.extract_text()
    if page_text:
        extracted_resume_text += f"\n--- RESUME PAGE {page_num} ---\n" + page_text

# Direct payload variables to use extracted document buffers
execution_inputs = {
    "target_roles": "Embedded Software & Firmware Engineering Internships",
    "location": "Greater Toronto Area",
    "user_profile": extracted_resume_text  
}


if __name__ == "__main__":
    # Route primary execution traces down to our log interceptor filter
    output_filename = "full_report.md"
    sys.stdout = TerminalTee(output_filename)

    print("\n==============================================")
    print("Running Pipeline...")
    print("==============================================\n")
    
    # Fire up agent framework loops
    final_report = job_hunting_crew.kickoff(inputs=execution_inputs)
    
    print("\n==============================================")
    print("Pipeline Complete. Outputs Generated Successfully.")
    print("==============================================\n")