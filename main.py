import os
from dotenv import load_dotenv
from crewai import Crew, Process, LLM

# Import factory functions from our new local modules
from agents import create_agents
from tasks import create_tasks

# Load environment configuration secrets
load_dotenv()

# Initialize central processing brain
claude_brain = LLM(
    model="anthropic/claude-sonnet-5",
    
)

# Instantiate the modular building blocks
job_searcher, skills_advisor, interview_coach = create_agents(claude_brain)
tasks_list = create_tasks(job_searcher, skills_advisor, interview_coach)

# Assemble everything into the runtime orchestrator
job_hunting_crew = Crew(
    agents=[job_searcher, skills_advisor, interview_coach],
    tasks=tasks_list,
    process=Process.sequential
)

# Execution payload setup
# Execution payload setup
execution_inputs = {
    "target_roles": "Embedded Software & Firmware Engineering Internships",
    "location": "Greater Toronto Area",
    "user_profile": (
        "Candidate Background: Computer Engineering student at McMaster University "
        "with a 3.86/4.0 GPA (Dean's List). Strong foundational knowledge in Data Structures "
        "& Algorithms, Embedded Systems Design, Digital Logic, and Computer Architecture.\n\n"
        
        "Enterprise Experience: Former IT Core Systems Intern at Zurich Canada. Experienced "
        "in deploying enterprise error monitoring systems (Datadog) across multi-environment "
        "stacks, building VBA data aggregation pipelines for large datasets (14,000+ records), "
        "and tracking agile engineering delivery with custom Jira dashboards.\n\n"
        
        "Core Hardware & Systems Projects:\n"
        "- Game Boy Emulator (C++): Built a low-level, cycle-accurate Sharp LR35902 CPU architecture "
        "emulator from scratch using SDL2. Implemented opcode decoding, a custom Memory Management "
        "Unit (MMU), memory bank switching (MBC), and persistent cartridge save states.\n"
        "- Portable LiDAR Scanner (C): Developed firmware on a TI MSP432 MCU inside Keil uVision. "
        "Configured register-level peripheral interfacing via I2C (100 kbps) and UART (115200 bps), "
        "driving a stepper motor for 360-degree sweeps mapped to a 3D polar-to-volumetric MATLAB engine.\n"
        "- Assistive Engineering Design: Co-designed mechanical shortcut-mapped hardware enclosures "
        "following the Engineering Design Cycle.\n\n"
        
        "Technical Toolset:\n"
        "- Languages: Advanced in C/C++, Python, Java, JavaScript, Verilog, VHDL, MATLAB.\n"
        "- Hardware/EDA Tools: KiCad, Intel Quartus, Git, Soldering, SolidWorks, Fusion 360.\n"
        "- Silicon Architectures: ARM-based Microcontrollers (MSP432, ESP32), Arduino, and FPGAs."
    )
}

if __name__ == "__main__":
    print("\nRunning Pipeline...")
    
    # Execute the crew pipeline
    final_report = job_hunting_crew.kickoff(inputs=execution_inputs)
    
    print("\n✨ Pipeline Complete. Report:")
    print(final_report)