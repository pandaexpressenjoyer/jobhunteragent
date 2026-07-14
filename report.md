# 🎯 Technical Interview Performance Playbook
## Candidate: Aditya Ganguli | Target: Embedded Software/Firmware Internships (GTA Pipeline)
### Prepared for: Kepler Communications, AMD, Rivian/VW, Qualcomm, MDA Space

---

## 🧭 STRATEGIC CONTEXT

This playbook is built on the collision of two datasets: the **hard requirements** pulled from five live GTA postings (Kepler, AMD, Rivian/VW, Qualcomm, MDA), and the **skill gap analysis** showing Aditya is strong in bare-metal C/C++ and protocol-level firmware (Game Boy emulator, MSP432 LiDAR project) but has **zero demonstrated exposure to Embedded Linux and RTOS task scheduling** — the two things that appear as hard requirements (not preferences) in 3 of 5 target postings.

Interviewers at this level do not ask "do you know FreeRTOS?" as a yes/no gate — they ask scenario questions that surface whether a candidate has *actually wrestled* with concurrency, memory-mapped hardware, or the software/hardware debugging boundary. The three questions below are the exact archetypes a hiring manager at Kepler, AMD, or Rivian/VW would use to separate "read about it" from "built it." Each includes the ideal engineering response strategy so preparation can be structured around demonstrating depth rather than reciting definitions.

---

## ❓ QUESTION 1 — Concurrency & RTOS Reasoning
**(Targets: Kepler — "interrupt handlers, concurrency," FreeRTOS; AMD — RTOS/embedded controller structures; Rivian/VW — RTOS fundamentals)**

> "Walk me through how you'd redesign your LiDAR scanner firmware if you had to run it under FreeRTOS instead of bare-metal on the MSP432 — specifically, how would you split the work into tasks, and what would you do if your UART transmit task and your motor control task both needed to touch the same sensor data buffer at the same time?"

### 🎓 Ideal Engineering Response Strategy
A strong candidate should not just say "I'd use a mutex." They should walk through the reasoning chain:
1. **Task decomposition first** — identify natural concurrency boundaries: sensor polling (periodic, ISR-driven), motor control (periodic, timing-sensitive), UART transmit (bursty, lower priority). Explain *why* these are separate tasks rather than one big loop — decoupling timing-critical motor control from potentially blocking UART I/O.
2. **Shared resource identification** — explicitly name the shared sensor data buffer as a critical section and explain the race condition risk (partial write while another task reads = corrupted LiDAR frame).
3. **Correct primitive choice with justification** — a mutex (not a binary semaphore) for mutual exclusion on a resource, versus a queue for producer/consumer handoff between the polling task and the transmit task. Bonus points if they distinguish *why* a queue is often preferable to a shared buffer + mutex in RTOS design (avoids holding locks across task boundaries, avoids priority inversion).
4. **ISR-safety awareness** — if sensor polling is interrupt-driven, they should mention needing ISR-safe APIs (e.g., `xQueueSendFromISR`) rather than blocking calls inside an interrupt context.
5. **Priority inversion mention** — even a brief, correct mention ("I'd need to watch for priority inversion if the low-priority UART task holds the mutex the high-priority motor task needs — could use priority inheritance") signals real RTOS literacy versus textbook memorization.

### 🚩 Red Flags to Watch For
- Jumping straight to "mutex" without identifying *why* a race condition exists.
- No mention of ISR-safe variants of RTOS APIs.
- Treating "task" and "thread" as interchangeable without acknowledging RTOS-specific scheduling (priority-based preemption vs. OS thread fairness).
- Inability to connect back to his own project — if he can't map this onto the actual LiDAR sensor/motor/UART components he built, it suggests the RTOS knowledge is freshly memorized rather than internalized.

### 💬 Good Follow-Up Probes
- "What happens if the motor control task misses its deadline because the mutex is held too long?"
- "How would this differ if you were doing this in embedded Linux with pthreads instead of FreeRTOS?"

---

## ❓ QUESTION 2 — Linux Kernel / Driver-Level Systems Thinking
**(Targets: Kepler — "writing kernel modules/drivers," Embedded Linux for space/ground systems; Rivian/VW — Hardware Abstraction Layers, board bring-up)**

> "Say you've built a character device driver that exposes a GPIO pin as a file in `/dev`. A userspace application writes to it to toggle an LED, but sometimes writes are silently dropped when the system is under load. Walk me through how you'd debug this, and separately, explain why we'd even want a kernel driver here instead of just using `sysfs` GPIO exports or a userspace library like `libgpiod`."

### 🎓 Ideal Engineering Response Strategy
This question is deliberately two-layered: a debugging scenario plus an architectural judgment call, because Kepler's posting specifically wants engineers who can move between hardware drivers and higher-level embedded Linux systems.

