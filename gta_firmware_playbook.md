# 🎯 TECHNICAL INTERVIEW PERFORMANCE PLAYBOOK
## Aditya Ganguli — Embedded Systems Internship Pipeline
### Kepler Communications | Block/Square | Geotab

---

## INTERVIEW QUESTION #1: EMBEDDED LINUX & DEVICE DRIVER ARCHITECTURE
### *Criticality: HIGHEST (Required by Kepler, Geotab; Differentiator for Q-Block)*

**THE QUESTION:**

"Walk us through how you would implement a device driver in embedded Linux to interface with an SPI-based sensor. Specifically:

1. **Architecture:** Describe the difference between kernel-space driver code and userspace application code. Why would you put certain logic in each?
2. **SPI Communication:** How would you configure the SPI bus (clock polarity, phase, data rate) in the driver? Show a code sketch.
3. **Data Flow:** Once the sensor sends data via SPI, how does that data reach a userspace application that needs to log it to a file? Walk through the complete path.
4. **Real-World Constraint:** Your application requires sub-100ms latency for sensor reads. How would you ensure the driver doesn't introduce unacceptable delays? What about if the sensor sometimes takes 50ms to respond?"

---

### 📋 IDEAL ENGINEERING RESPONSE STRATEGY

#### **A. Demonstrate Architectural Understanding**

**STRONG ANSWER demonstrates:**

- [ ] **Clear kernel vs. userspace separation**
  - "Kernel-space code handles low-level hardware control (SPI configuration, interrupt servicing, buffer management). Userspace handles application logic (data filtering, logging, business logic)."
  - "I'd use a character device driver (`/dev/my_sensor`) as the interface. The kernel driver manages the SPI peripheral; userspace reads from the device node."

- [ ] **Interrupts vs. polling trade-off**
  - "For a sensor that updates frequently, I'd use SPI in interrupt-driven mode: when data arrives, the SPI controller fires an IRQ → driver's interrupt handler reads data into a ring buffer → userspace can poll or mmap the buffer."
  - "Polling would work for slow sensors, but at 100+ Hz update rates, interrupts reduce CPU waste."

- [ ] **Mention standard Linux abstractions**
  - "I'd use the `spi_device` structure from `<linux/spi/spi.h>` and implement `spi_driver` with probe/remove callbacks."
  - "For userspace communication, I could expose data via `/proc`, `/sys`, or ioctl() calls depending on the use case."

**RED FLAGS to avoid:**

- ❌ "I don't know the difference between kernel and userspace"
- ❌ "I'd just bitbang the SPI pins in userspace" (ignores Linux driver model)
- ❌ "I don't understand interrupts vs. polling"

---

#### **B. Code Sketch: SPI Configuration (Kernel Driver)**

**STRONG ANSWER provides:**

```c
// In probe() function when device is detected
#include <linux/spi/spi.h>

static int my_sensor_probe(struct spi_device *spi) {
    // Configure SPI timing/polarity
    spi->mode = SPI_MODE_0;           // CPOL=0, CPHA=0
    spi->max_speed_hz = 5000000;      // 5 MHz clock
    spi->bits_per_word = 8;
    
    // Validate configuration
    int ret = spi_setup(spi);
    if (ret < 0) {
        dev_err(&spi->dev, "SPI setup failed\n");
        return ret;
    }
    
    // Allocate driver private data
    struct my_sensor *sensor = devm_kzalloc(&spi->dev, 
                                            sizeof(*sensor), 
                                            GFP_KERNEL);
    spi_set_drvdata(spi, sensor);
    
    // Register interrupt handler
    ret = request_irq(spi->irq, sensor_irq_handler, 
                      IRQF_TRIGGER_FALLING, 
                      "my_sensor", sensor);
    
    return ret;
}

// Interrupt handler (runs in atomic context)
static irqreturn_t sensor_irq_handler(int irq, void *dev_id) {
    struct my_sensor *sensor = dev_id;
    
    // Schedule work in process context to avoid blocking
    schedule_work(&sensor->work);
    
    return IRQ_HANDLED;
}

// Work queue function (runs in process context, can sleep)
static void sensor_work_handler(struct work_struct *work) {
    struct my_sensor *sensor = container_of(work, 
                                            struct my_sensor, 
                                            work);
    
    // Perform SPI read
    u8 tx_buf[1] = {0x01};  // Command: read sensor
    u8 rx_buf[2];
    
    struct spi_transfer xfer = {
        .tx_buf = tx_buf,
        .rx_buf = rx_buf,
        .len = sizeof(rx_buf),
    };
    
    int ret = spi_sync_transfer(sensor->spi, &xfer, 1);
    if (ret < 0) {
        dev_err(&sensor->spi->dev, "SPI read failed: %d\n", ret);
        return;
    }
    
    // Store data in ring buffer
    u16 raw_value = (rx_buf[0] << 8) | rx_buf[1];
    kfifo_put(&sensor->buffer, raw_value);
    
    // Wake waiting userspace processes
    wake_up_interruptible(&sensor->wait_queue);
}
```

