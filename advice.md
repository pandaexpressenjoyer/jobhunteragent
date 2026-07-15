# 🎯 Performance Playbook: Embedded/Firmware Internship Pipeline (GTA)
### Candidate: Aditya Ganguli | Target Roles: Kepler Communications, Block (Square), ecobee, Hitachi Rail

---

## Interview Context & Strategy Rationale

Aditya presents as a strong outlier for a 2nd-year candidate — a cycle-accurate CPU emulator, real MSP432 firmware work (I2C/UART, LiDAR scanning system), and enterprise tooling exposure. However, cross-referencing his current portfolio against all four active listings reveals he is **bare-metal-only** with **no demonstrated Embedded Linux, RTOS, SPI/CAN, or structured test/debug methodology**. These four gaps are exactly where Kepler, Block, ecobee, and Hitachi Rail concentrate their technical screening. The three questions below are constructed to directly probe those seams — they are not generic "tell me about embedded systems" questions, but scenario-based prompts modeled on the literal responsibilities pulled from the job postings. Each includes the ideal engineering response strategy an interviewer should be listening for, and the specific red flags that indicate a gap has not been closed.

---

## Question 1 — Embedded Linux, Kernel/Driver Architecture, and Bare-Metal-to-Linux Transition
**(Primary target: Kepler Communications | Secondary: ecobee)**

> "Kepler's onboard satellite software runs across bare-metal firmware, Embedded Linux, and custom Yocto/OpenEmbedded builds. Walk me through how you'd take your existing MSP432 LiDAR firmware — currently a bare-metal control loop — and port its sensor-polling logic to run as a Linux kernel module or user-space driver on an embedded Linux board instead. What changes at the architecture level, and what stays the same?"

### Why this question is asked
This maps line-for-line to Kepler's JD: "Embedded Linux for both space and ground systems," "writing kernel modules and drivers," and "memory-mapped peripherals." ecobee's stack is 80% Linux across roles for the same reason. This is the single highest-leverage question because it currently sits on Aditya's #1 critical gap (Gap 1: no Embedded Linux/Yocto exposure) — the interviewer needs to know whether he understands the *conceptual* delta even if he lacks hands-on Yocto build experience yet.

### Ideal Engineering Response Strategy
A strong candidate should structure the answer around three layers, not just say "I'd rewrite it in C for Linux":
1. **Address space & memory access model** — On MSP432 bare-metal, the sensor register is accessed directly via a memory-mapped address in the linker script. On Linux, that same physical address is no longer directly addressable from user space; the candidate should articulate the need for either `/dev/mem` + `mmap()` for a quick user-space approach, or a proper character device driver exposing `ioctl`/`read` calls if built correctly.
2. **Scheduling model shift** — Bare-metal superloop → kernel gives you a real scheduler. The candidate should note that polling the I2C ToF sensor in a tight loop is now wasteful/blocking; the correct kernel-level approach uses interrupt-driven I2C (via the Linux I2C subsystem, `i2c_client` driver model) or a workqueue rather than busy-waiting.
3. **Build/toolchain implications** — Cross-compilation is now required (not just IDE-based compile/flash like Keil uVision); the candidate should reference recipe-based builds (Yocto `.bb` files) or at minimum understand that the driver needs to be built against the target kernel's headers, not the host machine's.

**Bonus signal:** if the candidate proactively mentions device tree overlays (how the Linux kernel discovers the I2C sensor at boot vs. hardcoded pin definitions in bare-metal) — this indicates genuine conceptual depth beyond memorized buzzwords.

### Red Flags
- Says "I'd just use the Arduino/MSP432 code as-is" — indicates no understanding that Linux mediates all hardware access.
- Cannot explain the difference between kernel-space and user-space driver approaches when prompted.
- No mention of interrupts/blocking vs. the polling loop they already built — shows they haven't internalized *why* Linux changes the concurrency model.

### Follow-up Probes
- "If you only had a week, would you go the `/dev/mem`+mmap route or write a proper character device driver? Justify the tradeoff."
- "How would Yocto's `.bb` recipe system know to include your driver in the final image?"

---

## Question 2 — RTOS Task Design, Priority, and Race Conditions
**(Primary target: Kepler Communications, Block, ecobee | Secondary: Hitachi Rail — real-time systems)**

> "Your LiDAR project currently runs stepper control, I2C distance polling, and UART streaming inside a single bare-metal loop. If you ported this to FreeRTOS as three separate tasks, what would you use to pass data between them, how would you assign task priorities, and what's a concrete race condition or priority inversion scenario that could break this design if you got it wrong?"

