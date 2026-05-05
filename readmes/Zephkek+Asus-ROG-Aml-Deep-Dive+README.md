# The ASUS Gaming Laptop ACPI Firmware DPC Stall: A Deep Technical Investigation

> **Status update (December 2025):** The original periodic ACPI/DPC stall described in this write-up is **fixed** by an updated ASUS UEFI that rewrites the ACPI `ECLV` routine (removing sleeps/self-rearm behavior) and includes additional ACPI power-management optimizations.

## What changed

ASUS updated the firmware's ACPI EC/GPE event handling. The key change is the `ECLV` method: it no longer sleeps inside the event-processing loop and no longer self-rearms when it hits an internal "time budget".

### AML diff (old vs new)

```diff
 Method (ECLV, 0, NotSerialized)
 {
-    // Main loop - continues while events exist OR sleep events are pending
-    // AND we haven't exceeded our time budget (TI3S < 0x78)
-    While (((CKEV() != Zero) || (SLEC != Zero)) && (TI3S < 0x78))
+    While ((CKEV () != Zero))
     {
         Local1 = One
-        While (Local1 != Zero)
+        While ((Local1 != Zero))
         {
-            Local1 = GEVT()    // Get next event from queue
-            LEVN (Local1)      // Process the event
-            TIMC += 0x19       // Increment time counter by 25
-            
-            If ((SLEC != Zero) && (Local1 == Zero))
-            {
-                If (TIMC == 0x19)
-                {
-                    Sleep (0x64)
-                    TIMC = 0x64
-                    TI3S += 0x04
-                }
-                Else
-                {
-                    Sleep (0x19)
-                    TI3S++
-                }
-            }
+            Local1 = GEVT ()
+            LEVN (Local1)
         }
     }
-    
-    If (TI3S >= 0x78)
-    {
-        TI3S = Zero
-        If (EEV0 == Zero)
-        {
-            EEV0 = 0xFF
-        }
-    }
 }
```

### Updated LatencyMon results (G533ZW, UEFI 327)

<img width="1738" height="636" alt="image" src="https://github.com/user-attachments/assets/767bde14-84c7-41ea-a33f-75a71076cfb9" />


## If You're Here, You Know The Pain

You own a high-end ASUS ROG laptop perhaps a Strix, Scar, or Zephyrus. It's specifications are impressive: an RTX 30/40 series GPU, a top-tier Intel processor, and plenty of RAM. Yet, it stutters during basic tasks like watching a YouTube video, audio crackles and pops on Discord calls, the mouse cursor freezes for a split second, just long enough to be infuriating.

You've likely tried all the conventional fixes:
- Updating every driver imaginable, multiple times.
- Performing a "clean" reinstallation of Windows.
- Disabling every conceivable power-saving option.
- Manually tweaking processor interrupt affinities.
- Following convoluted multi-step guides from Reddit threads.
- Even installing Linux, only to find the problem persists.

If none of that worked, it's because the issue isn't with the operating system or a driver. The problem was embedded in the machine's firmware (UEFI) - and ASUS has since shipped a UEFI update that fixes the original periodic ACPI/DPC stall mechanism described below.

## Initial Symptoms and Measurement

### The Pattern Emerges

The first tool in any performance investigator's toolkit for these symptoms is LatencyMon. It acts as a canary in the coal mine for system-wide latency issues. On an affected ASUS Zephyrus M16, the results are immediate and damning:

```
CONCLUSION
Your system appears to be having trouble handling real-time audio and other tasks. 
You are likely to experience buffer underruns appearing as drop outs, clicks or pops.

HIGHEST MEASURED INTERRUPT TO PROCESS LATENCY
Highest measured interrupt to process latency (μs):   65,816.60
Average measured interrupt to process latency (μs):   23.29

HIGHEST REPORTED ISR ROUTINE EXECUTION TIME
Highest ISR routine execution time (μs):              536.80
Driver with highest ISR routine execution time:       ACPI.sys

HIGHEST REPORTED DPC ROUTINE EXECUTION TIME  
Highest DPC routine execution time (μs):              5,998.83
Driver with highest DPC routine execution time:       ACPI.sys
```

The data clearly implicates `ACPI.sys`. However, the per-CPU data reveals a more specific pattern:

