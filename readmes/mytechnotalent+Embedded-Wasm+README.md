# Embedded Wasm 

> See also: [Embedded Hacking](https://github.com/mytechnotalent/Embedded-Hacking) — A FREE comprehensive step-by-step embedded hacking course covering Embedded Software Development to Reverse Engineering.

A collection of repos that runs a WebAssembly Component Model runtime (wasmtime + Pulley interpreter) directly on bare-metal w/ HW capabilities exposed through WIT.

<br>

## Why Run Wasm on a Microcontroller?

A traditional embedded project compiles C or Rust directly to ARM machine code, flashes it, and runs it. It is simple, fast, and uses minimal RAM. So why add a WebAssembly runtime to a device with 512 KiB of memory?

**Sandboxing.** The Wasm guest runs inside a sandbox enforced by Wasmtime. It cannot access arbitrary memory, call arbitrary functions, or touch hardware directly. Every interaction with the outside world goes through a WIT-defined interface that the host explicitly implements. A bug or exploit in the guest cannot corrupt the host firmware, overwrite stack frames, or hijack peripherals. On a traditional bare-metal C binary, a single buffer overflow in application logic can take over the entire device.

**Portable application logic.** The Wasm component is compiled once to `wasm32-unknown-unknown` and runs on any host that implements the same WIT interface. The same blinky guest that runs on an RP2350 through Pulley could run on an ESP32, an STM32, or a Linux desktop — without recompilation. The hardware-specific code lives in the host firmware; the application logic is platform-independent.

**Separation of concerns.** The WIT interface creates a hard contract between the application developer and the firmware developer. The application developer writes guest code against `gpio.set-high(pin: u32)` and `timing.delay-ms(ms: u32)` without knowing or caring how GPIO or timing work on the target hardware. The firmware developer implements those interfaces against the HAL. Either side can be updated, replaced, or audited independently.

**Safe over-the-air updates.** Because the Wasm component is sandboxed and interface-bound, you could update the guest application without reflashing the entire firmware. A new `.cwasm` blob can be loaded from flash, UART, or a network interface, deserialized by the existing Wasmtime engine, and executed — with the guarantee that it can only do what the WIT interface allows. A corrupted or malicious update cannot escape the sandbox.

**Flash wear reduction.** The NOR flash memory used in microcontrollers has a finite lifespan — typically rated for 100,000 program/erase cycles per sector (the RP2350's Winbond W25Q16JV is rated for exactly this). Every full firmware reflash erases and rewrites the sectors containing code. In a traditional C firmware, any change to application logic — even a one-line fix — requires reflashing the entire binary, burning through those erase cycles. With a Wasm-based architecture, the host firmware is flashed once and stays put. Application updates are delivered as new `.cwasm` blobs that can be loaded from a dedicated flash region, written to a separate sector, or streamed directly into RAM over UART without touching the firmware sectors at all. This extends the usable life of the flash and avoids the failure mode where a device in the field becomes unupdatable because its flash has been erased too many times.

**Language flexibility.** Any language that compiles to Wasm can produce a guest component — Rust, C, C++, TinyGo, AssemblyScript, or Zig. The host firmware does not need to change. This means a team can write performance-critical drivers in Rust and application logic in whatever language fits their workflow, all communicating through typed WIT interfaces.

**The tradeoff is RAM.** The Wasmtime runtime, Pulley interpreter, and guest linear memory consume approximately 300 KiB of the RP2350's 512 KiB. A native C blinky uses roughly 4 KiB. You are paying for isolation, portability, and a well-defined security boundary. On devices where those properties matter — updatable field devices, multi-tenant firmware, safety-critical systems — the RAM cost is worth it. On a throwaway prototype that blinks an LED, it is not.

<br>

## How It All Fits Together

Every repo in this collection shares the same architecture: a bare-metal Rust firmware that boots an RP2350 microcontroller, compiles a WebAssembly component ahead of time, and executes it through the Wasmtime runtime's Pulley interpreter. The Wasm guest calls back into the host for hardware access (GPIO, UART, timers) through interfaces defined in WIT.

The dependency stack has three layers — **hardware**, **Wasm runtime**, and **glue** — and each crate plays a specific role.

### Hardware Layer

These crates give the firmware direct access to the RP2350's Cortex-M33 core and peripherals.

- **[cortex-m](https://docs.rs/cortex-m)** — Low-level access to ARM Cortex-M registers, interrupts, and intrinsics. The firmware uses it to disable/enable interrupts and access core peripherals like the SysTick timer.

- **[cortex-m-rt](https://docs.rs/cortex-m-rt)** — The Cortex-M startup runtime. It provides the reset vector, initializes `.bss` and `.data` sections, and calls `main()`. The `#[entry]` attribute macro marks the firmware's entry point.

- **[rp235x-hal](https://docs.rs/rp235x-hal)** — The RP2350 Hardware Abstraction Layer. It wraps the chip's raw registers into safe Rust types for clocks, GPIO pins, UART peripherals, and more. Every hardware operation — toggling an LED, reading a button, sending a UART byte — goes through this crate.

- **[embedded-hal](https://docs.rs/embedded-hal)** — A set of traits that define portable hardware interfaces (GPIO, UART, SPI, I2C). The firmware codes against these traits so the same logic works across different HALs as the `rp235x-hal` implements these traits for the RP2350.

- **[fugit](https://docs.rs/fugit)** — Type-safe time units for embedded systems. Baud rates (`115_200.Hz()`) and clock frequencies (`150.MHz()`) are expressed as `fugit` types, catching unit mismatches at compile time.

- **[critical-section](https://docs.rs/critical-section)** — Cross-platform interrupt-safe mutual exclusion. The firmware uses it to protect shared global state (UART handle, GPIO pins) from interrupt races. `rp235x-hal` provides the platform-specific critical section implementation.

### Wasm Runtime Layer

These crates compile, encode, and execute WebAssembly components on the microcontroller.

- **[Wasmtime](https://docs.wasmtime.dev)** ([API docs](https://docs.rs/wasmtime)) — The WebAssembly runtime. At build time, Wasmtime's Cranelift backend compiles the guest `.wasm` into Pulley bytecode. At run time, Wasmtime's engine deserializes this precompiled component and executes it through the Pulley interpreter. The `Engine`, `Store`, `Component`, and `Linker` types orchestrate the entire lifecycle.

- **[Cranelift](https://cranelift.dev)** ([API docs](https://docs.rs/cranelift-codegen)) — The compiler backend used during `build.rs` to AOT-compile Wasm into Pulley bytecode. It runs on the host machine (not the MCU) and produces a serialized artifact that gets embedded into the firmware binary.

- **[Pulley](https://docs.rs/pulley-interpreter)** — Wasmtime's portable interpreter bytecode format. Instead of compiling Wasm to native ARM instructions, the pipeline compiles to Pulley bytecode, which Wasmtime's built-in interpreter executes on any architecture — including the Cortex-M33. This is what makes Wasm on a microcontroller possible without a native code generator for Thumb-2.

- **[WIT / Component Model](https://component-model.bytecodealliance.org)** ([wit-bindgen docs](https://docs.rs/wit-bindgen)) — The interface definition language that describes what the Wasm guest can import from the host (e.g., `gpio.set-high`, `button.is-pressed`, `timing.delay-ms`). `wit-bindgen` generates guest-side Rust bindings, and Wasmtime's `bindgen!` macro generates host-side bindings. The `wit-component` crate encodes a core Wasm module into a Component Model component during the build.

### Glue Layer

- **[embedded-alloc](https://docs.rs/embedded-alloc)** — A heap allocator for `no_std` environments. Wasmtime needs heap allocation for its `Store`, `Engine`, and component instantiation. The firmware carves out a fixed-size heap from RAM and registers this allocator as the `#[global_allocator]`.

### The Wasm Build Pipeline

Before diving into this project's specific artifacts, it helps to understand how source code becomes WebAssembly in general. The pipeline mirrors a traditional native build — preprocessing, compiling, assembling, linking — but the target is a portable bytecode format instead of a specific CPU's instruction set.

**1. Preprocessing and Compiling.** Your toolchain (Clang/LLVM for C/C++, `rustc` for Rust) reads source code and translates it into WebAssembly instructions instead of ARM or x86 machine code. The compiler front-end works the same way it always does — parsing, type checking, optimization — but the back-end emits Wasm opcodes (`i32.add`, `call`, `local.get`, etc.) rather than native instructions.

**2. Assembling (WAT to Wasm).** WebAssembly has its own human-readable assembly language called WAT (WebAssembly Text format). WAT uses nested S-expressions — parenthesized prefix notation that looks similar to Lisp. For example, a function that adds two integers:

```wat
(func $add (param $a i32) (param $b i32) (result i32)
  local.get $a
  local.get $b
  i32.add)
```

The assembler takes WAT instructions and encodes them into the compact binary format: a `.wasm` file. This `.wasm` file is the Wasm equivalent of a native object file (`.o`) or standalone executable. In practice, compilers like `rustc` emit the binary `.wasm` directly — you only see WAT when you disassemble with `wasm-tools print`.

**3. Linking.** This is where Wasm diverges from native builds. There are two fundamentally different kinds of linking:

- **Static linking (building a module).** If your project is made of multiple source files, the Wasm linker (`wasm-ld`) takes the individual object files and links them together into a single `.wasm` module — just like a native linker produces a single ELF or PE binary. The result is one self-contained module with all internal references resolved.

- **Component linking (composing modules).** This is the Component Model's contribution. When you want to connect two independently compiled Wasm modules — say a `checkout.wasm` that calls a `pdf.wasm` — you are taking two fully built, complete binary modules and wiring their typed imports and exports together through WIT interfaces. Each module retains its own isolated linear memory and internal state. The connection happens at the interface boundary, not by merging code. This is fundamentally different from native static linking, where everything collapses into one address space.

In this project, the guest (`wasm-app/`) is statically linked into a single core `.wasm` module (Artifact 1 below), then component-encoded with WIT type information (Artifact 2), and finally AOT-compiled to Pulley bytecode (Artifact 3). The component linking between host and guest happens at runtime when Wasmtime's `Linker` wires the host's Rust implementations to the guest's WIT imports.

### The Wasm Compilation Pipeline

The build produces three distinct Wasm artifacts. Each one is a transformation of the previous, and understanding all three is essential to understanding how code written in Rust ends up executing on a microcontroller through a WebAssembly runtime.

#### Artifact 1: Core Wasm Module (`.wasm`)

**What it is:** A standard WebAssembly module compiled from the guest Rust source code.

**Where it lives:** `wasm-app/target/wasm32-unknown-unknown/release/wasm_app.wasm`

**How it is produced:** `build.rs` spawns `cargo build --release --target wasm32-unknown-unknown` inside the `wasm-app/` directory. The Rust compiler (`rustc`) compiles `wasm-app/src/lib.rs` into a core Wasm module. Because the guest uses `wit-bindgen`, the compiler also embeds Component Model type metadata as a custom section inside this `.wasm` file. This metadata describes the WIT imports and exports the guest expects.

**What is inside:** Standard Wasm sections — types, functions, tables, memories, globals, exports, and code. Plus custom sections injected by `wit-bindgen` that describe the component type signature. At this stage, the file is a plain core module — it has no Component Model envelope yet.

**How to inspect it:**
```bash
# Install wasm-tools (one-time)
cargo install wasm-tools

# Print the WAT (WebAssembly Text Format) — human-readable disassembly
wasm-tools print wasm-app/target/wasm32-unknown-unknown/release/wasm_app.wasm

# Validate the module
wasm-tools validate wasm-app/target/wasm32-unknown-unknown/release/wasm_app.wasm

# Dump raw section headers and sizes
wasm-tools dump wasm-app/target/wasm32-unknown-unknown/release/wasm_app.wasm

# Show the component type metadata embedded by wit-bindgen
wasm-tools metadata show wasm-app/target/wasm32-unknown-unknown/release/wasm_app.wasm
```

#### Artifact 2: Component-Encoded Wasm (in-memory only)

**What it is:** A Wasm Component Model component that wraps the core module with typed imports and exports matching the WIT definition.

**Where it lives:** Only in memory — inside `build.rs` as the `component_bytes` variable in `compile_wasm_to_pulley()`. It is never written to disk because it is immediately passed to the Cranelift compiler.

**How it is produced:** `build.rs` reads the core `.wasm` file (Artifact 1) and feeds it to `wit_component::ComponentEncoder`. The encoder reads the custom sections that `wit-bindgen` embedded, validates them against the WIT definition, and wraps the core module in a Component Model envelope. The result is a fully-typed component with:
- **Typed imports** — `embedded:platform/gpio.set-high(pin: u32)`, `embedded:platform/timing.delay-ms(ms: u32)`, etc.
- **Typed exports** — `run: func()`
- **Canonical ABI adapters** — shim functions that translate between the Component Model's typed interface and the core module's raw integer-based calling convention

The `ComponentEncoder` is the library version of `wasm-tools component new`. Using it as a library avoids a subprocess call and keeps the entire pipeline in-process.

**What is inside:** A Component Model binary — it contains the original core module nested inside, plus component-level type sections, import/export declarations, and canonical lifting/lowering adapters.

**How to inspect it (if you write it to disk for debugging):**
```bash
# You can temporarily add this line to build.rs to dump it:
# std::fs::write(out.join("component.wasm"), &component_bytes).unwrap();

# Then inspect the component
wasm-tools print component.wasm
wasm-tools component wit component.wasm # extract the WIT back out
wasm-tools validate --features component-model component.wasm
```

#### Artifact 3: Precompiled Pulley Bytecode (`.cwasm`)

**What it is:** A serialized, AOT-compiled blob of Pulley interpreter bytecode. This is the final artifact — the one that actually runs on the RP2350.

**Where it lives:** `$OUT_DIR/blinky.cwasm` (e.g., `target/thumbv8m.main-none-eabihf/release/build/embedded-wasm-blinky-<hash>/out/blinky.cwasm`). It is embedded directly into the firmware ELF binary via `include_bytes!` in `main.rs`:
```rust
const WASM_BINARY: &[u8] = include_bytes!(concat!(env!("OUT_DIR"), "/blinky.cwasm"));
```

**How it is produced:** `build.rs` creates a Wasmtime `Engine` configured to target `pulley32` (the 32-bit Pulley interpreter). It then calls `engine.precompile_component(&component_bytes)` which invokes Cranelift to compile every function in the component (Artifact 2) into Pulley bytecode. The result is serialized into a platform-independent blob.

The engine configuration is critical — it must exactly match the runtime engine on the MCU:
- `target("pulley32")` — compile for the 32-bit Pulley interpreter, not native ARM
- `signals_based_traps(false)` — bare-metal has no OS signal handlers for traps
- `memory_init_cow(false)` — no virtual memory, no copy-on-write page tricks
- `memory_reservation(0)` — no virtual address space to reserve (embedded target)
- `memory_guard_size(0)` — no guard pages (no MMU/MPU-based trap detection)
- `guard_before_linear_memory(false)` — no pre-guard pages
- `max_wasm_stack(16384)` — 16 KiB Wasm stack (constrained by available RAM)

If the build-time and run-time engine configurations do not match, deserialization will fail at boot with a version/config mismatch error.

**What is inside:** Serialized Wasmtime metadata plus compiled Pulley bytecode for every function. This is not a standard Wasm format — it is a Wasmtime-internal serialization format. You cannot inspect it with `wasm-tools`.

**How to inspect it:**
```bash
# .cwasm files are Wasmtime-internal format, not standard Wasm
# You can check the file size to verify it was produced
ls -lh $OUT_DIR/blinky.cwasm

# To verify it loads correctly, the firmware itself is the test —
# Engine::deserialize() at boot will reject any corrupt or mismatched blob
```

### The Build-to-Boot Sequence

Here is the complete sequence from source code to blinking LED, showing exactly which crate does what and when:

**Phase 1: WIT Definition (developer writes once)**

The developer defines the hardware interface contract in `wit/world.wit`:
```wit
package embedded:platform;

interface gpio {
    set-high: func(pin: u32);
    set-low: func(pin: u32);
}

interface timing {
    delay-ms: func(ms: u32);
}

world blinky {
    import gpio;
    import timing;
    export run: func();
}
```

This single file drives code generation on both sides — the guest uses `wit-bindgen` to generate Rust import stubs, and the host uses Wasmtime's `bindgen!` to generate Rust trait implementations.

**Phase 2: Build Script (`cargo build` triggers `build.rs`)**

When you run `cargo build`, Cargo executes `build.rs` on the host machine before compiling the firmware. The build script runs four steps in sequence:

1. **Write linker script** — copies `rp2350.x` (the RP2350 memory layout: Flash at `0x10000000`, RAM at `0x20000000`) into `$OUT_DIR/memory.x` so `cortex-m-rt` knows where to place code and data

2. **Compile Wasm guest** — spawns `cargo build --release --target wasm32-unknown-unknown` inside `wasm-app/` as Rust compiles the guest code + `wit-bindgen` stubs into a core Wasm module (Artifact 1)

3. **Encode as component** — `ComponentEncoder` from `wit-component` wraps the core module into a Component Model component (Artifact 2, in-memory only)

4. **AOT-compile to Pulley** — Wasmtime's `Engine` (with Cranelift backend) compiles the component into Pulley bytecode and writes `blinky.cwasm` to `$OUT_DIR/` (Artifact 3)

**Phase 3: Firmware Compilation (`rustc` compiles `src/main.rs`)**

After `build.rs` finishes, Cargo compiles the firmware source. The `include_bytes!` macro bakes the `.cwasm` blob directly into the firmware's `.rodata` section. The result is a single ELF binary that contains both the ARM firmware code and the precompiled Wasm bytecode.

**Phase 4: Flashing**

`probe-rs download --chip RP235x firmware.elf` writes the ELF to the RP2350's flash memory at `0x10000000`.

**Phase 5: Boot (`cortex-m-rt` starts the Cortex-M33)**

On power-up, the RP2350's Boot ROM reads the image definition from the `.start_block` section, verifies it, and jumps to the reset vector. `cortex-m-rt` takes over:
1. Initializes `.bss` (zero-fills) and `.data` (copies from Flash to RAM)
2. Calls the function marked `#[entry]` — which is `main()`

**Phase 6: Hardware Initialization (`main()` in `src/main.rs`)**

`main()` brings up the hardware in order:
1. `init_heap()` — carves 256 KiB from RAM and registers `embedded-alloc` as `#[global_allocator]`
2. `init_clocks()` — configures the RP2350's PLLs and clock tree to 150 MHz via `rp235x-hal`
3. `init_hardware()` — initializes UART0 (GPIO0/GPIO1 at 115200 baud) and GPIO25 (the onboard LED) via `rp235x-hal` + `embedded-hal` traits
4. Calls `run_wasm()` to enter the Wasm execution loop

**Phase 7: Wasm Execution (`Wasmtime` runs the guest)**

`run_wasm()` sets up and executes the Wasm component:
1. `create_engine()` — creates a Wasmtime `Engine` with the same `pulley32` configuration used at build time
2. `Engine::deserialize()` — loads the precompiled `.cwasm` bytes (the `WASM_BINARY` constant) back into a `Component` as no compilation happens here — the bytecode is ready to execute
3. `build_linker()` — creates a `Linker` and registers host implementations for every WIT import (`gpio.set-high`, `gpio.set-low`, `timing.delay-ms`)
4. `execute_wasm()` — creates a `Store` (which holds the host state), instantiates the component through the linker, and calls the guest's exported `run()` function

**Phase 8: Guest Execution (Pulley interpreter runs the guest code)**

The guest's `run()` function executes inside the Pulley interpreter. It enters an infinite loop:
1. Calls `gpio.set-high(25)` -> crosses the Wasm boundary -> host drives GPIO25 high via `rp235x-hal`
2. Calls `timing.delay-ms(500)` -> crosses the Wasm boundary -> host spins for 500 ms
3. Calls `gpio.set-low(25)` -> crosses the Wasm boundary -> host drives GPIO25 low
4. Calls `timing.delay-ms(500)` -> crosses the Wasm boundary -> host spins for 500 ms
5. Back to step 1

Each "crosses the Wasm boundary" means the Pulley interpreter hits a host-call instruction, suspends guest execution, calls the host function registered in the `Linker`, and resumes the guest when it returns.

### Inspecting Wasm Artifacts

Install the [`wasm-tools`](https://github.com/bytecodealliance/wasm-tools) CLI to inspect and debug the Wasm artifacts produced by the build:

```bash
cargo install wasm-tools
```

| Command                                                | What it does                                                                |
| ------------------------------------------------------ | --------------------------------------------------------------------------- |
| `wasm-tools print <file>.wasm`                         | Disassemble to WAT (human-readable text format)                             |
| `wasm-tools validate <file>.wasm`                      | Validate a core module or component                                         |
| `wasm-tools dump <file>.wasm`                          | Dump raw binary sections and offsets                                        |
| `wasm-tools component wit <file>.wasm`                 | Extract the WIT interface from a component                                  |
| `wasm-tools metadata show <file>.wasm`                 | Show embedded metadata (producers, component type)                          |
| `wasm-tools component new core.wasm -o component.wasm` | Manually encode a core module as a component (what `ComponentEncoder` does) |
| `wasm-tools stats <file>.wasm`                         | Show size breakdown by section                                              |

### Reverse Engineering `.cwasm` Files

The `.cwasm` format is Wasmtime's internal serialization — undocumented, version-specific, and changes between Wasmtime releases without notice. There is no off-the-shelf disassembler or inspection tool. `wasm-tools` cannot read `.cwasm` files because they are not standard Wasm.

**Important:** The `.cwasm` ELF is **not** the same ELF that runs on the device. The firmware `.elf` (e.g., `embedded-wasm-blinky.elf`) is a Cortex-M33 ARM ELF binary — it contains the Wasmtime runtime, all host-side glue code, and the `.cwasm` blob embedded as a raw byte array via `include_bytes!`. The `.cwasm` ELF is a Wasmtime-internal container that holds Pulley bytecode and serialized metadata; it never executes directly on hardware. At boot, the firmware's `Engine::deserialize()` reads the `.cwasm` bytes out of flash, parses the ELF structure, validates the engine configuration, and feeds the Pulley bytecode into the interpreter. The two ELF files serve completely different purposes: the firmware ELF is loaded by `probe-rs` onto the RP2350's flash and executed by the Cortex-M33 core, while the `.cwasm` ELF is consumed at runtime by the Wasmtime engine running inside that firmware.

To reverse engineer a `.cwasm`, you would need to work through four layers:

**1. Parse the ELF container.** The `.cwasm` file is a valid ELF binary — not a custom magic-bytes format. Wasmtime marks it with a custom `ELFOSABI_WASMTIME` OS/ABI tag and uses `e_flags` to distinguish modules from components. Engine configuration metadata (version, compiler flags, tunables) is stored in a dedicated ELF section. This is how `Engine::deserialize()` detects config mismatches — if any flag differs between the engine that compiled the blob and the engine trying to load it, deserialization fails immediately. The ELF detection and compatibility-check logic lives in Wasmtime's source at [`crates/wasmtime/src/engine/serialization.rs`](https://github.com/bytecodealliance/wasmtime/blob/main/crates/wasmtime/src/engine/serialization.rs). Because it is a valid ELF, you can load a `.cwasm` file into [Ghidra](https://ghidra-sre.org/) and it will parse the ELF structure — sections, headers, and segment layout. However, the code sections contain Pulley bytecode (not native ARM/x86 machine code), so Ghidra cannot disassemble the instructions without a custom processor module for the Pulley ISA (none exists publicly).

**2. Deserialize the metadata.** The engine-configuration ELF section contains `postcard`-serialized metadata: target triple, compiler flags, ISA flags, tunables, and enabled Wasm features. Additional ELF sections hold function signatures, memory layout, trap tables, component type information, and canonical ABI adapter descriptions. Deserializing this requires matching the exact schema from the same Wasmtime version that produced the file. A version mismatch will produce garbage or deserialization errors.

**3. Extract the Pulley bytecode.** The compiled code sections contain raw Pulley interpreter instructions — a stack-based bytecode format designed for portability across architectures. There is no standalone CLI disassembler for Pulley. To decode the instructions, you would write a small Rust program using the [`pulley-interpreter`](https://docs.rs/pulley-interpreter) crate's `Decoder` API, which can step through the bytecode opcode-by-opcode and print each instruction.

**4. Map back to source.** The `.cwasm` does not contain DWARF debug info or source maps. To understand what a Pulley function does, cross-reference it by function index against the original `.wasm` file (Artifact 1), which you can disassemble with `wasm-tools print`. The `.cwasm` preserves the same function indices, so function 0 in the `.cwasm` corresponds to function 0 in the `.wasm`.

**In practice:** If you want to analyze what the Wasm guest is doing, inspect the `.wasm` (Artifact 1) with `wasm-tools print` — it contains the same logic in a standard, well-documented format. The `.cwasm` adds nothing semantically; it is a pre-compiled representation of the same code optimized for instant loading on the target device.

### Embedded Wasm Memory Challenges and How This Project Solves Them

Running WebAssembly on a microcontroller with 512 KiB of RAM and no MMU introduces memory challenges that do not exist on desktop or server targets. These are well-known pain points in the embedded Wasm space, and this project's architecture is specifically designed to avoid them.

**Challenge 1: 64 KiB Wasm page size vs. limited RAM.**
The WebAssembly specification defines a fixed page size of 64 KiB. On a device with 512 KiB of total RAM, a single `memory.grow` adds 64 KiB — over 12% of all available memory. Projects that pass strings, byte buffers, or lists across the WIT boundary trigger `cabi_realloc` inside the guest, which calls `memory.grow` to obtain heap space. Two pages of linear memory alone consume 128 KiB.

**How we avoid it:** All WIT interfaces in this project pass only `u32` scalars — `set-high(pin: u32)`, `delay-ms(ms: u32)`, `is-pressed(pin: u32) -> bool`. The canonical ABI does not need heap allocation to marshal a single integer across the boundary. The guest's initial linear memory (1 page = 64 KiB) is sufficient for its static data and stack, and `memory.grow` is never invoked. Page size is irrelevant when memory never grows.

**Challenge 2: Forced `memory.grow` from the guest allocator.**
Compiling to `wasm32-unknown-unknown` produces a guest where the default allocator treats all initial memory as the Wasm image. It immediately calls `memory.grow` to obtain heap space, forcing a minimum of 2 pages (128 KiB) for any component that performs dynamic allocation. The `#[global_allocator]` is required because `wit-bindgen` emits a `cabi_realloc` symbol that the linker demands.

**How we avoid it:** Our guests declare a `#[global_allocator]` (satisfying the linker) but never actually allocate. The blinky guest, for example, is an infinite loop of `set_high` / `delay_ms` / `set_low` / `delay_ms` — all stack-based, zero heap allocations. The allocator exists as dead code because our scalar-only WIT types never trigger `cabi_realloc` at runtime.

**Challenge 3: No-MMU reallocation overhead.**
Without virtual memory, linear memory must be physically contiguous. Growing from 1 to 2 pages requires the host to allocate 2 new contiguous pages, copy the original page, and free the old block — temporarily requiring 3 pages (192 KiB) of contiguous RAM for what ends up as a 2-page allocation.

**How we avoid it:** Since our guests stay within the initial 64 KiB page, the realloc-copy-free cycle never triggers. The engine configuration reinforces this: `memory_reservation(0)`, `memory_guard_size(0)`, `memory_reservation_for_growth(0)`, and `guard_before_linear_memory(false)` tell Wasmtime not to reserve any address space beyond what is immediately needed.

**Challenge 4: Multi-component memory multiplication.**
When composing multiple Wasm components (e.g., a sensor driver, a display driver, and application logic as separate components), each retains its own isolated linear memory. The page-size overhead and `memory.grow` penalties described above multiply for every sub-component, quickly exhausting available RAM.

**How we avoid it:** Each repo in this collection runs exactly one Wasm component with one linear memory. There is no multi-component composition. All hardware complexity lives in the host firmware (Rust), and the single Wasm guest is deliberately lightweight — it orchestrates hardware calls through WIT imports but performs no complex data processing itself.

**The design principle:** Keep the Wasm guest trivial and the WIT boundary scalar-only. All complexity — hardware drivers, UART I/O, clock configuration, pin management — lives in the host firmware where it has direct access to hardware and unconstrained memory. The Wasm layer provides sandboxing and portability for the application logic without paying the memory tax that comes with passing rich data types across the component boundary.

### Performance: Wasm Overhead vs. Native C Firmware

The natural question when running WebAssembly on a microcontroller is: how much slower is it compared to native C or Rust firmware without Wasm? For this project's architecture, the answer is effectively **zero measurable overhead** — not because Wasm is free, but because of where the time is actually spent.

**What runs through the Pulley interpreter:** The Wasm guest's loop body — a branch instruction, a function call setup, and scalar argument passing. In the blinky guest, that is roughly 10-20 Pulley bytecode instructions per iteration. At 150 MHz, the interpreter executes those in single-digit microseconds.

**What runs as native ARM code:** Every host call — `set_high`, `set_low`, `delay_ms`, `is_pressed`, `read_byte`, `write_byte` — crosses the Wasm boundary and executes as compiled Rust/ARM firmware. The GPIO register write takes approximately 10 nanoseconds. A `delay_ms(500)` call spins natively for 500 milliseconds. These are identical to what native C firmware would execute.

**Per-cycle overhead comparison (blinky example at 150 MHz):**

| Operation                | Native C/Rust      | This Project                                                           |
| ------------------------ | ------------------ | ---------------------------------------------------------------------- |
| GPIO register write      | ~10 ns             | ~10 ns (same register write, from host) + ~5 µs (Pulley call overhead) |
| 500 ms delay             | 500 ms (busy wait) | 500 ms (same busy wait, in host)                                       |
| Total per-cycle overhead | 0                  | ~10 µs                                                                 |
| Full cycle time          | ~1000 ms           | ~1000.01 ms                                                            |
| Overhead percentage      | 0%                 | ~0.001%                                                                |

**When Wasm overhead would matter:** If the Wasm guest performed heavy computation inside the Pulley interpreter — math, sorting, string processing, data transformation — you would see 20-50x slowdown compared to native code, which is typical for a well-optimized bytecode interpreter. This project deliberately avoids that by keeping all computation and hardware I/O in the native host firmware. The guest is a thin orchestration layer that sequences hardware calls through WIT imports.

**The real cost is RAM, not speed.** The Wasmtime runtime, Pulley interpreter, component metadata, and 64 KiB guest linear memory consume approximately 300 KiB of the RP2350's 512 KiB RAM. A native C blinky uses roughly 4 KiB. That is the fundamental tradeoff: sandboxing and portability in exchange for RAM. On a device where every kilobyte counts, this is a deliberate architectural choice — you are paying for the ability to run untrusted or portable Wasm components, isolated from the host, with a well-defined WIT interface contract.

<br>

## Repos

## embedded-wasm-uart-rp2350
A pure Embedded Rust UART echo project that runs a WebAssembly Component Model runtime (Wasmtime + Pulley interpreter) directly on the RP2350 bare-metal w/ HW capabilities exposed through WIT.

-> Click [HERE](https://github.com/mytechnotalent/embedded-wasm-uart-rp2350) to access the repo.

## embedded-wasm-blinky-rp2350
A pure Embedded Rust blinky project that runs a WebAssembly Component Model runtime (Wasmtime + Pulley interpreter) directly on the RP2350 bare-metal w/ HW capabilities exposed through WIT.

-> Click [HERE](https://github.com/mytechnotalent/embedded-wasm-blinky-rp2350) to access the repo.

## embedded-wasm-button-rp2350
A pure Embedded Rust button project that runs a WebAssembly Component Model runtime (Wasmtime + Pulley interpreter) directly on the RP2350 bare-metal with hardware capabilities exposed through WIT.

-> Click [HERE](https://github.com/mytechnotalent/embedded-wasm-button-rp2350) to access the repo.

## embedded-wasm-servo-rp2350
A pure Embedded Rust servo project that runs a WebAssembly Component Model runtime (Wasmtime + Pulley interpreter) directly on the RP2350 bare-metal with hardware capabilities exposed through WIT.

-> Click [HERE](https://github.com/mytechnotalent/embedded-wasm-servo-rp2350) to access the repo.

<br>

## License

- [MIT License](LICENSE)