### Why this question is asked
Three of the four target listings name RTOS explicitly (Kepler: FreeRTOS; Block: "RTOS concepts, bare-metal programming"; ecobee: RTOS tagged at 20% across their stack; Hitachi Rail: "implements real-time systems"). This is Gap 2 in the skill analysis — Aditya has zero scheduler/task/semaphore experience on record. This question forces him to reason about concurrency primitives live, rather than recite a definition of RTOS.

### Ideal Engineering Response Strategy
Strong candidates should walk through this as a systems design problem, not a vocabulary quiz:
1. **Task decomposition & data passing** — Correctly identify that a `xQueue` should carry distance readings from the I2C-polling task to the UART-streaming task, decoupling their execution rates. Stepper control should run as its own task since it has hard real-time timing requirements (step pulse width) that shouldn't be blocked by I2C bus latency.
2. **Priority assignment reasoning** — The candidate should reason (not guess) that stepper motor timing is the most latency-sensitive (must not miss a step pulse deadline) and should get the highest priority; UART streaming is the least time-critical and can be lowest priority. This shows understanding of rate-monotonic-style reasoning, not memorized RTOS trivia.
3. **Concrete failure scenario** — A strong answer names a real hazard: e.g., "If the I2C polling task and UART task both try to write to a shared distance buffer without a mutex, you get a torn read — UART could stream half-old, half-new bytes." Bonus: mentioning priority inversion (a low-priority task holding a mutex needed by a high-priority task, while a medium-priority task preempts and starves both) shows they understand the classic RTOS gotcha, and ideally they'll mention priority inheritance as the FreeRTOS-native mitigation (`xSemaphoreCreateMutex` uses priority inheritance by default vs. binary semaphores which don't).

### Red Flags
- Treats "task" and "function call" as synonymous — no understanding of preemption.
- Suggests using a global variable with no synchronization primitive "since it's quick."
- Can't articulate what would visibly break (a hang, a garbled reading, a missed step) if priorities were assigned wrong — indicates theoretical-only knowledge.

### Follow-up Probes
- "Would you use a binary semaphore or a mutex for the shared buffer, and why does that distinction matter here specifically?"
- "How would this design change on Kepler's satellite hardware, where the I2C bus might be shared with other subsystems under memory/power constraints?"

---

## Question 3 — Protocol-Level Hardware Debugging & Test Methodology
**(Primary target: Block/Square, Kepler | Secondary: Hitachi Rail — test automation)**

> "You've built I2C and UART firmware, but not SPI or CAN. Say I hand you an MCP2515 CAN controller and ask you to get two ESP32 boards talking to each other over CAN by tomorrow. Walk me through your actual debug process when the first attempt doesn't work — what tools do you reach for, what's your first hypothesis, and how do you isolate whether the bug is in your code, your wiring, or the protocol timing/config?"

### Why this question is asked
Kepler requires SPI+CAN explicitly ("bonus: oscilloscopes, logic analyzers for hardware debugging"); Block requires SPI+I2C+UART+USB and explicitly flags "use debugging tools to investigate/resolve firmware issues" and "write and run tests to validate firmware behavior." This targets Gap 3 (missing SPI/CAN) and Gap 4 (weak debug-tooling story) simultaneously. Since Aditya likely hasn't touched CAN yet, this question is deliberately designed to test **debugging methodology and protocol literacy transfer** rather than memorized CAN trivia — i.e., can he reason from his I2C/UART experience into an unfamiliar protocol under pressure, which is exactly what an internship demands.

### Ideal Engineering Response Strategy
A strong candidate should demonstrate a systematic, layered debug approach (this is the real signal, more than CAN-specific knowledge):
1. **Bottom-up isolation** — Start at the physical layer before touching code: check CAN_H/CAN_L wiring, confirm the 120Ω termination resistors are present on both ends of the bus (a classic CAN gotcha that trips up first-timers), verify power/ground to the MCP2515 module.
2. **Instrumentation first** — Reach for a logic analyzer (or oscilloscope if available) to capture actual bus traffic before assuming it's a software bug. This directly answers Block/Kepler's emphasis on hardware debug tooling. The candidate should state they'd look for whether *any* signal is toggling on the bus at all before debugging bit-rate/config mismatches.
3. **Protocol-specific hypothesis ordering** — A CAN-savvy answer moves through: (a) baud rate mismatch between the two nodes, (b) missing/incorrect acknowledgment due to only one node being active on the bus (CAN requires ≥2 active nodes to ACK), (c) SPI misconfiguration between the ESP32 and MCP2515 itself (since MCP2515 is SPI-controlled) — showing they understand CAN debugging is actually nested inside an SPI debugging problem.
4. **Test discipline** — References writing a minimal loopback test first (CAN controller's intern