```
CPU 0 Interrupt cycle time (s):                       208.470124
CPU 0 ISR highest execution time (μs):                536.804674
CPU 0 DPC highest execution time (μs):                5,998.834725
CPU 0 DPC total execution time (s):                   90.558238
```

CPU 0 is taking the brunt of the impact, spending over 90 seconds processing interrupts while other cores remain largely unaffected. This isn't a failure of load balancing; it's a process locked to a single core.

A similar test on a Scar 15 from 2022 shows the exact same culprit: high DPC latency originating from `ACPI.sys`.

<img width="974" height="511" alt="latencymon" src="https://github.com/user-attachments/assets/fdf6f26a-dda8-4561-82c7-349fc8c298ab" />

It's easy to blame a Windows driver, but `ACPI.sys` is not a typical driver. It primarily functions as an interpreter for ACPI Machine Language (AML), the code provided by the laptop's firmware (UEFI). If `ACPI.sys` is slow, it's because the firmware is feeding it inefficient or flawed AML code to execute. These slowdowns are often triggered by General Purpose Events (GPEs) and traffic from the Embedded Controller (EC). To find the true source, we must dig deeper.

## Capturing the Problem in More Detail: ETW Tracing

### Setting Up Advanced ACPI Tracing

To understand what `ACPI.sys` is doing during these latency spikes, we can use Event Tracing for Windows (ETW) to capture detailed logs from the ACPI providers.

```powershell
# Find the relevant ACPI ETW providers
logman query providers | findstr /i acpi
# This returns two key providers:
# Microsoft-Windows-Kernel-Acpi {C514638F-7723-485B-BCFC-96565D735D4A}
# Microsoft-ACPI-Provider {DAB01D4D-2D48-477D-B1C3-DAAD0CE6F06B}

# Start a comprehensive trace session
logman start ACPITrace -p {DAB01D4D-2D48-477D-B1C3-DAAD0CE6F06B} 0xFFFFFFFF 5 -o C:\Temp\acpi.etl -ets
logman update ACPITrace -p {C514638F-7723-485B-BCFC-96565D735D4A} 0xFFFFFFFF 5 -ets

# Then once we're done we can stop the trace and check the etl file and save the data in csv format aswell.
logman stop ACPITrace -ets
tracerpt C:\Temp\acpi.etl -o C:\Temp\acpi_events.csv -of CSV
```

### An Unexpected Discovery

Analyzing the resulting trace file in the Windows Performance Analyzer reveals a crucial insight. The spikes aren't random; they are periodic, occurring like clockwork every 30 to 60 seconds.

<img width="1673" height="516" alt="61c7abb1-d7aa-4b69-9a88-22cca7352f00" src="https://github.com/user-attachments/assets/2aac7320-3e06-4025-841c-86129f9d5b62" />

Random interruptions often suggest hardware faults or thermal throttling. A perfectly repeating pattern points to a systemic issue, a timer or a scheduled event baked into the system's logic.

The raw event data confirms this pattern:
```csv
Clock-Time (100ns),        Event,                      Kernel(ms), CPU
134024027290917802,       _GPE._L02 started,          13.613820,  0
134024027290927629,       _SB...BAT0._STA started,    0.000000,   4
134024027290932512,       _GPE._L02 finished,         -,          6
```

The first event, `_GPE._L02`, is an interrupt handler that takes **13.6 milliseconds** to execute. For a high-priority interrupt, this is an eternity and is catastrophic for real-time system performance.

Deeper in the trace, another bizarre behavior emerges; the system repeatedly attempts to power the discrete GPU on and off, even when it's supposed to be permanently active.
```csv
Clock-Time,                Event,                    Duration
134024027315051227,       _SB.PC00.GFX0._PS0 start, 278μs     # GPU Power On
134024027315155404,       _SB.PC00.GFX0._DOS start, 894μs     # Display Output Switch
134024027330733719,       _SB.PC00.GFX0._PS3 start, 1364μs    # GPU Power Off
[~15 seconds later]
134024027607550064,       _SB.PC00.GFX0._PS0 start, 439μs     # Power On Again!
134024027607657368,       _SB.PC00.GFX0._DOS start, 1079μs    # Display Output Switch
134024027623134006,       _SB.PC00.GFX0._PS3 start, 394μs     # Power Off Again!
...
```
### Note on GPU power-method activity

