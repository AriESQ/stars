![Build Status](https://img.shields.io/github/actions/workflow/status/jit89/PicoButtonAsync/compile-test.yml?label=build)
![Latest Release](https://img.shields.io/github/v/release/jit89/PicoButtonAsync?color=blue)
![License](https://img.shields.io/github/license/jit89/PicoButtonAsync)

# PicoButtonAsync

A fast, multicore-safe button management library for the **RP2040** and **RP2350** (Raspberry Pi Pico/Pico 2). This library is designed for projects requiring reliability, non-interference with other hardware resources (e.g Timers, Wi-Fi/USB stack etc), and low-latency input detection that does not block the main execution loop.

## 🚀 Key Features

### 1. Fast and Efficient
Unlike traditional libraries that loop through pins sequentially, `PicoButtonAsync` utilizes **parallel bitwise integration**. 
* **Bit-Shift Operations:** The library snapshots the entire GPIO bank in a single CPU cycle using the SIO (Single-cycle IO) bus.
* **Minimal Overhead:** Debounce history is processed for all buttons simultaneously using bitwise AND/OR logic. This ensures that handling 30 buttons consumes nearly the same CPU resources as handling one.

### 2. Robust Independent State Tracking
Standard button logic often suffers from "state-stealing," where one function (like `justPressed`) clears a transition flag before another function (like `justReleased`) can see it. 
* **Dual Trackers:** We implement separate internal tracking variables for `justPressed` and `justReleased`. Even though it increases the code size, but the gain in reliability is several folds.
* **Order Independent:** The logic functions can be called in any order, or skipped entirely, without breaking the internal state machine. This makes the library immune to logic bugs common in complex, non-linear code.

### 3. Async Context & System Compatibility
Built on the Raspberry Pi Pico SDK `async_context` architecture with the following considerations:
* **Non-Blocking:** It uses a background software timer rather than a raw hardware alarm.
* **Context Aware:** It is fully compatible with **CYW43 Wi-Fi** and **USB** async contexts. By using a low-priority interrupt (`0xC0`), it ensures that time-critical networking tasks always take precedence, preventing Wi-Fi disconnections or USB timing errors.

### 4. Multi-Core and Interrupt Safe
Safe for dual-core use in RP2040/RP2350:
* **Hardware Spinlocks:** Internally uses SDK critical sections (`critical_section_t`) to prevent data corruption when **Core 0** and **Core 1** access button states simultaneously.
* **ISR Safe:** Safely checks button states inside other interrupts or high-priority tasks without causing system deadlocks.

### 5. Simple and Clean User API
* No `update()` function/method calls in the main `void loop()` to update the internal state of the button debouncer.
* Polling the button state is handled internally by the class using a timer and `millis()` function.
* Simple function names like `justPressed()`, `justReleased()` to catch falling and rising edges.

## 🛠 API Usage

### `DebounceManager`

The background engine that samples and filters noise.

| Method | Description |
| --- | --- |
| **`DebounceManager(interval_ms)`** | Initialize with a sampling rate (default is 5ms). |
|**`begin()`** | Starts the background sampling task. |
| **`getSafeState()`** | Returns the raw 32-bit debounced bitmask. |
| **`checkChord(mask)`** | Returns `true` if all pins in the provided mask are held simultaneously. |

### `PicoButton`

The user-facing interface for individual pins.

| Method | Description |
| --- | --- |
| **`justPressed()`** | Returns `true` only at the instant the button is pushed. |
| **`justReleased()`** | Returns `true` only at the instant the button is released. |
| **`justLongPressed(ms)`** | Returns `true` once after the button has been held for the specified duration. |
| **`repeat(delay, interval)`** | Returns `true` at specified intervals while held (ideal for menu navigation). |

## 💻 Basic Example

```cpp
#include <PicoButtonAsync.h>

// 1. Initialize the manager (5ms sampling)
DebounceManager debouncer(5);

// 2. Define your buttons on specific GPIO pins
PicoButton btnA(debouncer, 14);
PicoButton btnB(debouncer, 15);

void setup() {
    Serial.begin(115200);
    
    // 3. Start the background sampling
    debouncer.begin();
}

void loop() {
    // Each function tracks state independently!
    if (btnA.justPressed()) {
        Serial.println("Button A: Leading edge detected.");
    }

    if (btnB.justLongPressed(1000)) {
        Serial.println("Button B: 1-Second Long Press achieved.");
    }

    // Example of a Chord (A and B held together)
    uint32_t chordMask = (1UL << 14) | (1UL << 15);
    if (debouncer.checkChord(chordMask)) {
        static uint32_t lastChord = 0;
        if (millis() - lastChord > 500) {
            Serial.println("CHORD: A+B are held!");
            lastChord = millis();
        }
    }
}
```

## ⚙️ Technical Considerations

On the RP2040 and RP2350, hardware interrupts are tied to the core that enabled them.

- If you call `debouncer.begin()` inside the standard setup(), the background sampling ISR will execute on **Core 0**.

- If you call `debouncer.begin()` inside `setup1()`, the ISR will execute on **Core 1**. This allows you to offload all button sampling overhead to a specific core, ensuring your primary application timing remains jitter-free.

- This is not a very lightweight library:
    - The library ensures thread safety and reliability in a multi-core environment while trying to be as fast as possible while alsominimising interference with other software stacks present in the pico C SDK.
    - If you want to look for a ultra-low memory button debouncing library, you should go with one that has a lower total memory footprint.
  - Even though the functions of the `PicoButton` class are safe to be called from within the ISR, it is not recommended. The ISR should be as short as possible and functions like `justLongPressed` should not be used from within the ISR.

## ⚠️ Important Notes

- **Active-Low Logic:** This library assumes a standard wiring configuration where the button connects the GPIO to GND. It automatically enables internal PULLUP resistors.

- **The Ghost Guard:** Includes logic that automatically resets timers if a button is physically released during a long loop() delay. This prevents a quick tap from being misread as a "Long Press" if the CPU was occupied elsewhere.

- **Sample Window:** To calculate the total debounce time, multiply interval_ms by DEBOUNCE_SAMPLES (default is 8). With 5ms intervals, the button must be stable for 40ms to trigger a state change.

## 📚 Theoretical Overview

The main driver logic of the code is based on:

- **A Guide to Debouncing** by Jack Ganssle
    - https://www.ganssle.com/debouncing.pdf
    - https://www.ganssle.com/debouncing-pt2.htm

- High Level API (C-SDK) for Raspberry Pi Pico:
    - [**`async_context`**](https://www.raspberrypi.com/documentation/pico-sdk/high_level.html#group_pico_async_context)
    - [**`critical_section_t`**](https://www.raspberrypi.com/documentation/pico-sdk/high_level.html#group_pico_async_context)

 ## 🤝 Credits & Acknowledgments
 - [Jack Ganssle](https://www.ganssle.com/debouncing.pdf)
 - [Earle Philhower](https://github.com/earlephilhower/arduino-pico)
