# ATS Optimization Deliverable — Aditya Ganguli
## Tailored Resume Sections: Technical Skills Matrix + Project Bullet Rewrite
### Target Roles: Embedded Software/Firmware Internships (Kepler, AMD, Rivian/VW, Qualcomm, MDA — GTA Pipeline)

---

## ⚠️ INTEGRITY NOTE (Read First)

Every rewrite below is a **reframing of existing, verifiable work** — not new experience. Where the target job postings require skills Aditya does not yet have evidence for (RTOS, embedded Linux, CAN, kernel drivers), I have **not** inserted those terms into the skills list or bullets. Instead, I've done three things:

1. Upgraded vague/generic verbs and nouns into the **precise technical vocabulary** ATS parsers and recruiters are trained to match (e.g., "opcode decoding" → "Instruction Set Architecture (ISA) emulation").
2. Flagged a small number of **conditional additions** (e.g., CMake) that should only be added if factually true — with the exact test to apply.
3. Provided a **Keyword Gap Ledger** at the end showing honestly which JD keywords are earned, partially earned, or not present — so no line here should be pasted onto the resume if it isn't true for him.

---

## 1️⃣ REVISED TECHNICAL SKILLS MATRIX

**Formatting upgrade rationale:** ATS parsers weight skills sections heavily and often do exact-string matching. Converting the current two-paragraph "Additional" block into **labeled, categorized rows** increases the number of discrete matchable tokens, improves readability for human reviewers, and mirrors the structure most parsers (Workday, Greenhouse, Taleo) expect.

```markdown
## TECHNICAL SKILLS

**Languages:** C, C++, Java, JavaScript, Python, Verilog, VHDL, MATLAB, HTML, CSS

**Embedded Systems & Firmware:** ARM Cortex-M Microcontrollers (MSP432E401Y, ESP32), 
Register-Level Programming, Memory-Mapped I/O, Interrupt-Driven Firmware Design, 
Bare-Metal Systems Programming, Cross-Platform Build Configuration, Keil uVision IDE

**Communication Protocols:** I2C (100 kbps master/slave interfacing), UART/Serial 
Communication (115200 bps), Real-Time Sensor Data Streaming

**Hardware Design & Debug Tools:** Quartus (FPGA/CPLD Synthesis), KiCad (PCB Schematic 
Capture), Arduino, Soldering & Hardware Bring-Up, Oscilloscope/Multimeter-Based Validation

**CAD / Mechanical-Electrical Integration:** Autodesk Inventor, AutoCAD, SolidWorks, 
Fusion 360, Rapid Prototyping (3D Printing)

**Software Engineering Practices:** Git (Version Control), Agile/Scrum (Jira Sprint 
Tracking), Data Pipeline Automation (Excel-VBA), System Monitoring & Observability (Datadog)
```

**Why this structure wins on ATS:**
- Each category header is itself a matchable keyword cluster ("Embedded Systems & Firmware," "Communication Protocols") that aligns with how Kepler/AMD/Qualcomm postings segment their own requirements.
- "Register-Level Programming," "Memory-Mapped I/O," and "Interrupt-Driven Firmware Design" are **legitimate descriptions of MSP432/Keil work he already did** — they were previously buried in prose bullets and invisible to skills-section keyword scans. Pulling them into the skills line doubles their matching surface area.
- Verilog/VHDL are retained (already an existing resume claim, not new) but are **not** paired with a fabricated FPGA project — see Gap Ledger for honest framing if asked in interview.

---

## 2️⃣ REVISED PROJECT BULLETS

### 🎮 GBU — Cycle-Accurate Game Boy ISA Emulator & Hardware Simulator (C++)
*(Title upgrade: "Gameboy Emulator" → naming it as an ISA/hardware simulator surfaces to ATS scans for "computer architecture," "embedded systems," and "systems programming" roles — all of which explicitly appear in the target postings.)*

```markdown
GBU — Cycle-Accur