The trace also shows periodic GPU-related ACPI method activity (for example `_PS0`, `_PS3`, and `_DOS`) correlated with `_GPE._L02`. The exact platform intent and correctness of these GPU transitions varies by model, configuration, and UEFI version, so this write-up no longer treats this as a settled root cause. The focus below is the measured ACPI stall mechanism and its firmware fix.

### Understanding General Purpose Events

GPEs are the firmware's mechanism for signaling hardware events to the operating system. They are essentially hardware interrupts that trigger the execution of ACPI code. The trace data points squarely at `_GPE._L02` as the source of our latency.

A closer look at the timing reveals a consistent and problematic pattern:
```
_GPE._L02 Event Analysis from ROG Strix Trace:

Event 1 @ Clock 134024027290917802
  Duration: 13,613,820 ns (13.61ms)
  Triggered: Battery and AC adapter status checks

Event 2 @ Clock 134024027654496591  
  Duration: 13,647,255 ns (13.65ms)
  Triggered: Battery and AC adapter status checks
  
Event 3 @ Clock 134024028048493318
  Duration: 13,684,515 ns (13.68ms)  
  Triggered: Battery and AC adapter status checks

Interval between events: ~36-39 seconds
Consistency: The duration is remarkably stable and the interval is periodic.
```

### The Correlation

Every single time the lengthy `_GPE._L02` event fires, it triggers the exact same sequence of ACPI method calls.

<img width="589" height="589" alt="64921999-7614-4706-a5ac-54c39c38fd0b" src="https://github.com/user-attachments/assets/01326c61-b7a2-4c12-a907-8433f43a6a72" />

The pattern is undeniable:
1.  A hardware interrupt fires `_GPE._L02`.
2.  The handler executes methods to check battery status.
3.  Shortly thereafter, the firmware attempts to change the GPU's power state.
4.  The system runs normally for about 30-60 seconds.
5.  The cycle repeats.

## Extracting and Decompiling the Firmware Code

### Getting to the Source

To analyze the code responsible for this behavior, we must extract and decompile the ACPI tables provided by the UEFI to the operating system.

```bash
# Extract all ACPI tables into binary .dat files
acpidump -b

# Output includes:
# DSDT.dat - The main Differentiated System Description Table
# SSDT1.dat ... SSDT17.dat - Secondary System Description Tables

# Decompile the main table into human-readable ACPI Source Language (.dsl)
iasl -d dsdt.dat
```
This decompiled ASL provides a direct view into the firmware's executable logic. It is a precise representation of the exact instructions that the ACPI.sys driver is fed by the firmware and executes at the highest privilege level within the Windows kernel. Any logical flaws found in this code are the direct cause of the system's behavior.


### Finding the GPE Handler

Searching the decompiled `DSDT.dsl` file, we find the definition for our problematic GPE handler:

```asl
Scope (_GPE)
{
    Method (_L02, 0, NotSerialized)  // _Lxx: Level-Triggered GPE
    {
        \_SB.PC00.LPCB.ECLV ()
    }
}
```
This code is simple: when the `_L02` interrupt occurs, it calls a single method, `ECLV`. The "L" prefix in `_L02` signifies that this is a **level-triggered** interrupt, meaning it will continue to fire as long as the underlying hardware condition is active. This is a critical detail.

### The pre-fix `ECLV` implementation (historical)

In older UEFI versions, `ECLV()` looked like this. This behavior is sufficient to explain the periodic stutters/latency spikes observed in ETW and LatencyMon. Newer UEFI builds replace it (see the diff at the top of this document).