**Why this is strong:**

- ✅ Uses proper Linux APIs (`devm_kzalloc`, `request_irq`, `schedule_work`)
- ✅ Separates interrupt handler (atomic) from SPI read (process context)
- ✅ Shows understanding of kernel memory management (`devm_` prefix = auto-cleanup)
- ✅ Demonstrates SPI configuration specifics (mode, speed, bits-per-word)

---

#### **C. Data Flow Explanation (Complete Path)**

**STRONG ANSWER follows this narrative:**

1. **Interrupt fires (sensor data ready)**
   - Hardware SPI controller receives 16 bits from sensor
   - Controller generates IRQ → `sensor_irq_handler()` called
   
2. **Interrupt handler defers work**
   - IRQ handler must be fast → immediately calls `schedule_work()`
   - Marks sensor device as "data ready"
   
3. **Work queue processes SPI transaction**
   - Work handler runs in process context (can block/sleep)
   - Calls `spi_sync_transfer()` to read from SPI device
   - Data returned in `rx_buf`
   
4. **Data stored in kernel ring buffer**
   - Uses `kfifo_put()` to store raw sensor value
   - Ring buffer prevents data loss if userspace is slow
   
5. **Userspace wakes up**
   - `wake_up_interruptible()` signals waiting processes
   - Userspace app unblocks from `read()` syscall
   
6. **Userspace reads from `/dev/my_sensor`**
   - Application calls `read(fd, buffer, sizeof(buffer))`
   - Driver's `read()` fop copies data from ring buffer to userspace
   - Application gets raw sensor value, can log/process

```c
// Userspace code
int fd = open("/dev/my_sensor", O_RDONLY);
u16 sensor_value;

while (1) {
    read(fd, &sensor_value, sizeof(sensor_value));  // Blocks until data ready
    printf("Sensor: %u\n", sensor_value);
}
```

**Why this shows competence:**

- ✅ Explains both hardware and OS-level mechanics
- ✅ Shows understanding of latency: interrupts → work queue → ring buffer → userspace
- ✅ Addresses buffering (ring buffer prevents data loss)

---

#### **D. Real-Time Latency Constraints (Sub-100ms)**

**STRONG ANSWER addresses timing explicitly:**

"For sub-100ms latency requirement:

1. **Interrupt-driven polling is essential** – Don't poll the SPI in a loop; let hardware IRQ wake the driver.

2. **Minimize work queue deferral**
   - The work queue adds ~1–5ms on modern systems
   - For tighter latency, could use `tasklet_schedule()` instead (atomic context, but still preemptible)
   - For critical paths, could do SPI read directly in IRQ handler (risky – blocks other IRQs)

3. **Ring buffer sizing**
   - If sensor produces 1000 samples/sec, userspace reads every 50ms
   - Ring buffer needs 50+ entry capacity to avoid loss
   - Use `kfifo` for lockless circular buffer

4. **Validate with `ftrace` / kernel profiling**
   - Use Linux kernel's `ftrace` tool to measure actual IRQ-to-read latency
   - Profile the work queue handler to confirm <100ms end-to-end
   - If latency exceeds budget, move SPI read earlier (into IRQ handler) or reduce sensor sample rate

5. **If sensor takes 50ms to respond**
   - This is a hardware constraint; driver can't fix it
   - Ensure SPI transaction is non-blocking so IRQ handler doesn't stall
   - Document that end-to-end latency includes sensor response time
   - If 50ms + driver overhead exceeds 100ms budget, request faster sensor or longer timeout from system architects"

**Why this impresses interviewers:**

- ✅ Shows production-mindset thinking (latency measurement, profiling)
- ✅ Demonstrates trade-offs (IRQ vs. tasklet vs. work queue vs. polling)
- ✅ Realistic acknowledgment of hardware limits
- ✅ Proposes concrete validation method (`ftrace`)

---

### 🚩 EXPECTED FOLLOW-UP QUESTIONS & DEFLECTION STRATEGY

| Follow-Up | Aditya's Strategy |
|-----------|-------------------|
| "What if you need to support 10 SPI sensors simultaneously?" | "I'd register 10 separate IRQ handlers, each with its own ring buffer. Kernel scheduler handles context switching. For resource contention, I'd profile with `ftrace` to measure system impact." |
| "How would you handle SPI bus errors or timeouts?" | "Add retry logic in work handler. For permanent failures, use `sysfs` to expose error counters so userspace monitoring can alert. Consider CRC checking on SPI frames for data integrity." |
| "What's the difference between `request_irq()` and `request_threaded_irq()`?" | "`request_irq()` runs handler in atomic context (fast, can't block). `request_threaded_irq()` automatically defers to thread context (easier, but slightly higher latency). For SPI, I'd use `request_threaded_irq()` because SPI transactions block." |
| "How do you prevent userspace from reading stale data?" | "Use timestamps in the ring buffer entry. Userspace reads (timestamp, sensor_value). Application can discard data older than time threshold. Or use atomic swap: kernel maintains two buffers, swaps atomically on new data." |