1. **Debugging methodology** — a strong candidate should think in layers: (a) confirm the write syscall is actually reaching the driver's `write()` file operation (add `printk`/`dmesg` logging), (b) check if the driver's write handler is doing anything non-atomic that could be preempted or interrupted, (c) consider whether GPIO toggling itself is subject to scheduling delay (is this an RTOS-hard-realtime concern bleeding into a general-purpose Linux kernel — a legitimate expectation mismatch to flag), (d) check return values — is the userspace write() checking that all bytes were actually written, or silently ignoring partial writes/EAGAIN?
2. **Architectural judgment** — the interviewer wants to see the candidate understand *trade-offs*, not just "kernel drivers are cooler." A mature answer: sysfs GPIO/libgpiod is faster to develop and sufficient for simple toggling, but a custom character driver makes sense when you need custom ioctl commands, interrupt-driven GPIO handling (edge-triggered wakeups), buffering, or you're bundling GPIO control with other hardware logic (e.g., a sensor driver that also manages a GPIO chip-select line) into one cohesive interface.
3. **Concurrency awareness in kernel space** — bonus if they mention that kernel code sharing state across processes calling into the driver concurrently needs its own locking (spinlocks in atomic context, mutexes if sleeping is allowed) — distinct from userspace RTOS locking discussed in Q1, showing they understand the layers are architecturally different.

### 🚩 Red Flags to Watch For
- No mention of `dmesg`/`printk` as the first debugging instinct in kernel space — signals they haven't actually worked in a kernel dev loop.
- Treating kernel driver work as identical to userspace debugging (no acknowledgment of atomic context restrictions, no mention that you can't just "print and step through" the way you would in GDB on a userspace app).
- Unable to articulate *any* reason to prefer a custom driver over sysfs — suggests the character-device driver project (if built per the roadmap) was copy-pasted from a tutorial without understanding motivation.

### 💬 Good Follow-Up Probes
- "How would `dmesg` output differ if this were a kernel panic versus a silently dropped write?"
- "If you had to make this GPIO toggle interrupt-driven instead of polled, what would change in your driver?"

---

## ❓ QUESTION 3 — Hardware/Software Boundary Debugging
**(Targets: AMD — "waveform-level analysis for root-causing FW/HW issues," debugging FW/HW boundary; M.I.S. Electronics — oscilloscope/logic analyzer fluency; Qualcomm — real-time system debugging)**

> "Your I2C sensor read is intermittently returning garbage data — maybe 1 in 200 reads. You've checked your C code logic three times and it looks correct. How do you figure out whether this is a firmware bug, a timing/electrical issue on the bus, or something else entirely? Be specific about the tools you'd reach for and in what order."

### 🎓 Ideal Engineering Response Strategy
This is the classic AMD/M.I.S.-style question probing whether a candidate defaults to pure software debugging or actually knows how to root-cause across the hardware boundary — directly testing the "waveform-level analysis" and logic-analyzer fluency called out in the job postings.

A strong, layered answer should sound like:
1. **Reproduce and isolate first** — establish whether the failure correlates with anything: bus load, temperature, specific register addresses, timing since power-on. This shows scientific method before tool selection.
2. **Instrument in software first (cheap, fast)** — add a checksum/retry counter, log the specific failing byte pattern, check if it's always the same bit flipping (suggests noise/electrical) versus random garbage (suggests timing/protocol violation like a NACK being mishandled or a clock stretch not respected).
3. **Move to the logic analyzer/scope (the differentiator answer)** — capture the actual I2C waveform on the failing transaction. Specifically look at: (a) clock stretching being handled correctly by the master, (b) setup/hold time violations at the specific clock speed being used, (c) whether there's bus contention or a floating line during multi-master conditions, (d) pull-up resistor adequacy — rise time on SDA/SCL if the bus is loaded with multiple devices.
4. **Correlate the electrical capture with the code path** — this is the "root-cause across the boundary" moment interviewers are listening for: e.g., "if the scope shows the read happening correctly on the wire but the C code is off by one on the buffer index during a specific interrupt overlap, that tells me it's actually a firmware race condition, not an electrical problem" — explicitly ruling hardware in or out using captured evidence rather than guessing.
5. **Fix-and-verify loop** — after a hypothesis (e.g., "clock speed too high for bus capacitance, causing occasional bit errors"), state how they'd verify the fix (slow down the clock, re-capture waveform, confirm error rate drops to zero) rather than assuming the fix worked.

### 🚩 Red Flags to Watch For
- Immediately jumping to "I'd add a retry loop" without ever mentioning a scope/logic analyzer — reveals the candidate has only ever done software-only debugging (a known gap per his current project history — the Li