```asl
Method (ECLV, 0, NotSerialized)  // Starting at line 099244
{
    // Main loop - continues while events exist OR sleep events are pending
    // AND we haven't exceeded our time budget (TI3S < 0x78)
    While (((CKEV() != Zero) || (SLEC != Zero)) && (TI3S < 0x78))
    {
        Local1 = One
        While (Local1 != Zero)
        {
            Local1 = GEVT()    // Get next event from queue
            LEVN (Local1)      // Process the event
            TIMC += 0x19       // Increment time counter by 25
            
            // This is where it gets really bad
            If ((SLEC != Zero) && (Local1 == Zero))
            {
                // No events but sleep events pending
                If (TIMC == 0x19)
                {
                    Sleep (0x64)    // Sleep for 100 milliseconds!!!
                    TIMC = 0x64     // Set time counter to 100
                    TI3S += 0x04    // Increment major counter by 4
                }
                Else
                {
                    Sleep (0x19)    // Sleep for 25 milliseconds!!!
                    TI3S++          // Increment major counter by 1
                }
            }
        }
    }
    
    // Here's where it gets even worse
    If (TI3S >= 0x78)  // If we hit our time budget (120)
    {
        TI3S = Zero
        If (EEV0 == Zero)
        {
            EEV0 = 0xFF    // Force another event to be pending!
        }
    }
}
```

### Breaking down the pre-fix behavior

This short block of code violates several fundamental principles of firmware and kernel programming.

**Issue 1: Sleeping in an interrupt-driven path**
```asl
Sleep (0x64)    // 100ms sleep
Sleep (0x19)    // 25ms sleep
```
An interrupt handler runs at a very high priority to service hardware requests quickly. The `Sleep()` function completely halts the execution of the CPU core it is running on (CPU 0 in this case). While CPU 0 is sleeping, it cannot:
- Process any other hardware interrupts.
- Allow the kernel to schedule other threads.
- Update system timers.

> Clarification: These Sleep() calls live in the ACPI GPE handling path for the GPE L02, these calls get executed at PASSIVE_LEVEL after the SCI/GPE is acknowledged so it's not a raw ISR (because i don't think windows will even allow that) but analyzing this further while the control method runs the GPE stays masked  and the ACPI/EC work is serialized. With the Sleep() calls inside that path and the self rearm it seems to have the effect of making ACPI.sys get tied up in long periodic bursts (often on CPU 0) which still have the same effect on the system.

**Issue 2: Time-sliced event processing**
The entire loop is designed to run for an extended period, processing events in batches. It's effectively a poorly designed task scheduler running inside an interrupt handler, capable of holding a CPU core hostage for potentially seconds at a time.

**Issue 3: Self-rearming behavior**
```asl
If (EEV0 == Zero)
{
    EEV0 = 0xFF    // Forces all EC event bits on
}
```
This logic ensures that even if the Embedded Controller's event queue is empty, the code will create a new, artificial event. This guarantees that another interrupt will fire shortly after, creating the perfectly periodic pattern of ACPI spikes observed in the traces.

## The Event Dispatch System

### How Events Route to Actions

The LEVN() method takes an event and routes it:

```asl
Method (LEVN, 1, NotSerialized)
  {
      If ((Arg0 != Zero))
      {
          MBF0 = Arg0
          P80B = Arg0
          Local6 = Match (LEGA, MEQ, Arg0, MTR, Zero, Zero)
          If ((Local6 != Ones))
          {
              LGPA (Local6)
          }
      }
  }

```

### The `LGPA` Dispatch Table

The LGPA() method is a giant switch statement handling different events:

```asl
Method (LGPA, 1, Serialized)  // Line 098862
{
    Switch (ToInteger (Arg0))
    {
        Case (Zero)  // Most common case - power event
        {
            DGD2 ()       // GPU-related function
            ^EC0._QA0 ()  // EC query method
            PWCG ()       // Power change - this is our battery polling
        }
        
        Case (0x18)  // GPU-specific event
        {
            If (M6EF == One)
            {
                Local0 = 0xD2
            }
            Else
            {
                Local0 = 0xD1
            }
            NOD2 (Local0)  // Notify GPU driver
        }
        
        Case (0x1E)  // Another GPU event
        {
            Notify (^^PEG1.PEGP, 0xD5)  // Direct GPU notification
            ROCT = 0x55                  // Sets flag for follow-up
        }
       
    }
}
```
This shows a direct link: a GPE fires, and the dispatch logic calls functions related to battery polling and GPU notifications.

## The Battery Polling Function

The `PWCG()` method, called by multiple event types, is responsible for polling the battery and AC adapter status.