---

## INTERVIEW QUESTION #2: FREERTOS TASK SCHEDULING & REAL-TIME CONSTRAINTS
### *Criticality: HIGH (Required by Kepler, Q-Block; Implicit in Block/Geotab)*

**THE QUESTION:**

"You're designing a real-time IoT module for Kepler's satellite that must:
- Read I2C sensor data every 100ms (Safety-critical)
- Log data to flash storage every 5 seconds
- Respond to ground commands over UART within 500ms
- Keep CPU utilization under 60% to save power

**Your tasks:**

1. **Task Design:** Design the task structure (how many tasks? priorities? stack sizes?). What OS primitives would you use for synchronization?

2. **Scheduling:** Show the task execution timeline over 10 seconds. Which task runs when? Can you guarantee the 100ms sensor read deadline?

3. **Failure Case:** What happens if the flash write (worst case: 800ms) coincides with a ground command arriving? How do you prevent the command from missing its 500ms deadline?

4. **Code:** Write the pseudocode for the I2C sensor task, including error handling and how it signals the logging task."

---

### 📋 IDEAL ENGINEERING RESPONSE STRATEGY

#### **A. Task Architecture Design**

**STRONG ANSWER demonstrates:**

- [ ] **Multi-task decomposition**
  - "I'd create three tasks:
    1. **SensorTask** (priority HIGH, 100ms period) – Reads I2C sensor
    2. **CommandTask** (priority CRITICAL, event-triggered) – Responds to UART immediately
    3. **LoggerTask** (priority LOW, 5sec period) – Writes to flash
  
  This separates real-time-critical (sensor, command) from best-effort (logging)."

- [ ] **Synchronization strategy**
  - "SensorTask fills a ring buffer with sensor readings. LoggerTask periodically drains the buffer to flash."
  - "CommandTask is event-driven: UART ISR signals a semaphore → CommandTask unblocks → handles command."
  - "Use a mutex to protect the ring buffer (shared between SensorTask and LoggerTask)."

- [ ] **Stack sizing reasoning**
  - "SensorTask: 1KB (simple I2C transaction, local variables)"
  - "CommandTask: 2KB (parses UART data, may buffer up to 256 bytes)"
  - "LoggerTask: 4KB (flash I/O may have large local buffers)"
  - "System stack: 2KB (ISRs, exception handling)"

**RED FLAGS to avoid:**

- ❌ "I'd use one big task that does everything" (ignores real-time requirements)
- ❌ "I don't know what task priorities mean"
- ❌ "I'd make all tasks the same priority" (violates deadline requirements)

---

#### **B. Task Execution Timeline (10 seconds)**

**STRONG ANSWER provides visual timeline:**

```
Time (ms) | Event                          | Running Task      | Reason
----------|--------------------------------|-------------------|------------------
0         | SensorTask wakes (period)      | SensorTask        | Preempts Logger
0–50      | I2C read (50ms worst case)     | SensorTask        | 
50        | SensorTask fills buffer        | (blocked)         | Waiting for next period
          | LoggerTask resumes             | LoggerTask        | (was preempted at 0ms)
100       | UART data arrives (interrupt)  | UART ISR (1ms)     | ISR signals Cmd semaphore
100       | CommandTask wakes              | CommandTask       | CRITICAL priority preempts all
100–150   | Parse command, prepare response| CommandTask       | 
150       | CommandTask sends UART reply   | CommandTask       | (completes in 50ms, within 500ms deadline)
150       | LoggerTask resumes             | LoggerTask        | 
200       | SensorTask wakes (2nd period)  | SensorTask        | Preempts Logger (HIGH > LOW)
200–250   | I2C read                       | SensorTask        | 
250–1000  | Alternating: Sensor (100ms)    | SensorTask/Logger | LoggerTask starves until sensor quiet
          | → Logger (in gaps)             |                   |
5000      | LoggerTask timer fires         | LoggerTask        | Logs all buffered sensor data (800ms)
5000–5800 | Flash write (may block)        | LoggerTask        | 
```

**Key insight:**
- ✅ Sensor reads **never miss 100ms deadline** (HIGH priority, only 50ms work)
- ✅ Command response **completes within 500ms** (CRITICAL priority preempts all)
- ✅ Logger completes within 5-second window (LOW priority, but sufficient time: 5000ms window – 800ms write = 4200ms idle)

**Why this demonstrates competence:**

- ✅ Shows concrete understanding of FreeRTOS priority-based preemption
- ✅ Quantifies timing margins (sensor: 100ms – 50ms = 50ms slack)
- ✅ Identifies potential issue (LoggerTask could starve) and explains why it's OK

---

#### **C. Failure Case Analysis: Conflicting Deadlines**

**STRONG