```asl
Method (PWCG, 0, NotSerialized)
{
    Notify (ADP0, Zero)      // Tell OS to check the AC adapter
    ^BAT0._BST ()            // Execute the Battery Status method
    Notify (BAT0, 0x80)      // Tell OS the battery status has changed
    ^BAT0._BIF ()            // Execute the Battery Information method  
    Notify (BAT0, 0x81)      // Tell OS the battery info has changed
}
```
Which we can see here:

<img width="1043" height="315" alt="image" src="https://github.com/user-attachments/assets/f6c62050-b470-49bd-ad55-35def0fff893" />

Each of these operations requires communication with the Embedded Controller, adding to the workload inside the already-stalled interrupt handler.

### The GPU Notification System

The `NOD2()` method sends notifications to the GPU driver.

```asl
Method (NOD2, 1, Serialized)
{
    If ((Arg0 != DNOT))
    {
        DNOT = Arg0
        Notify (^^PEG1.PEGP, Arg0)
    }

    If ((ROCT == 0x55))
    {
        ROCT = Zero
        Notify (^^PEG1.PEGP, 0xD1) // Hardware-Specific
    }
}
```
These notifications (`0xD1`, `0xD2`, etc.) are hardware-specific signals that tell the NVIDIA driver to re-evaluate its power state. In traces this can surface as GPU-related ACPI method activity (for example `_PSx` / `_DOS`) near the same periodic events.

## Cross-System Analysis

Traces from multiple ASUS gaming laptop models confirm this is not an isolated issue.

#### Scar 15 Analysis
- **Trace Duration:** 4.1 minutes
- **`_GPE._L02` Events:** 7 (every ~39 seconds)
- **Avg. GPE Duration:** 1.56ms 
- **GPU Power Cycles:** 8

#### Zephyrus M16 Analysis
- **Trace Duration:** 19.9 minutes
- **`_GPE._L02` Events:** 3 (same periodic pattern)
- **Avg. GPE Duration:** 2.94ms
- **GPU Power Cycles:** 197 (far more frequent)
- **ASUS WMI Calls:** 2,370 (Armoury Crate amplifying the problem)

### What Actually Breaks

The firmware acts as the hardware abstraction layer between Windows and the physical hardware. When ACPI control methods execute, they run under the Windows ACPI driver with specific timing constraints and because of these timing constraints GPE control methods need to finish quickly because the firing GPE stays masked until the method returns so sleeping or polling inside a path like that can trigger real time-glitches and produce very high latency numbers, as our tests indicate.

Microsoft's [Hardware Lab Kit GlitchFree test](https://learn.microsoft.com/windows-hardware/test/hlk/testref/f0ed5aa8-ef49-4fc9-99b6-753c857e4e2d) validates this hardware-software contract by measuring audio/video glitches during HD playback. It fails systems with driver stalls exceeding a few milliseconds because such delays break real-time guarantees needed for smooth media playback.

These ASUS systems violate those constraints. The firmware holds GPE._L02 masked for 13ms while sleeping in ECLV, serializing all ACPI/EC operations behind that delay. It polls battery state when it should use event-driven notifications. The net result is severe periodic latency spikes on otherwise high-end hardware.

### The Universal Pattern

Despite being different models, all affected systems exhibit the same core flaws:
1.  `_GPE._L02` handlers take milliseconds to execute instead of microseconds.
2.  The GPEs trigger unnecessary battery polling.
3.  Some platforms show GPU-related method activity correlated with the same periodic events.
4.  The entire process is driven by a periodic, timer-like trigger.

## Summarizing the Findings

This bug is a cascade of firmware design failures.

### Root Cause 1: The Misunderstanding of Interrupt Context

On windows, the LXX / EXX run at PASSIVE_LEVEL via ACPI.sys but while a GPE control method runs **the firing GPE stays masked** and ACPI/EC work is **serialized**. ASUS's dispatch from GPE._L02 to ECLV loops, calls Sleep(25/100ms) and re-arms the EC stretching that masked window into tens of milliseconds (which would explain the 13ms CPU time in ETW (Kernel ms) delay for GPE Events) and producing a periodic ACPI.sys burst that causes the latency problems on the system. The correct behavior is to latch or clear the event, exit the method, and signal a driver with Notify for any heavy work; do not self-rearm or sleep in this path at all.

### Root Cause 2: Flawed Interrupt Handling
The firmware artificially re-arms the interrupt, creating an endless loop of GPEs instead of clearing the source and waiting for the next legitimate hardware event. This transforms a hardware notification system into a disruptive, periodic timer.

### Root Cause 3: Lack of Platform Awareness
Some of the GPU-related ACPI activity observed alongside `_GPE._L02` remains under investigation and is not treated as a settled root cause in this write-up.

## Timeline of User Reports

### The Three-Year Pattern

This issue is not new or isolated. User reports documenting identical symptoms with high ACPI.sys DPC latency, periodic stuttering, and audio crackling have been accumulating since at least 2021 across ASUS's entire gaming laptop lineup.

**August 2021: First major reports (AMD Advantage Edition)**
The earliest documented case on the official ASUS ROG forums is a **G15 Advantage Edition (G513QY, all-AMD)** owner reporting ["severe DPC latency from ACPI.sys"](https://rog-forum.asus.com/t5/rog-strix-series/g15-advantage-edition-g513qy-severe-dpc-latency-audio-dropouts/m-p/809512) with audio dropouts under any load. The thread, last edited in March 2024, shows the issue remained unresolved for years.

**August 2021: Parallel reports (NVIDIA-based models)**
Around the same time, **separate Reddit threads on NVIDIA-based ROG models** describe [identical ACPI.sys latency problems](https://www.reddit.com/r/ASUS/comments/odprtv/high_dpc_latency_from_acpisys_can_be_caused_by/). Different GPU vendors, same firmware/ACPI failure pattern.

**2021-2023: Spreading Across Models**  
Throughout this period, the issue proliferates across ASUS's gaming lineup:
- [ROG Strix models experience micro-stutters](https://www.reddit.com/r/techsupport/comments/mxtm86/i_need_help_high_acpisys_latency_and_microstutters/)
- [TUF Gaming series reports throttling for seconds at a time](https://www.reddit.com/r/Asustuf/comments/1m2e40v/my_laptop_throttling_for_few_seconds/)
- [G18 models exhibit the characteristic 45-second periodic stuttering](https://www.reddit.com/r/techsupport/comments/17rqfq5/new_laptop_started_stuttering_every_45_seconds/)

**2023-2024: The Problem Persists in New Models**  
Even the latest generations aren't immune:
- [2023 Zephyrus M16 owners report persistent audio issues](https://www.reddit.com/r/ZephyrusM16/comments/1j33ld6/this_machine_has_been_nothing_but_problems_no/)
- [2023 G16 models continue experiencing audio pops/crackles](https://www.reddit.com/r/ZephyrusG14/comments/1l4jb13/audio_popscrackles_on_zephyrus_g16_2023/)
- [2024 Intel G16 models require workarounds for audio stuttering](https://www.reddit.com/r/ZephyrusG14/comments/1i2w9ah/resolving_audio_popsstuttering_on_2024_intel_g16/)

## Conclusion

### Status: fixed (UEFI update)

The periodic ACPI/DPC stall mechanism in this write-up was caused by firmware behavior inside `ECLV` (sleeping/polling and self-rearming in the EC/GPE event path). ASUS has since shipped a UEFI update that rewrites `ECLV` to process queued events without sleeping and without artificial self-rearm, and also optimizes additional ACPI power-management methods.

If you were here for the original "ACPI.sys latency spikes every ~30–60 seconds" symptom: update to the latest UEFI for your model and then capture fresh LatencyMon screenshots in the section above.

### Ongoing investigation

Separate from the original DPC stall, other platform stability/power-management issues are still being investigated (including PCIe power-management configuration problems such as LTR L1.2 threshold mismatches). That work is outside the scope of this specific "DPC stall" write-up.

> Update 1: ASUS has officially put out a statement: https://x.com/asus_rogna/status/1968404596658983013?s=46

> Update 2: Reply from ASUS RD received; repro info sent over

> Update 3: Asus sent me beta UEFI, currently testing. (https://x.com/ASUS_ROGNA/status/1971662996339646645/photo/1)

> Update 4: Updated UEFI shipped; `ECLV` rewritten and the periodic ACPI/DPC stall is resolved (see the diff and new LatencyMon screenshots above).






























